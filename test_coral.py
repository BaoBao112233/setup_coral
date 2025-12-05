#!/usr/bin/env python3
"""
Test script for Coral USB Accelerator
This script verifies that the Edge TPU is properly installed and accessible.
"""

import sys

def test_tflite_runtime():
    """Test if TensorFlow Lite runtime is installed"""
    try:
        import tflite_runtime
        print("✓ TensorFlow Lite runtime is installed")
        print(f"  Version: {tflite_runtime.__version__}")
        return True
    except ImportError as e:
        print("✗ TensorFlow Lite runtime is NOT installed")
        print(f"  Error: {e}")
        return False

def test_pycoral():
    """Test if PyCoral library is installed"""
    try:
        import pycoral
        print("✓ PyCoral library is installed")
        return True
    except ImportError as e:
        print("✗ PyCoral library is NOT installed")
        print(f"  Error: {e}")
        return False

def test_edge_tpu():
    """Test if Edge TPU is accessible"""
    try:
        from pycoral.utils import edgetpu
        
        # List available Edge TPU devices
        devices = edgetpu.list_edge_tpus()
        
        if devices:
            print("✓ Edge TPU device(s) found:")
            for device in devices:
                print(f"  - {device}")
            return True
        else:
            print("✗ No Edge TPU devices found")
            print("  Make sure the Coral USB Accelerator is connected")
            return False
    except Exception as e:
        print("✗ Error accessing Edge TPU")
        print(f"  Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Coral USB Accelerator Test")
    print("=" * 50)
    print()
    
    results = []
    
    print("Testing TensorFlow Lite runtime...")
    results.append(test_tflite_runtime())
    print()
    
    print("Testing PyCoral library...")
    results.append(test_pycoral())
    print()
    
    print("Testing Edge TPU access...")
    results.append(test_edge_tpu())
    print()
    
    print("=" * 50)
    if all(results):
        print("✓ All tests passed! Your Coral USB Accelerator is ready to use.")
        print()
        print("Next steps:")
        print("  - Try the examples: https://github.com/google-coral/pycoral/tree/master/examples")
        print("  - Read the documentation: https://coral.ai/docs/")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print()
        print("Troubleshooting:")
        print("  - Run the setup script: bash setup_coral.sh")
        print("  - Check USB connection: lsusb | grep 'Global Unichip'")
        print("  - Verify udev rules are set up correctly")
        print("  - Try unplugging and reconnecting the device")
        return 1

if __name__ == "__main__":
    sys.exit(main())
