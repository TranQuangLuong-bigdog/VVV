import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import os
from des_socket_utils import encrypt_des_cbc, build_packet

def choose_file():
    # Mở cửa sổ chọn file
    filepath = filedialog.askopenfilename()
    if filepath:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filepath)

def send_file():
    ip = entry_ip.get()
    port = entry_port.get()
    filepath = entry_file.get()

    if not ip or not port or not filepath:
        messagebox.showwarning("Warning", "Please fill in all fields and select a file!")
        return

    if not os.path.exists(filepath):
        messagebox.showerror("Error", "File does not exist!")
        return

    try:
        port = int(port)
        
        # 1. Đọc file dưới dạng nhị phân (rb)
        with open(filepath, 'rb') as f:
            plain_bytes = f.read()
        
        # 2. Mã hóa file
        key, iv, cipher_bytes = encrypt_des_cbc(plain_bytes)
        overall = build_packet(key, iv, cipher_bytes)

        # 3. Gửi qua mạng
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(overall)

        filename = os.path.basename(filepath)
        log_text = f"[+] Sent file: {filename}\nSize: {len(plain_bytes)} bytes\nKey: {key.hex()}\n\n"
        text_log.insert(tk.END, log_text)
        text_log.see(tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send: {str(e)}")

# Thiết kế giao diện Máy Gửi
root = tk.Tk()
root.title("DES File Sender (Máy 2)")
root.geometry("450x350")

tk.Label(root, text="Receiver IP:").pack(pady=2)
entry_ip = tk.Entry(root, width=45)
entry_ip.insert(0, "172.20.10.5")
entry_ip.pack()

tk.Label(root, text="Port:").pack(pady=2)
entry_port = tk.Entry(root, width=45)
entry_port.insert(0, "6000")
entry_port.pack()

# Khu vực chọn file
frame_file = tk.Frame(root)
frame_file.pack(pady=10)
entry_file = tk.Entry(frame_file, width=33)
entry_file.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame_file, text="Browse", command=choose_file)
btn_browse.pack(side=tk.LEFT)

tk.Button(root, text="Encrypt & Send File", command=send_file, bg="lightblue").pack(pady=10)

text_log = tk.Text(root, height=8, width=50)
text_log.pack()

root.mainloop()