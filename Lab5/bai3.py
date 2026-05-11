import hashlib
import shutil
import os

# 🔹 Hàm băm file
def hash_file(filepath):
    sha512 = hashlib.sha512()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha512.update(chunk)
    return sha512.hexdigest()


# 🔹 Mô phỏng gửi file
def send_file(source_path, dest_path):
    print("📤 Đang gửi file...")

    # Tính hash trước khi gửi
    file_hash = hash_file(source_path)

    # Copy file (giả lập gửi qua mạng)
    shutil.copy(source_path, dest_path)

    print("✔ File đã gửi")
    print("🔑 Hash gửi kèm:", file_hash)

    return file_hash


# 🔹 Mô phỏng nhận file
def receive_file(received_path, original_hash):
    print("\n📥 Đang nhận file...")

    # Tính hash file nhận
    received_hash = hash_file(received_path)

    print("🔑 Hash nhận được:", received_hash)

    # So sánh
    if received_hash == original_hash:
        print("✅ File toàn vẹn (không bị thay đổi)")
    else:
        print("❌ File đã bị thay đổi hoặc lỗi")


# ===========================
# 🔹 MAIN
# ===========================

source_file = "Heban.webp"
received_file = "Heban1.jpg"

# Gửi file
hash_sent = send_file(source_file, received_file)

# 👉 Thử sửa file ở đây để test (mở ảnh chỉnh 1 chút rồi lưu)

# Nhận file
receive_file(received_file, hash_sent)