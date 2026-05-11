import hashlib

def hash_file(filepath):
    sha512 = hashlib.sha512()

    with open(filepath, "rb") as f:
        while chunk := f.read(4096):  # đọc từng khối
            sha512.update(chunk)

    return sha512.hexdigest()


# 🔹 File gốc
file1 = "Heban.webp"

# 🔹 File đã chỉnh sửa (hoặc copy rồi sửa)
file2 = "Heban1.jpg"

hash1 = hash_file(file1)
hash2 = hash_file(file2)

print("Hash file gốc:", hash1)
print("Hash file sửa:", hash2)

if hash1 == hash2:
    print("✅ File không bị thay đổi (toàn vẹn)")
else:
    print("❌ File đã bị thay đổi")