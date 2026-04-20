import tkinter as tk
import socket
import threading
from des_socket_utils import HEADER_SIZE, parse_header, recv_exact, decrypt_des_cbc

is_listening = False

def listen_for_messages(port, save_filename):
    global is_listening
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
            s.listen(5)
            update_log(f"[*] Đang chờ dữ liệu tại cổng {port}...\n")
            
            while is_listening:
                conn, addr = s.accept()
                with conn:
                    update_log(f"\n[+] Kết nối từ {addr}")
                    
                    # 1. Nhận và bóc tách gói tin
                    header = recv_exact(conn, HEADER_SIZE)
                    key, iv, length = parse_header(header)
                    cipher_bytes = recv_exact(conn, length)
                    
                    # 2. Giải mã lấy lại dữ liệu gốc
                    original_data = decrypt_des_cbc(key, iv, cipher_bytes)
                    
                    # 3. Ghi dữ liệu ra file
                    with open(save_filename, 'wb') as f:
                        f.write(original_data)
                    update_log(f"[+] Đã giải mã và lưu vào file: {save_filename}\n")

                    # 4. TÍNH NĂNG MỚI: NẾU LÀ FILE TXT THÌ IN RA MÀN HÌNH
                    if save_filename.lower().endswith('.txt'):
                        try:
                            # Cố gắng chuyển dữ liệu nhị phân thành chữ để in ra
                            text_content = original_data.decode('utf-8')
                            update_log(f"--- NỘI DUNG FILE ---\n{text_content}\n---------------------\n")
                        except Exception:
                            update_log("[!] File txt chứa ký tự lạ không thể hiển thị.\n")

    except Exception as e:
        if is_listening:
            update_log(f"[!] Lỗi Server: {str(e)}\n")

def update_log(msg):
    text_log.insert(tk.END, msg)
    text_log.see(tk.END)

def start_server():
    global is_listening
    if not is_listening:
        port_str = entry_port.get()
        save_name = entry_savename.get()
        
        if not port_str.isdigit() or not save_name:
            update_log("[!] Vui lòng nhập cổng và tên file lưu.\n")
            return
        
        is_listening = True
        btn_start.config(state=tk.DISABLED)
        threading.Thread(target=listen_for_messages, args=(int(port_str), save_name), daemon=True).start()

# --- Thiết kế giao diện ---
root = tk.Tk()
root.title("DES File Receiver (Máy 1)")
root.geometry("480x450")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Port:").pack(side=tk.LEFT)
entry_port = tk.Entry(frame_top, width=8)
entry_port.insert(0, "6000")
entry_port.pack(side=tk.LEFT, padx=5)

tk.Label(frame_top, text="Lưu tên là:").pack(side=tk.LEFT)
entry_savename = tk.Entry(frame_top, width=20)
entry_savename.insert(0, "tin_nhan.txt") # Mặc định lưu thành file txt
entry_savename.pack(side=tk.LEFT, padx=5)

btn_start = tk.Button(root, text="Bật Máy Nhận", command=start_server, bg="lightgreen")
btn_start.pack(pady=5)

# Tăng kích thước hộp hiển thị chữ
text_log = tk.Text(root, height=18, width=55)
text_log.pack(pady=5)

root.mainloop()