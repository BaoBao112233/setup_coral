# Hướng dẫn cài đặt Edge TPU (Coral) Runtime trên Linux — Chi tiết

Tài liệu này hướng dẫn chi tiết cách cài đặt Edge TPU runtime (thư viện `libedgetpu`) trên hệ Debian/Ubuntu, cách cài `pycoral`, cách cấu hình quyền (udev), xử lý sự cố phổ biến, và cách kiểm tra/kiểm thử. Các lệnh đều đã được kiểm tra và phù hợp cho Ubuntu 20.04/22.04 (và các bản tương đương).

**Lưu ý quan trọng**: một số bước yêu cầu quyền `sudo`. Đọc hết phần xử lý sự cố trước khi thực hiện thao tác nâng cấp firmware (DFU) — flash firmware sai có thể làm hỏng thiết bị.
- Hệ điều hành: Debian/Ubuntu phổ biến (20.04/22.04). Các bản khác có thể cần điều chỉnh một số lệnh.
- Quyền `sudo` để thêm APT repository, cài gói và reload udev rules.
- Kết nối internet để tải repo và gói.

## 1. Yêu cầu trước khi cài
## 2. Mô tả ngắn rút gọn
1. Thêm Coral APT repository an toàn (sử dụng `signed-by` keyring).
2. Cài Edge TPU runtime (`libedgetpu1-std` hoặc `libedgetpu1-max`).
3. Cài `pycoral` cho Python (APT package hoặc `pip` trong virtualenv).

## 3. Thêm APT repo (khuyến nghị: keyring + signed-by)
Chúng ta không dùng `apt-key` (đã deprecated). Thay vào đó lưu GPG key vào `/usr/share/keyrings` và tham chiếu bằng `signed-by`.
```bash

```bash
Ghi chú:
 - Nếu bạn đã thêm key bằng `apt-key` trước đó, việc thêm keyring mới không gây hại; apt sẽ dùng `signed-by` khi source list yêu cầu.

 - Nếu hệ của bạn bật `i386` multiarch, apt có thể cảnh báo "doesn't support architecture 'i386'" cho một số repo — đây chỉ là cảnh báo. Để loại bỏ, gõ `sudo dpkg --remove-architecture i386` nếu bạn không cần 32-bit support.

## 4. Cài Edge TPU runtime và Python support

Bạn có hai lựa chọn chính cho runtime: `libedgetpu1-std` (thông dụng) hoặc `libedgetpu1-max` (hiệu năng cao khi phần cứng hỗ trợ). Phần lớn trường hợp `libedgetpu1-std` là đủ.
```bash
sudo apt update
sudo apt install -y libedgetpu1-std python3-pip python3-venv

```bash
sudo apt install -y python3-pycoral || true
Nếu `python3-pycoral` không có trong APT (tùy distro), cài bằng `pip` trong virtualenv:
```bash

python3 -m venv coral-venv
```
source coral-venv/bin/activate
pip install --upgrade pip
pip install pycoral
```
## 5. Cấu hình udev rule (truy cập device không cần sudo)
Khi thiết bị đã được kernel nhận, để truy cập Edge TPU không cần `sudo` ta thêm udev rule. Tạo file `/etc/udev/rules.d/99-edgetpu-accelerator.rules` với nội dung ví dụ sau (sửa `idProduct` nếu thiết bị của bạn khác khi ở chế độ hoạt động):
```
SUBSYSTEM=="usb", ATTR{idVendor}=="1a6e", ATTR{idProduct}=="089a", MODE="0664", GROUP="plugdev"
```
Sau đó reload rules:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```
Ghi chú: `MODE="0664"` và `GROUP="plugdev"` cho phép thành viên nhóm `plugdev` truy cập. Thêm user vào nhóm `plugdev` nếu cần:
```bash
sudo usermod -aG plugdev $USER
newgrp plugdev
```
## 6. Kiểm tra (verification)
1. Kiểm tra gói đã cài:
```bash
apt-cache policy libedgetpu1-std libedgetpu1-max
dpkg -l | grep libedgetpu
```
2. Kiểm tra library đã được đăng ký với ldconfig:
```bash
ldconfig -p | grep edgetpu
```
3. Chạy script kiểm tra trong repo:
```bash
python3 scripts/test_coral_runtime.py
```
Kết quả mong đợi: script báo `EdgeTPU runtime found` và `pycoral import succeeded`.
4. Kiểm tra thiết bị USB (nếu có accelerator gắn):
```bash
lsusb
sudo dmesg | tail -n 50
```
Look for vendor/product như `1a6e:089a` (vendor `Global Unichip Corp.`) — note: vendor/product có thể khác tùy thiết bị/firmware.
## 7. Xử lý sự cố thường gặp
- Lỗi: `libedgetpu.so.1: cannot open shared object file`: kiểm tra `libedgetpu1-std` đã cài chưa, và chạy `ldconfig`:
```bash
sudo ldconfig
ldconfig -p | grep edgetpu
```
- Cảnh báo apt về `apt-key` deprecation: sửa bằng cách dùng `gpg --dearmour` và `signed-by` (đã trình bày ở phần 3).
- Cảnh báo repository "doesn't support architecture 'i386'": xảy ra nếu hệ có `i386` là foreign architecture; gỡ nó nếu không cần:
```bash
sudo dpkg --remove-architecture i386
sudo apt update
```
- Thiết bị xuất hiện ở chế độ DFU (ví dụ `1a6e:089a` hiển thị như DFU): nghĩa là thiết bị đang ở chế độ firmware-update. Kiểm tra bằng `dfu-util`:
```bash
sudo apt install -y dfu-util
sudo dfu-util --list
```
Nếu thiết bị ở DFU và bạn không có firmware chính xác, **không flash**; thử rút cáp, đổi cổng/cáp, hoặc reboot hệ để thiết bị quay về chế độ hoạt động bình thường.
Nếu bạn hiểu rõ và có firmware chính thức từ nhà sản xuất, có thể flash bằng `dfu-util -d <vendor:product> -D firmware.bin` (rất rủi ro nếu firmware sai).
## 8. Ví dụ inference nhanh (tùy chọn)
Sau khi runtime và `pycoral` đã hoạt động, bạn có thể chạy một ví dụ inference để kiểm tra throughput. Đây là ví dụ tối thiểu dùng `pycoral`:
```python
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common
from pycoral.adapters import classify

model_path = 'mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite'  # thay bằng model EdgeTPU-compiled
interpreter = make_interpreter(model_path)
interpreter.allocate_tensors()
print('Interpreter ready on EdgeTPU')

# load input image and run inference (chi tiết phụ thuộc model)
```
Lưu ý: để tận dụng Edge TPU, model phải được biên dịch (compiled) cho Edge TPU (từ `edgetpu_compiler`) hoặc tải model đã có sẵn cho Coral.
## 9. Tài liệu & tham khảo
- Coral docs (runtime on Linux): <https://coral.ai/docs/accelerator/get-started/#runtime-on-linux>
- pycoral API và ví dụ: <https://coral.ai/docs/accelerator/get-started/#python>
## 10. Tổng kết nhanh
- Chạy `sudo bash scripts/install_coral_runtime.sh` để tự động hóa bước repo + install (script trong repo đã sử dụng keyring/signed-by).
- Tạo virtualenv và `pip install pycoral` nếu bạn ưu tiên môi trường ảo.
- Thêm udev rule để truy cập device không cần sudo.
- Kiểm tra bằng `python3 scripts/test_coral_runtime.py`.

Nếu bạn muốn, tôi sẽ:
- thêm file udev mẫu vào repo và cập nhật `README.md`, hoặc
- thêm script ví dụ inference hoàn chỉnh với model mẫu và hướng dẫn download.


````
```

Ghi chú về cảnh báo bạn có thể thấy:
- "Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg)": xảy ra khi key được thêm bằng `apt-key`. Sử dụng `gpg --dearmour` và `signed-by` như trên sẽ tránh cảnh báo.
- "doesn't support architecture 'i386'": xuất hiện nếu hệ của bạn có `i386` là một foreign architecture (multiarch) nhưng repo Coral chỉ xuất bản cho kiến trúc chính (ví dụ `amd64`). Để tắt cảnh báo đó có thể:
	- Giới hạn repo bằng tham số `arch=` (như lệnh trên).
	- Nếu bạn không cần i386, gỡ bỏ kiến trúc i386: `sudo dpkg --remove-architecture i386` (cẩn trọng: chỉ làm nếu bạn chắc chắn).

2. Cài runtime và gói Python (APT):

```bash
sudo apt install -y libedgetpu1-std python3-pip python3-venv
# Nếu bạn muốn dùng gói Python hệ thống:
sudo apt install -y python3-pycoral
```

3. (Tùy chọn) Cài `pycoral` trong virtualenv bằng pip:

```bash
python3 -m venv coral-venv
source coral-venv/bin/activate
pip install --upgrade pip
pip install pycoral
```

4. Kiểm tra nhanh:

```bash
python3 scripts/test_coral_runtime.py
```

Nếu mọi thứ OK, script sẽ báo `EdgeTPU runtime found` và `pycoral` (nếu có) cũng sẽ load được.

Phần xử lý sự cố nhanh:
- Nếu `libedgetpu.so.1` không tìm thấy: kiểm tra `apt` có cài `libedgetpu1-std` hay chưa.
- Kiểm tra quyền truy cập USB: đảm bảo device Coral được kết nối, người dùng có thể cần quyền truy cập (uDev rules). Nếu gặp lỗi quyền, thử `sudo` hoặc thêm udev rule theo tài liệu Coral.
- Nếu dùng `pip` và gặp lỗi import `pycoral`: thử cài `python3-pycoral` bằng apt hoặc cài đúng wheel/tflite runtime phù hợp với kiến trúc.

Tham khảo chính thức:
- Coral documentation: https://coral.ai/docs/accelerator/get-started/#runtime-on-linux

Hãy chạy `scripts/install_coral_runtime.sh` để tự động hóa các bước hoặc thực hiện từng lệnh theo ý bạn. Lưu ý script đã dùng phương thức keyring/signed-by để tránh cảnh báo `apt-key`.

