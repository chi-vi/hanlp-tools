# HƯỚNG DẪN SỬ DỤNG CÔNG CỤ PHÂN TÍCH NGỮ PHÁP.

Công cụ này viết bằng Python nên khoai hơn các công cụ mỳ ăn liền khác, các bạn phải cài đủ thứ nó mới chạy được.

## Cài đặt ban đầu

### Bước 1: Cài đặt Python 3.10.

Các bạn phải cài đúng phiên bản 3.10, mới hơn 3.11 nó không chạy.
Download file cài đặt tại đây: https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

Lưu ý là khi cài bấm vào phần `Customize installation` để cài `pip`.

### Bước 2: Tải xuống công cụ

Sau khi cài xong python, hãy download dữ liệu của công cụ này từ đường dẫn:
https://github.com/chi-vi/hanlp-tools/archive/refs/heads/main.zip

Sau khi tải xuống được file zip, hãy giải nén nó ra một thư mục nào đó, vào thư mục đó rồi mở Terminal.

Gõ vào dòng `python -m pip install -r requirements.txt` để cài đặt thư viện cho chương trình.

### Bước 3: Chạy công cụ phân tích dữ liệu

Sau khi làm xong các bước trên, bấm đúp vào tệp `hanlp-cli.py` để chạy chương trình.
Tệp kết quả sẽ được lưu trong thư mục con `output` của thư mục vừa được giải nén.

Lưu ý: Lần đầu tiên chạy chương trình có thể sẽ lâu chút vì thư viện nó phải tải dữ liệu model. Các bạn thỉnh kiên nhẫn.
