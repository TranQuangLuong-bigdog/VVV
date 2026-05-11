import hashlib

def hash_data(data):
    # Chuyển dữ liệu sang dạng bytes
    data_bytes = data.encode()

    # SHA-256
    sha256_hash = hashlib.sha256(data_bytes).hexdigest()

    # SHA-512
    sha512_hash = hashlib.sha512(data_bytes).hexdigest()

    return sha256_hash, sha512_hash


# 🔹 Dữ liệu ban đầu
original_data = "Hello World"

# 🔹 Dữ liệu bị sửa (chỉ thêm dấu !)
modified_data = "Hello World!"

# Băm dữ liệu
orig_sha256, orig_sha512 = hash_data(original_data)
mod_sha256, mod_sha512 = hash_data(modified_data)

# In kết quả
print("=== DỮ LIỆU GỐC ===")
print("SHA-256:", orig_sha256)
print("SHA-512:", orig_sha512)

print("\n=== DỮ LIỆU ĐÃ SỬA ===")
print("SHA-256:", mod_sha256)
print("SHA-512:", mod_sha512)

# So sánh
print("\n=== SO SÁNH ===")
print("SHA-256 giống nhau?", orig_sha256 == mod_sha256)
print("SHA-512 giống nhau?", orig_sha512 == mod_sha512)