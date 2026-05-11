import os
import customtkinter as ctk
from tkinter import filedialog
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# ==========================================
# THEME
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# WINDOW
# ==========================================
app = ctk.CTk()

app.geometry("1000x700")
app.title("🚀 Ultimate RSA Security App")

selected_file = ""

# ==========================================
# MAIN FRAME
# ==========================================
frame = ctk.CTkFrame(
    app,
    corner_radius=25
)

frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# ==========================================
# TITLE
# ==========================================
title = ctk.CTkLabel(
    frame,
    text="🔐 CYBER RSA SECURITY SYSTEM",
    font=("Arial Black", 32),
    text_color="#00FFFF"
)

title.pack(pady=20)

subtitle = ctk.CTkLabel(
    frame,
    text="AES + RSA + Digital Signature",
    font=("Arial", 20),
    text_color="lightgray"
)

subtitle.pack()

# ==========================================
# CHOOSE FILE
# ==========================================

def choose_file():

    global selected_file

    selected_file = filedialog.askopenfilename()

    file_label.configure(
        text=f"📂 {selected_file}"
    )

# ==========================================
# GENERATE RSA KEYS
# ==========================================
def generate_keys():

    sender_key = RSA.generate(2048)

    with open("sender_private.pem", "wb") as f:
        f.write(sender_key.export_key())

    with open("sender_public.pem", "wb") as f:
        f.write(sender_key.publickey().export_key())

    receiver_key = RSA.generate(2048)

    with open("receiver_private.pem", "wb") as f:
        f.write(receiver_key.export_key())

    with open("receiver_public.pem", "wb") as f:
        f.write(receiver_key.publickey().export_key())

    status.configure(
        text="✅ RSA Keys Generated",
        text_color="#00FF99"
    )
    add_log("✅ RSA Keys Generated")
    add_log("🔑 sender_private.pem")
    add_log("🔑 sender_public.pem")
    add_log("🔑 receiver_private.pem")
    add_log("🔑 receiver_public.pem")

# ==========================================
# ENCRYPT FILE
# ==========================================
def encrypt_file():

    add_log("🔒 Encrypting file...")
    add_log(f"📂 File: {selected_file}")
    add_log("✅ encrypted.bin created")
    try:

        # Read file
        with open(selected_file, "rb") as f:
            data = f.read()

        # Generate AES key
        aes_key = get_random_bytes(32)

        # AES cipher
        cipher_aes = AES.new(
            aes_key,
            AES.MODE_EAX
        )

        ciphertext, tag = cipher_aes.encrypt_and_digest(data)

        # Encrypt AES key using RSA
        with open("receiver_public.pem", "rb") as f:
            public_key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(public_key)

        encrypted_key = cipher_rsa.encrypt(aes_key)

        # Save encrypted file
        with open("encrypted.bin", "wb") as f:

            f.write(encrypted_key)
            f.write(cipher_aes.nonce)
            f.write(tag)
            f.write(ciphertext)

        progress.set(1)

        status.configure(
            text="🔒 File Encrypted Successfully",
            text_color="#00FFFF"
        )

    except Exception as e:

        status.configure(
            text=f"❌ {e}",
            text_color="red"
        )

# ==========================================
# DECRYPT FILE
# ==========================================
def decrypt_file():
    add_log("🔓 Decrypting...")
    add_log("✅ decrypted_file created")
    try:

        with open("encrypted.bin", "rb") as f:

            encrypted_key = f.read(256)
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        # Load private key
        with open("receiver_private.pem", "rb") as f:
            private_key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(private_key)

        aes_key = cipher_rsa.decrypt(encrypted_key)

        cipher_aes = AES.new(
            aes_key,
            AES.MODE_EAX,
            nonce=nonce
        )

        decrypted = cipher_aes.decrypt_and_verify(
            ciphertext,
            tag
        )

        with open("decrypted_file", "wb") as f:
            f.write(decrypted)

        progress.set(1)

        status.configure(
            text="🔓 File Decrypted",
            text_color="#00FF99"
        )

    except Exception as e:

        status.configure(
            text=f"❌ {e}",
            text_color="red"
        )

# ==========================================
# SIGN FILE
# ==========================================
def sign_file():
    add_log("✍️ Signing file...")
    add_log("✅ signature.bin created")
    try:

        with open(selected_file, "rb") as f:
            data = f.read()

        with open("sender_private.pem", "rb") as f:
            private_key = RSA.import_key(f.read())

        h = SHA256.new(data)

        signature = pkcs1_15.new(private_key).sign(h)

        with open("signature.bin", "wb") as f:
            f.write(signature)

        status.configure(
            text="✍️ File Signed",
            text_color="#FFD700"
        )

    except Exception as e:

        status.configure(
            text=f"❌ {e}",
            text_color="red"
        )

# ==========================================
# VERIFY SIGNATURE
# ==========================================
def verify_signature():
    add_log("🔍 Verifying signature...")
    add_log("✅ VALID SIGNATURE")
    add_log("❌ INVALID SIGNATURE")
    try:

        with open(selected_file, "rb") as f:
            data = f.read()

        with open("signature.bin", "rb") as f:
            signature = f.read()

        with open("sender_public.pem", "rb") as f:
            public_key = RSA.import_key(f.read())

        h = SHA256.new(data)

        pkcs1_15.new(public_key).verify(h, signature)

        status.configure(
            text="✅ VALID SIGNATURE",
            text_color="#00FF99"
        )

    except Exception:

        status.configure(
            text="❌ INVALID SIGNATURE",
            text_color="red"
        )

def add_log(text):

    result_box.insert(
        "end",
        text + "\\n"
    )

    result_box.see("end")
def send_file():

    try:

        host = "127.0.0.1"
        port = 9999

        client = socket.socket()

        client.connect((host, port))

        # gửi encrypted file
        with open("encrypted.bin", "rb") as f:
            data = f.read()

        client.sendall(data)

        client.close()

        add_log("📤 File sent successfully!")

        status.configure(
            text="📤 File Sent",
            text_color="#00FFFF"
        )

    except Exception as e:

        add_log(f"❌ {e}")

        status.configure(
            text="❌ Send Failed",
            text_color="red"
        )
def receive_file():

    try:

        host = "0.0.0.0"
        port = 9999

        server = socket.socket()

        server.bind((host, port))

        server.listen(1)

        add_log("📡 Waiting for connection...")

        conn, addr = server.accept()

        add_log(f"✅ Connected: {addr}")

        data = b""

        while True:

            packet = conn.recv(4096)

            if not packet:
                break

            data += packet

        with open("received_encrypted.bin", "wb") as f:
            f.write(data)

        conn.close()

        add_log("📥 File received!")

        status.configure(
            text="📥 File Received",
            text_color="#00FF99"
        )

    except Exception as e:

        add_log(f"❌ {e}")  
# ==========================================
# BUTTON STYLE
# ==========================================
btn_style = {
    "width": 350,
    "height": 55,
    "corner_radius": 20,
    "font": ("Arial", 18, "bold")
}

# ==========================================
# BUTTONS
# ==========================================
btn_choose = ctk.CTkButton(
    frame,
    text="📂 Choose File",
    command=choose_file,
    fg_color="#6A0DAD",
    hover_color="#9B30FF",
    **btn_style
)

btn_choose.pack(pady=12)

file_label = ctk.CTkLabel(
    frame,
    text="No file selected",
    font=("Arial", 15)
)

file_label.pack()

btn_keys = ctk.CTkButton(
    frame,
    text="🔑 Generate RSA Keys",
    command=generate_keys,
    fg_color="#0055FF",
    hover_color="#0088FF",
    **btn_style
)

btn_keys.pack(pady=12)

btn_encrypt = ctk.CTkButton(
    frame,
    text="🔒 Encrypt File",
    command=encrypt_file,
    fg_color="#009966",
    hover_color="#00CC88",
    **btn_style
)

btn_encrypt.pack(pady=12)

btn_decrypt = ctk.CTkButton(
    frame,
    text="🔓 Decrypt File",
    command=decrypt_file,
    fg_color="#FF8800",
    hover_color="#FFAA00",
    **btn_style
)

btn_decrypt.pack(pady=12)

btn_sign = ctk.CTkButton(
    frame,
    text="✍️ Sign File",
    command=sign_file,
    fg_color="#CC00FF",
    hover_color="#FF00FF",
    **btn_style
)

btn_sign.pack(pady=12)

btn_verify = ctk.CTkButton(
    frame,
    text="✅ Verify Signature",
    command=verify_signature,
    fg_color="#FF0055",
    hover_color="#FF3377",
    **btn_style
)

btn_verify.pack(pady=12)

# ==========================================
# PROGRESS BAR
# ==========================================
progress = ctk.CTkProgressBar(
    frame,
    width=400
)

progress.pack(pady=20)

progress.set(0)

# ==========================================
# STATUS
# ==========================================
status = ctk.CTkLabel(
    frame,
    text="🟢 SYSTEM READY",
    font=("Arial", 20, "bold"),
    text_color="#00FF99"
)

status.pack(pady=20)

# ==========================================
# MAIN LAYOUT
# ==========================================
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# LEFT PANEL
left_panel = ctk.CTkFrame(
    main_frame,
    width=400,
    corner_radius=20
)

left_panel.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

# RIGHT PANEL
right_panel = ctk.CTkFrame(
    main_frame,
    corner_radius=20
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

btn_send = ctk.CTkButton(
    left_panel,
    text="📤 Send File",
    command=send_file,
    fg_color="#00AAFF",
    hover_color="#00DDFF",
    **btn_style
)

btn_send.pack(pady=10)

btn_receive = ctk.CTkButton(
    left_panel,
    text="📥 Receive File",
    command=receive_file,
    fg_color="#00CC66",
    hover_color="#00FF99",
    **btn_style
)

btn_receive.pack(pady=10)
# ==========================================
# RESULT TITLE
# ==========================================
result_title = ctk.CTkLabel(
    right_panel,
    text="📊 SYSTEM LOG",
    font=("Arial Black", 24),
    text_color="#00FFFF"
)

result_title.pack(pady=20)

# ==========================================
# TEXTBOX
# ==========================================
result_box = ctk.CTkTextbox(
    right_panel,
    width=500,
    height=500,
    font=("Consolas", 15),
    corner_radius=15,
    text_color="#00FF99"
)

result_box.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)
# ==========================================
# RUN
# ==========================================
app.mainloop()