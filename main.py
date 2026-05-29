import customtkinter as ctk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image
import json
import random
import string
import os
from flask import Flask, redirect
from threading import Thread
import waitress
# -------------------------
# Flask Server
# -------------------------

server = Flask(__name__)

# -------------------------
# Redirect
# -------------------------

@server.route("/<code>")

def redirect_link(code):

    try:

        with open("links.json", "r") as f:

            links = json.load(f)

        if code in links:

            return redirect(
                links[code]
            )

        return "Link not found"

    except:

        return "Server Error"

# -------------------------
# Start Server
# -------------------------

def run_server():

    waitress.serve(
        server,
        host="0.0.0.0",
        port=5000
    )

# -------------------------
# Background Thread
# -------------------------

server_thread = Thread(
    target=run_server,
    daemon=True
)

server_thread.start()
# -------------------------
# Theme
# -------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------------
# App
# -------------------------

app = ctk.CTk()

app.title("QR Generator Pro")
app.geometry("900x700")

# -------------------------
# Variables
# -------------------------

qr_image = None
current_qr_path = None

# -------------------------
# Generate Function
# -------------------------

def generate():

    global qr_image
    global current_qr_path

    long_url = textbox.get("1.0", "end").strip()

    if not long_url:

        messagebox.showwarning(
            "Warning",
            "Please enter URL"
        )

        return

    try:

        # -------------------------
        # Create Short Code
        # -------------------------

        code = ''.join(

            random.choices(

                string.ascii_letters + string.digits,

                k=6

            )

        )

        # -------------------------
        # Load Database
        # -------------------------

        with open("links.json", "r") as f:

            links = json.load(f)

        # -------------------------
        # Save Link
        # -------------------------

        links[code] = long_url

        with open("links.json", "w") as f:

            json.dump(
                links,
                f,
                indent=4
            )

        # -------------------------
        # Short URL
        # -------------------------

        short_url = f"https://qr-generator-aegv.onrender.com/{code}"

        short_link_var.set(short_url)

        # -------------------------
        # QR Generate
        # -------------------------

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(short_url)

        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        # -------------------------
        # Folder
        # -------------------------

        if not os.path.exists("qr_codes"):

            os.makedirs("qr_codes")

        # -------------------------
        # File Name
        # -------------------------

        filename = code + ".png"

        path = os.path.join(
            "qr_codes",
            filename
        )

        img.save(path)

        current_qr_path = path

        # -------------------------
        # Preview
        # -------------------------

        preview = Image.open(path)

        qr_image = ctk.CTkImage(
            light_image=preview,
            dark_image=preview,
            size=(250,250)
        )

        qr_label.configure(
            image=qr_image,
            text=""
        )

        status_label.configure(
            text="Generate Success ✅"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def save_qr():

    global current_qr_path

    if not current_qr_path:

        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG File","*.png")]
    )

    if file_path:

        img = Image.open(current_qr_path)

        img.save(file_path)

        messagebox.showinfo(
            "Saved",
            "QR Saved Successfully"
        )

# -------------------------
# UI
# -------------------------

title = ctk.CTkLabel(
    app,
    text="QR Generator Pro",
    font=("Arial",32,"bold")
)

title.pack(pady=20)

textbox = ctk.CTkTextbox(
    app,
    width=700,
    height=120,
    font=("Arial",16)
)

textbox.pack(pady=10)

generate_btn = ctk.CTkButton(
    app,
    text="Generate Short Link + QR",
    command=generate,
    width=300,
    height=50,
    font=("Arial",18,"bold")
)

generate_btn.pack(pady=20)

short_link_var = ctk.StringVar()

short_entry = ctk.CTkEntry(
    app,
    textvariable=short_link_var,
    width=700,
    height=45,
    font=("Arial",16)
)

short_entry.pack(pady=10)

qr_label = ctk.CTkLabel(
    app,
    text=""
)

qr_label.pack(pady=20)

save_btn = ctk.CTkButton(
    app,
    text="Save QR",
    command=save_qr,
    width=200,
    height=45,
    font=("Arial",16,"bold")
)

save_btn.pack(pady=10)

status_label = ctk.CTkLabel(
    app,
    text="Ready",
    font=("Arial",14)
)

status_label.pack(pady=10)

# -------------------------
# Run
# -------------------------

app.mainloop()