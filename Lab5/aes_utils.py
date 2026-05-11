import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# AES sử dụng block size 16 byte
BLOCK_SIZE = 16

def encrypt_aes_cbc(plain_text: str):
    # AES-256 yêu cầu khóa 32 byte
    key = os.urandom(32)
    iv = os.urandom(16) # IV 16 byte ngẫu nhiên
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Thêm đệm PKCS#7
    ciphertext = cipher.encrypt(pad(plain_text.encode('utf-8'), BLOCK_SIZE))
    return key, iv, ciphertext

def decrypt_aes_cbc(key: bytes, iv: bytes, ciphertext: bytes):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Gỡ đệm PKCS#7
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE).decode('utf-8')

def recv_exact(conn, n: int):
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet: return None
        data += packet
    return data