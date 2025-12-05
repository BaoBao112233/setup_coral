#!/usr/bin/env bash
set -euo pipefail

echo "== Edge TPU (Coral) runtime installer =="

if [ "$EUID" -ne 0 ]; then
  echo "This script requires sudo. Re-run with sudo or as root." >&2
  exit 2
fi

command -v lsb_release >/dev/null 2>&1 || apt update >/dev/null && apt install -y lsb-release >/dev/null || true
CODENAME=$(lsb_release -cs 2>/dev/null || echo "$(. /etc/os-release && echo $UBUNTU_CODENAME || true)")

echo "Detected distro codename: ${CODENAME}"

echo "Adding Coral APT repository and GPG key (using keyring)..."
# Use a keyring file instead of apt-key (apt-key is deprecated)
KEYRING=/usr/share/keyrings/coral-edgetpu-archive-keyring.gpg
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmour -o "$KEYRING"

# Restrict to the primary architecture to avoid warnings when i386 is enabled as a foreign arch
PRIMARY_ARCH=$(dpkg --print-architecture)
echo "deb [signed-by=$KEYRING arch=$PRIMARY_ARCH] https://packages.cloud.google.com/apt coral-edgetpu-stable main" > /etc/apt/sources.list.d/coral-edgetpu.list

echo "Updating apt..."
apt update

echo "Installing Edge TPU runtime and common Python tooling..."
apt install -y libedgetpu1-std python3-pip python3-venv || {
  echo "APT install failed. Check your distro or network." >&2
  exit 1
}

echo "(Optional) Installing system pycoral package (convenient for system Python)..."
apt install -y python3-pycoral || echo "python3-pycoral not available for this distro; you can pip install pycoral in a venv." 

echo "If you previously saw a warning about 'doesn't support architecture i386', it's because your apt is configured with i386 as a foreign architecture but the Coral repo only publishes packages for the main architecture. If you don't need i386 support, you can remove it with:"
echo "  sudo dpkg --remove-architecture i386"

echo "Done."
echo "Next steps (recommended):"
echo "  1) Create and activate a virtualenv:"
echo "       python3 -m venv coral-venv"
echo "       source coral-venv/bin/activate"
echo "  2) Inside venv, upgrade pip and install pycoral if needed:"
echo "       pip install --upgrade pip"
echo "       pip install pycoral"
echo "  3) Run the test script: python3 scripts/test_coral_runtime.py"

exit 0
