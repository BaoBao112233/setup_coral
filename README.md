# Coral USB Accelerator Setup

This repository provides automated setup scripts and documentation for the Google Coral USB Accelerator, a USB device that adds an Edge TPU coprocessor to your system for fast machine learning inference.

## About Coral USB Accelerator

The Coral USB Accelerator is a USB accessory with an Edge TPU chip inside that provides fast ML inferencing for TensorFlow Lite models. It's perfect for prototyping on-device inferencing for embedded systems.

**Key Features:**
- High-speed ML inferencing on device
- USB 3.0 connectivity (also works with USB 2.0)
- Support for TensorFlow Lite models
- Compatible with Linux, Windows, and macOS

**Official Documentation:** https://www.coral.ai/docs/accelerator/get-started/

## Quick Start

### Linux (Debian/Ubuntu/Raspberry Pi)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/BaoBao112233/setup_coral.git
   cd setup_coral
   ```

2. **Run the automated setup script:**
   ```bash
   chmod +x setup_coral.sh
   bash setup_coral.sh
   ```

3. **Test the installation:**
   ```bash
   python3 test_coral.py
   ```

### Manual Installation

If you prefer to install manually or are on a different platform, follow the platform-specific instructions below.

## Platform-Specific Instructions

### Linux (Debian/Ubuntu)

1. **Add Coral repository:**
   ```bash
   echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
   curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   sudo apt-get update
   ```

2. **Install Edge TPU runtime:**
   ```bash
   # Standard performance (recommended, runs cooler)
   sudo apt-get install libedgetpu1-std
   
   # OR Maximum performance (faster, may run hot)
   # sudo apt-get install libedgetpu1-max
   ```

3. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

### Raspberry Pi

Same as Linux instructions above. Works on:
- Raspberry Pi 4
- Raspberry Pi 3
- Raspberry Pi Zero 2 W
- Other models with USB support

**Note:** For Raspberry Pi 5 with Bookworm OS, you may need to use Docker or downgrade to Bullseye due to Python version requirements.

### Windows

1. **Install Prerequisites:**
   - Install [Python 3.7-3.9](https://www.python.org/downloads/)
   - Install [Visual C++ 2019 Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe)

2. **Download Edge TPU Runtime:**
   - Download from: https://github.com/google-coral/edgetpu/releases/latest
   - Extract and run `install.bat`
   - Select "No" when asked about maximum performance mode (recommended)

3. **Install Python libraries:**
   ```cmd
   pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
   pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
   ```

4. **Install USB driver:**
   - Connect the Coral USB Accelerator
   - Install the "Google Universal Serial Bus devices" driver when prompted

### macOS

1. **Install Edge TPU runtime:**
   ```bash
   # Download the runtime
   curl -O https://github.com/google-coral/edgetpu/releases/download/v2.0.0/edgetpu_runtime_20210119.zip
   unzip edgetpu_runtime_20210119.zip
   cd edgetpu_runtime
   sudo bash install.sh
   ```

2. **Install Python libraries:**
   ```bash
   pip3 install -r requirements.txt
   ```

## Verifying Installation

After installation, verify everything is working:

1. **Check USB device is detected:**
   ```bash
   # Linux/macOS
   lsusb | grep "Global Unichip"
   
   # Windows (Device Manager)
   # Should show "Google Coral USB Accelerator" under Universal Serial Bus devices
   ```

2. **Run the test script:**
   ```bash
   python3 test_coral.py
   ```

   You should see output like:
   ```
   ✓ TensorFlow Lite runtime is installed
   ✓ PyCoral library is installed
   ✓ Edge TPU device(s) found
   ```

## Usage Examples

### Basic Image Classification

```python
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
from PIL import Image

# Load the model
interpreter = make_interpreter('model.tflite')
interpreter.allocate_tensors()

# Load and preprocess image
image = Image.open('image.jpg')
common.set_input(interpreter, image)

# Run inference
interpreter.invoke()

# Get results
classes = classify.get_classes(interpreter, top_k=3)
for c in classes:
    print(f'{c.id}: {c.score:.5f}')
```

### List Available Edge TPU Devices

```python
from pycoral.utils import edgetpu

devices = edgetpu.list_edge_tpus()
for device in devices:
    print(device)
```

## Example Projects

Explore these official examples to get started:

1. **Image Classification:** https://github.com/google-coral/pycoral/tree/master/examples
2. **Object Detection:** https://github.com/google-coral/examples-camera
3. **Transfer Learning:** https://coral.ai/docs/edgetpu/retrain-classification/

## Troubleshooting

### Device Not Detected

**Linux:**
```bash
# Check if device is connected
lsusb | grep "Global Unichip"

# Check dmesg for errors
dmesg | grep -i usb

# Try different USB port (USB 3.0 preferred)
```

**Permissions Issue:**
```bash
# Add user to plugdev group
sudo usermod -a -G plugdev $USER

# Log out and log back in for changes to take effect
```

### Python Import Errors

```bash
# Reinstall PyCoral and TensorFlow Lite
pip3 uninstall pycoral tflite_runtime
pip3 install -r requirements.txt
```

### Performance Issues

- Use USB 3.0 port for best performance
- Consider installing the maximum performance runtime (libedgetpu1-max)
- Note: Maximum performance runtime may cause the device to run hot

### Model Compatibility

- Only TensorFlow Lite models compiled for Edge TPU will run on the accelerator
- Use the [Edge TPU Compiler](https://coral.ai/docs/edgetpu/compiler/) to convert models
- Pre-compiled models available at: https://coral.ai/models/

## File Structure

```
setup_coral/
├── README.md              # This file
├── setup_coral.sh         # Automated setup script for Linux
├── test_coral.py          # Test script to verify installation
├── requirements.txt       # Python dependencies
└── .gitignore            # Git ignore file
```

## Performance Modes

The Edge TPU runtime comes in two performance modes:

1. **Standard (libedgetpu1-std)** - Recommended
   - Lower clock frequency
   - Runs cooler
   - Suitable for most applications

2. **Maximum (libedgetpu1-max)**
   - Higher clock frequency
   - Better performance
   - May run hot during sustained use
   - Requires adequate cooling

## System Requirements

- **Operating System:** 
  - Linux (Debian, Ubuntu, or derivatives)
  - Raspberry Pi OS
  - Windows 10/11
  - macOS 10.14 or later

- **Python:** 3.7, 3.8, or 3.9 (3.9 recommended for newer systems)

- **USB:** USB 2.0 or 3.0 port (3.0 recommended for best performance)

- **RAM:** 1GB minimum (2GB+ recommended)

## Additional Resources

- **Official Website:** https://coral.ai/
- **Documentation:** https://coral.ai/docs/
- **PyCoral API Reference:** https://coral.ai/docs/reference/py/
- **GitHub Repositories:**
  - PyCoral: https://github.com/google-coral/pycoral
  - Examples: https://github.com/google-coral/examples-camera
  - Edge TPU Runtime: https://github.com/google-coral/edgetpu

## Contributing

Contributions are welcome! If you find issues or have improvements:

1. Fork this repository
2. Create a feature branch
3. Submit a pull request

## License

This setup repository is provided as-is for educational and development purposes. Please refer to Google's Coral documentation for official licensing information.

## Support

For issues specific to this setup repository, please open an issue on GitHub.

For Coral device support, visit:
- Coral Forums: https://coral.ai/community/
- GitHub Issues: https://github.com/google-coral/edgetpu/issues

---

**Note:** This is an unofficial setup guide. Always refer to the official Coral documentation at https://coral.ai/docs/accelerator/get-started/ for the most up-to-date information.