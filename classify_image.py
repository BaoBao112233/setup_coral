#!/usr/bin/env python3
"""
Simple inference example for Coral USB Accelerator
This demonstrates basic image classification using a pre-trained model.
"""

import argparse
import time
from pathlib import Path

try:
    from pycoral.adapters import classify
    from pycoral.adapters import common
    from pycoral.utils.edgetpu import make_interpreter
    from PIL import Image
except ImportError as e:
    print(f"Error: Required library not installed: {e}")
    print("Please run: pip3 install -r requirements.txt")
    exit(1)


def load_labels(path):
    """Load labels from file."""
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def run_inference(model_path, image_path, labels_path=None, top_k=3):
    """Run inference on an image using Edge TPU."""
    
    # Load the TFLite model and allocate tensors
    print(f"Loading model: {model_path}")
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()
    
    # Get model input size
    input_details = interpreter.get_input_details()
    _, height, width, _ = input_details[0]['shape']
    print(f"Model input size: {width}x{height}")
    
    # Load and resize image
    print(f"Loading image: {image_path}")
    image = Image.open(image_path).convert('RGB').resize((width, height), Image.LANCZOS)
    
    # Run inference
    print("Running inference...")
    start_time = time.perf_counter()
    
    common.set_input(interpreter, image)
    interpreter.invoke()
    
    inference_time = (time.perf_counter() - start_time) * 1000
    print(f"Inference time: {inference_time:.1f} ms")
    
    # Get results
    classes = classify.get_classes(interpreter, top_k=top_k)
    
    # Load labels if provided
    labels = None
    if labels_path and Path(labels_path).exists():
        labels = load_labels(labels_path)
    
    # Print results
    print(f"\nTop {top_k} results:")
    print("-" * 50)
    for i, c in enumerate(classes, 1):
        label = labels[c.id] if labels else f"Class {c.id}"
        print(f"{i}. {label}")
        print(f"   Score: {c.score:.5f} ({c.score*100:.2f}%)")
    
    return classes


def main():
    parser = argparse.ArgumentParser(
        description='Run image classification on Coral USB Accelerator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python3 classify_image.py --model model.tflite --image cat.jpg
  python3 classify_image.py --model model.tflite --image cat.jpg --labels labels.txt
  
Note: The model must be compiled for Edge TPU.
Download pre-compiled models from: https://coral.ai/models/
        """
    )
    
    parser.add_argument(
        '--model',
        required=True,
        help='Path to .tflite model file (must be compiled for Edge TPU)'
    )
    
    parser.add_argument(
        '--image',
        required=True,
        help='Path to input image'
    )
    
    parser.add_argument(
        '--labels',
        help='Path to labels file (optional)'
    )
    
    parser.add_argument(
        '--top_k',
        type=int,
        default=3,
        help='Number of top results to display (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Verify files exist
    if not Path(args.model).exists():
        print(f"Error: Model file not found: {args.model}")
        return 1
    
    if not Path(args.image).exists():
        print(f"Error: Image file not found: {args.image}")
        return 1
    
    if args.labels and not Path(args.labels).exists():
        print(f"Warning: Labels file not found: {args.labels}")
        print("Continuing without labels...")
        args.labels = None
    
    # Run inference
    try:
        run_inference(args.model, args.image, args.labels, args.top_k)
        return 0
    except Exception as e:
        print(f"\nError during inference: {e}")
        print("\nTroubleshooting:")
        print("  - Ensure the Coral USB Accelerator is connected")
        print("  - Verify the model is compiled for Edge TPU")
        print("  - Run 'python3 test_coral.py' to check setup")
        return 1


if __name__ == '__main__':
    exit(main())
