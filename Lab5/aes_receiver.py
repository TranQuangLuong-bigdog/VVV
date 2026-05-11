import socket
import struct
import threading
import tkinter as tk
from tkinter import scrolledtext
from aes_utils import decrypt_aes_cbc, recv_exact

KEY_PORT = 5001
DATA_PORT = 5000

class ReceiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Receiver - Server")
        self.root.geometry("600x500")
        self.root.configure(bg="#34495e")

        tk.Label(root, text="NHẬT KÝ HỆ THỐNG NHẬN", font=("Arial", 14, "bold"), bg="#34495e", fg="white").pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(root, width=70, height=22, font=("Consolas", 10), bg="#1e272e", fg="#d2dae2")
        self.log_area.pack(pady=10, padx=10)

        # Khởi tạo luồng lắng nghe Socket
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def write_log(self, text):
        self.log_area.insert(tk.END, f"{text}\n")
        self.log_area.see(tk.END)

    def listen_loop(self):
        while True:
            try:
                # 1. Chờ nhận Khóa/IV trên cổng 5001
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_key:
                    s_key.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s_key.bind(('0.0.0.0', KEY_PORT))
                    s_key.listen(1)
                    self.write_log(f"[*] Đang đợi Khóa/IV trên cổng {KEY_PORT}...")
                    conn, addr = s_key.accept()
                    with conn:
                        key = recv_exact(conn, 32)
                        iv = recv_exact(conn, 16)
                        self.write_log(f"[+] Đã nhận Khóa từ địa chỉ: {addr[0]}")

                # 2. Chờ nhận Bản mã trên cổng 5000
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_data:
                    s_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s_data.bind(('0.0.0.0', DATA_PORT))
                    s_data.listen(1)
                    self.write_log(f"[*] Đang đợi Bản mã trên cổng {DATA_PORT}...")
                    conn, addr = s_data.accept()
                    with conn:
                        header = recv_exact(conn, 4)
                        length = struct.unpack('!I', header)[0]
                        ciphertext = recv_exact(conn, length)
                        
                        # 3. Giải mã dữ liệu
                        plain = decrypt_aes_cbc(key, iv, ciphertext)
                        self.write_log("-" * 50)
                        self.write_log(f"[BẢN RÕ NHẬN ĐƯỢC]: {plain}")
                        self.write_log("-" * 50 + "\n")
            except Exception as e:
                self.write_log(f"[!] Lỗi: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverApp(root)
    root.mainloop()