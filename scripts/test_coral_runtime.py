#!/usr/bin/env python3
"""Kiểm tra EdgeTPU runtime và pycoral.

Chạy: `python3 scripts/test_coral_runtime.py`
"""
import ctypes
import sys


def check_libedgetpu():
    try:
        ctypes.CDLL('libedgetpu.so.1')
        print('EdgeTPU runtime found (libedgetpu.so.1 loaded).')
        return True
    except OSError as e:
        print('EdgeTPU runtime not found or not loadable:', e)
        return False


def check_pycoral():
    try:
        import pycoral  # type: ignore
        print('pycoral import succeeded (package available).')
        return True
    except Exception:
        # Try a more specific import path used by pycoral utilities
        try:
            from pycoral.utils.edgetpu import make_interpreter  # type: ignore
            print('pycoral utilities import succeeded.')
            return True
        except Exception as e:
            print('pycoral not importable:', e)
            return False


def main():
    ok_lib = check_libedgetpu()
    ok_py = check_pycoral()

    print('\nSummary:')
    if ok_lib and ok_py:
        print('  All checks passed: runtime and pycoral are available.')
        sys.exit(0)
    if ok_lib and not ok_py:
        print('  Runtime found but pycoral missing. Consider: `sudo apt install python3-pycoral` or install in venv with `pip install pycoral`.')
        sys.exit(2)
    if not ok_lib:
        print('  Edge TPU runtime missing or not loadable. Ensure you installed `libedgetpu1-std` and device is connected.')
        sys.exit(1)


if __name__ == '__main__':
    main()
