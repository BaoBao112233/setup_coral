# Quick Reference Guide - Coral USB Accelerator

## Installation Commands

### Linux/Raspberry Pi - Automated
```bash
chmod +x setup_coral.sh
bash setup_coral.sh
```

### Linux/Raspberry Pi - Manual
```bash
# Add repository
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update

# Install runtime (choose one)
sudo apt-get install libedgetpu1-std  # Standard performance
# OR
sudo apt-get install libedgetpu1-max  # Maximum performance

# Install Python packages
pip3 install -r requirements.txt
```

### Windows
```cmd
# 1. Install Visual C++ Redistributable
# 2. Download and run Edge TPU runtime installer
# 3. Install Python packages
pip install -r requirements.txt
```

### macOS
```bash
# Download and install runtime
curl -O https://github.com/google-coral/edgetpu/releases/download/v2.0.0/edgetpu_runtime_20210119.zip
unzip edgetpu_runtime_20210119.zip
cd edgetpu_runtime
sudo bash install.sh

# Install Python packages
pip3 install -r requirements.txt
```

## Testing Commands

### Test Installation
```bash
python3 test_coral.py
```

### Check USB Device
```bash
# Linux/macOS
lsusb | grep "Global Unichip"

# Expected output: "Bus XXX Device XXX: ID 1a6e:089a Global Unichip Corp."
```

### List Edge TPU Devices (Python)
```python
from pycoral.utils import edgetpu
print(edgetpu.list_edge_tpus())
```

## Usage Examples

### Run Image Classification
```bash
python3 classify_image.py --model model_edgetpu.tflite --image photo.jpg --labels labels.txt
```

### Benchmark Performance
```bash
python3 benchmark.py --model model_edgetpu.tflite --iterations 100
```

### Basic Python Example
```python
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common, classify
from PIL import Image

# Load model
interpreter = make_interpreter('model_edgetpu.tflite')
interpreter.allocate_tensors()

# Prepare image
image = Image.open('image.jpg')
common.set_input(interpreter, image)

# Run inference
interpreter.invoke()

# Get results
classes = classify.get_classes(interpreter, top_k=3)
```

## Troubleshooting

### Device Not Found
```bash
# Check USB connection
lsusb | grep "Global Unichip"

# Check dmesg for errors
dmesg | grep -i "usb"

# Try different USB port (USB 3.0 preferred)
```

### Permission Issues
```bash
# Add user to plugdev group
sudo usermod -a -G plugdev $USER

# Logout and login for changes to take effect
```

### Reinstall Python Packages
```bash
pip3 uninstall pycoral tflite_runtime
pip3 install -r requirements.txt
```

## Common File Paths

### Edge TPU Runtime
- **Linux:** `/usr/lib/libedgetpu.so.1.0`
- **Windows:** `C:\Program Files\EdgeTPU\`
- **macOS:** `/usr/local/lib/libedgetpu.1.dylib`

### Configuration
- **Linux repository list:** `/etc/apt/sources.list.d/coral-edgetpu.list`

## Performance Tips

1. **Use USB 3.0** port for best performance
2. **Choose runtime wisely:**
   - `libedgetpu1-std` - Cooler, adequate for most tasks
   - `libedgetpu1-max` - Faster, but runs hot
3. **Batch processing** - Process multiple images in sequence for efficiency
4. **Model optimization** - Use quantized models compiled for Edge TPU

## Getting Models

### Pre-compiled Models
Download from: https://coral.ai/models/

Popular models:
- **MobileNet V2** - Image classification
- **SSD MobileNet** - Object detection  
- **EfficientNet** - High accuracy classification
- **PoseNet** - Pose estimation

### Compile Your Own Model
```bash
# Install Edge TPU Compiler
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
sudo apt-get update
sudo apt-get install edgetpu-compiler

# Compile TFLite model
edgetpu_compiler model.tflite
# Output: model_edgetpu.tflite
```

## Useful Links

- **Official Docs:** https://coral.ai/docs/
- **Models:** https://coral.ai/models/
- **PyCoral GitHub:** https://github.com/google-coral/pycoral
- **Examples:** https://github.com/google-coral/pycoral/tree/master/examples
- **Community:** https://coral.ai/community/

## Python API Reference

### Most Used Functions

```python
# Make interpreter for Edge TPU
from pycoral.utils.edgetpu import make_interpreter
interpreter = make_interpreter('model.tflite')

# List devices
from pycoral.utils import edgetpu
devices = edgetpu.list_edge_tpus()

# Classification
from pycoral.adapters import classify
classes = classify.get_classes(interpreter, top_k=5)

# Object detection
from pycoral.adapters import detect
objects = detect.get_objects(interpreter, score_threshold=0.5)

# Common utilities
from pycoral.adapters import common
common.set_input(interpreter, data)
output = common.output_tensor(interpreter, 0)
```

## System Requirements

- **OS:** Linux, Windows 10+, macOS 10.14+
- **Python:** 3.7, 3.8, or 3.9
- **USB:** 2.0 or 3.0 port
- **RAM:** 1GB minimum, 2GB+ recommended

## File Descriptions

- `setup_coral.sh` - Automated setup for Linux
- `test_coral.py` - Verify installation
- `classify_image.py` - Image classification example
- `benchmark.py` - Performance testing
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation
- `QUICK_REFERENCE.md` - This file
