#!/bin/bash
# Coral USB Accelerator Setup Script
# This script automates the installation of the Coral USB Accelerator on Linux systems
# Based on official documentation: https://www.coral.ai/docs/accelerator/get-started/

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Coral USB Accelerator Setup ===${NC}"
echo ""

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
else
    echo -e "${RED}Cannot detect OS. This script is for Linux systems.${NC}"
    exit 1
fi

echo -e "${YELLOW}Detected OS: $OS $VER${NC}"
echo ""

# Check if running as root for installation
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}Running as root${NC}" 
else
   echo -e "${YELLOW}This script requires sudo privileges for installation${NC}"
   echo "You may be prompted for your password..."
   echo ""
fi

# Update package list
echo -e "${GREEN}Step 1: Updating package list...${NC}"
sudo apt-get update

# Install prerequisites
echo -e "${GREEN}Step 2: Installing prerequisites...${NC}"
sudo apt-get install -y curl gnupg ca-certificates

# Add Coral repository
echo -e "${GREEN}Step 3: Adding Coral repository...${NC}"
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

# Add Google package signing key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update package list again
echo -e "${GREEN}Step 4: Updating package list with Coral repository...${NC}"
sudo apt-get update

# Install Edge TPU runtime
echo -e "${GREEN}Step 5: Installing Edge TPU runtime...${NC}"
echo -e "${YELLOW}Choose runtime performance mode:${NC}"
echo "  1) Standard (recommended) - Lower performance, runs cooler"
echo "  2) Maximum - Higher performance, may run hot"
echo ""
read -p "Enter choice [1-2] (default: 1): " runtime_choice
runtime_choice=${runtime_choice:-1}

if [[ $runtime_choice == "2" ]]; then
    echo -e "${YELLOW}Installing maximum performance runtime...${NC}"
    sudo apt-get install -y libedgetpu1-max
else
    echo -e "${YELLOW}Installing standard performance runtime...${NC}"
    sudo apt-get install -y libedgetpu1-std
fi

# Install Python3 and pip if not already installed
echo -e "${GREEN}Step 6: Checking Python3 installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Installing Python3...${NC}"
    sudo apt-get install -y python3 python3-pip
else
    echo -e "${GREEN}Python3 is already installed${NC}"
    python3 --version
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing pip3...${NC}"
    sudo apt-get install -y python3-pip
fi

# Install PyCoral library
echo -e "${GREEN}Step 7: Installing PyCoral library...${NC}"
pip3 install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0

# Install TensorFlow Lite runtime
echo -e "${GREEN}Step 8: Installing TensorFlow Lite runtime...${NC}"
pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime

# Check if device is connected
echo ""
echo -e "${GREEN}Step 9: Checking for Coral USB Accelerator...${NC}"
if lsusb | grep -q "Global Unichip Corp"; then
    echo -e "${GREEN}✓ Coral USB Accelerator detected!${NC}"
    lsusb | grep "Global Unichip Corp"
else
    echo -e "${YELLOW}⚠ Coral USB Accelerator not detected${NC}"
    echo "Please make sure the device is properly connected to a USB port."
    echo "The device should appear as 'Global Unichip Corp' in lsusb output."
fi

# Add user to plugdev group (may be needed for permissions)
echo ""
echo -e "${GREEN}Step 10: Setting up device permissions...${NC}"
if ! groups $USER | grep -q "plugdev"; then
    echo -e "${YELLOW}Adding $USER to plugdev group...${NC}"
    sudo usermod -a -G plugdev $USER
    echo -e "${YELLOW}You may need to log out and log back in for group changes to take effect.${NC}"
else
    echo -e "${GREEN}User already in plugdev group${NC}"
fi

# Setup complete
echo ""
echo -e "${GREEN}=== Setup Complete! ===${NC}"
echo ""
echo "Next steps:"
echo "1. If you were added to the plugdev group, log out and log back in"
echo "2. Connect your Coral USB Accelerator if not already connected"
echo "3. Run 'python3 test_coral.py' to verify the installation"
echo "4. Check examples at: https://github.com/google-coral/pycoral/tree/master/examples"
echo ""
echo -e "${GREEN}Happy coding with Coral!${NC}"
