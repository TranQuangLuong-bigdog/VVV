import socket
import struct
import tkinter as tk
from tkinter import messagebox
from aes_utils import encrypt_aes_cbc

# Cấu hình cổng theo Lab 6.2
KEY_PORT = 5001
DATA_PORT = 5000
TARGET_IP = "172.16.4.134" #

class SenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Sender - 172.16.4.134")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")

        tk.Label(root, text="GỬI DỮ LIỆU AES (LAB 6.2)", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(pady=15)
        
        tk.Label(root, text="IP Máy Nhận:", bg="#2c3e50", fg="#bdc3c7").pack()
        self.ip_entry = tk.Entry(root, width=30, justify='center', font=("Arial", 10))
        self.ip_entry.insert(0, TARGET_IP)
        self.ip_entry.pack(pady=5)

        tk.Label(root, text="Thông điệp bảo mật:", bg="#2c3e50", fg="#bdc3c7").pack()
        self.msg_text = tk.Text(root, height=6, width=50, font=("Segoe UI", 10))
        self.msg_text.pack(pady=10, padx=20)

        self.send_btn = tk.Button(root, text="MÃ HÓA & GỬI NGAY", command=self.send_data, 
                                  bg="#e67e22", fg="white", font=("Arial", 10, "bold"), padx=30, pady=10)
        self.send_btn.pack(pady=20)
    def send_data(self):
        dest_ip = self.ip_entry.get()
        message = self.msg_text.get("1.0", tk.END).strip()

        if not message:
            messagebox.showwarning("Chú ý", "Hùng ơi, nhập tin nhắn đã nhé!")
            return

        try:
            # 1. Mã hóa
            key, iv, ciphertext = encrypt_aes_cbc(message)

            # 2. Gửi qua Kênh Khóa (Cổng 5001)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_key:
                s_key.connect((dest_ip, KEY_PORT))
                s_key.sendall(key + iv)

            # 3. Gửi qua Kênh Dữ liệu (Cổng 5000) kèm Header độ dài
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_data:
                s_data.connect((dest_ip, DATA_PORT))
                # Header 4 byte - Network Byte Order
                header = struct.pack('!I', len(ciphertext))
                s_data.sendall(header + ciphertext)

            messagebox.showinfo("Thành công", f"Đã gửi tới {dest_ip} qua 2 kênh an toàn!")
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không gửi được: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.mainloop()