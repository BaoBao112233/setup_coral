#!/usr/bin/env python3
"""
Benchmark script for Coral USB Accelerator
This script measures the inference performance of the Edge TPU.
"""

import argparse
import time
import statistics
from pathlib import Path

try:
    from pycoral.adapters import common
    from pycoral.utils.edgetpu import make_interpreter
    from PIL import Image
    import numpy as np
except ImportError as e:
    print(f"Error: Required library not installed: {e}")
    print("Please run: pip3 install -r requirements.txt")
    exit(1)


def benchmark_model(model_path, iterations=100):
    """Benchmark inference speed on Edge TPU."""
    
    print(f"Loading model: {model_path}")
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()
    
    # Get model input details
    input_details = interpreter.get_input_details()
    _, height, width, channels = input_details[0]['shape']
    print(f"Model input shape: {height}x{width}x{channels}")
    
    # Create a random input image
    print(f"Generating random input data...")
    random_input = Image.fromarray(
        np.random.randint(0, 255, (height, width, channels), dtype=np.uint8)
    )
    
    # Warmup runs
    print("Warming up (5 iterations)...")
    for _ in range(5):
        common.set_input(interpreter, random_input)
        interpreter.invoke()
    
    # Benchmark runs
    print(f"\nRunning benchmark ({iterations} iterations)...")
    inference_times = []
    
    for i in range(iterations):
        start_time = time.perf_counter()
        common.set_input(interpreter, random_input)
        interpreter.invoke()
        elapsed = (time.perf_counter() - start_time) * 1000  # Convert to ms
        inference_times.append(elapsed)
        
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{iterations} iterations", end='\r')
    
    print()  # New line after progress
    
    # Calculate statistics
    mean_time = statistics.mean(inference_times)
    median_time = statistics.median(inference_times)
    stdev_time = statistics.stdev(inference_times) if len(inference_times) > 1 else 0
    min_time = min(inference_times)
    max_time = max(inference_times)
    
    # Calculate inferences per second
    fps = 1000 / mean_time
    
    # Print results
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Model: {Path(model_path).name}")
    print(f"Iterations: {iterations}")
    print(f"Input shape: {height}x{width}x{channels}")
    print("-" * 60)
    print(f"Mean inference time:   {mean_time:.2f} ms")
    print(f"Median inference time: {median_time:.2f} ms")
    print(f"Std deviation:         {stdev_time:.2f} ms")
    print(f"Min inference time:    {min_time:.2f} ms")
    print(f"Max inference time:    {max_time:.2f} ms")
    print("-" * 60)
    print(f"Throughput:            {fps:.1f} FPS")
    print("=" * 60)
    
    return inference_times


def main():
    parser = argparse.ArgumentParser(
        description='Benchmark Coral USB Accelerator performance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python3 benchmark.py --model model.tflite
  python3 benchmark.py --model model.tflite --iterations 1000
  
Note: The model must be compiled for Edge TPU.
        """
    )
    
    parser.add_argument(
        '--model',
        required=True,
        help='Path to .tflite model file (must be compiled for Edge TPU)'
    )
    
    parser.add_argument(
        '--iterations',
        type=int,
        default=100,
        help='Number of inference iterations (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Verify model exists
    if not Path(args.model).exists():
        print(f"Error: Model file not found: {args.model}")
        return 1
    
    if args.iterations < 1:
        print("Error: Iterations must be at least 1")
        return 1
    
    # Run benchmark
    try:
        benchmark_model(args.model, args.iterations)
        return 0
    except Exception as e:
        print(f"\nError during benchmark: {e}")
        print("\nTroubleshooting:")
        print("  - Ensure the Coral USB Accelerator is connected")
        print("  - Verify the model is compiled for Edge TPU")
        print("  - Run 'python3 test_coral.py' to check setup")
        return 1


if __name__ == '__main__':
    exit(main())
