#!/bin/bash
# Download sample models and test images for Coral USB Accelerator
# This script downloads pre-compiled models and sample images for testing

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Downloading Sample Models and Images ===${NC}"
echo ""

# Create directories
mkdir -p models
mkdir -p test_images

# Download MobileNet V2 model (Image Classification)
echo -e "${GREEN}Downloading MobileNet V2 (Image Classification)...${NC}"
if [ ! -f "models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite" ]; then
    wget -O models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
        https://github.com/google-coral/test_data/raw/master/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite
    echo -e "${GREEN}✓ Downloaded MobileNet V2 model${NC}"
else
    echo -e "${YELLOW}Model already exists, skipping...${NC}"
fi

# Download labels for MobileNet V2
echo -e "${GREEN}Downloading labels...${NC}"
if [ ! -f "models/inat_bird_labels.txt" ]; then
    wget -O models/inat_bird_labels.txt \
        https://github.com/google-coral/test_data/raw/master/inat_bird_labels.txt
    echo -e "${GREEN}✓ Downloaded labels${NC}"
else
    echo -e "${YELLOW}Labels already exist, skipping...${NC}"
fi

# Download sample image (parrot)
echo -e "${GREEN}Downloading sample image...${NC}"
if [ ! -f "test_images/parrot.jpg" ]; then
    wget -O test_images/parrot.jpg \
        https://github.com/google-coral/test_data/raw/master/parrot.jpg
    echo -e "${GREEN}✓ Downloaded sample image${NC}"
else
    echo -e "${YELLOW}Sample image already exists, skipping...${NC}"
fi

# Download SSD MobileNet (Object Detection)
echo -e "${GREEN}Downloading SSD MobileNet V2 (Object Detection)...${NC}"
if [ ! -f "models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite" ]; then
    wget -O models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite \
        https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite
    echo -e "${GREEN}✓ Downloaded SSD MobileNet model${NC}"
else
    echo -e "${YELLOW}Model already exists, skipping...${NC}"
fi

# Download COCO labels
if [ ! -f "models/coco_labels.txt" ]; then
    wget -O models/coco_labels.txt \
        https://github.com/google-coral/test_data/raw/master/coco_labels.txt
    echo -e "${GREEN}✓ Downloaded COCO labels${NC}"
else
    echo -e "${YELLOW}COCO labels already exist, skipping...${NC}"
fi

echo ""
echo -e "${GREEN}=== Download Complete! ===${NC}"
echo ""
echo "Downloaded files:"
echo "  Models:"
echo "    - models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite"
echo "    - models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
echo "  Labels:"
echo "    - models/inat_bird_labels.txt"
echo "    - models/coco_labels.txt"
echo "  Images:"
echo "    - test_images/parrot.jpg"
echo ""
echo "Try running:"
echo "  python3 classify_image.py --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --image test_images/parrot.jpg --labels models/inat_bird_labels.txt"
echo ""
echo "  python3 benchmark.py --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite"
echo ""
