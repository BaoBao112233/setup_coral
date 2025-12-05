# Hướng dẫn cài đặt Edge TPU (Coral) Runtime trên Linux

Tài liệu này hướng dẫn cách cài đặt Edge TPU runtime (thư viện `libedgetpu`) và cách kiểm tra nhanh trên hệ điều hành Debian/Ubuntu. Nội dung viết bằng tiếng Việt, tóm tắt các bước chính và gồm script trợ giúp để chạy tự động.

Yêu cầu trước khi cài:
- Hệ điều hành: Debian/Ubuntu (20.04, 22.04 hoặc tương đương). Một số bản Debian khác có thể hoạt động nhưng các gói APT có thể khác.
- Quyền `sudo` để thêm repository và cài gói hệ thống.
- Kết nối internet.

Tổng quan các bước:
1. Thêm repository Coral (Google Cloud APT repo) và import GPG key.
2. Cài Edge TPU runtime (`libedgetpu1-std` hoặc `libedgetpu1-max` nếu bạn cần hiệu năng tối đa và phần cứng phù hợp).
3. Cài gói Python hỗ trợ (`python3-pycoral`) hoặc cài `pycoral` bằng `pip` trong virtualenv.
4. Kiểm tra bằng script Python mẫu để xác nhận `libedgetpu` và `pycoral` có hoạt động.

Lưu ý về lựa chọn `libedgetpu`:
- `libedgetpu1-std`: phiên bản standard (thường được dùng và tương thích với USB Accelerator).
- `libedgetpu1-max`: phiên bản tối ưu hóa cho hiệu năng (chỉ khi phần cứng và driver hỗ trợ).

Script kèm theo:
- `scripts/install_coral_runtime.sh` — script cài đặt tự động (chạy dưới `sudo`).
- `scripts/test_coral_runtime.py` — script kiểm tra nhanh (chạy bằng `python3`).

Hướng dẫn cài đặt (tay) — cách khuyến nghị (không dùng `apt-key` đã bị deprecate):

1. Thêm kho APT và import GPG key vào keyring (khuyến nghị):

```bash
# Lưu key vào keyring (yêu cầu sudo)
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
	| sudo gpg --dearmour -o /usr/share/keyrings/coral-edgetpu-archive-keyring.gpg

# Thêm source list và giới hạn cho kiến trúc chính (vd: amd64)
ARCH=$(dpkg --print-architecture)
echo "deb [signed-by=/usr/share/keyrings/coral-edgetpu-archive-keyring.gpg arch=${ARCH}] https://packages.cloud.google.com/apt coral-edgetpu-stable main" \
	| sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

sudo apt update
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

