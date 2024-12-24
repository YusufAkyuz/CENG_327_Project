import cv2
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from steganography import Steganography

import os
import platform

# MacOS version compatibility
if platform.system() == "Darwin":
    os.environ["TK_SILENCE_DEPRECATION"] = "1"
    os.environ["NO_AT_BRIDGE"] = "1"

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.steganography = Steganography()

        self.cover_image_path = None
        self.stego_image_path = None

        Label(root, text="Steganography Tool", font=("Helvetica", 16)).pack(pady=10)

        # Cover Image Selection
        Button(root, text="Select Cover Image", command=self.select_cover_image).pack(pady=5)
        self.cover_image_label = Label(root, text="No cover image selected")
        self.cover_image_label.pack()

        # Text Input for Encoding
        Label(root, text="Enter text to encode:").pack()
        self.text_input = Entry(root, width=50)
        self.text_input.pack()

        Button(root, text="Encode Text", command=self.encode_text).pack(pady=10)

        # Stego Image Selection for Decoding
        Button(root, text="Select Stego Image", command=self.select_stego_image).pack(pady=5)
        self.stego_image_label = Label(root, text="No stego image selected")
        self.stego_image_label.pack()

        Button(root, text="Decode Text", command=self.decode_text).pack(pady=10)

        # Output Label
        self.result_label = Label(root, text="", font=("Helvetica", 12), fg="green")
        self.result_label.pack(pady=10)

    def select_cover_image(self):
        try:
            self.cover_image_path = filedialog.askopenfilename(
                title="Select Cover Image",
                initialdir="/",
                filetypes=[("PNG Files", ".png"), ("JPEG Files", ".jpg"), ("JPEG Files", "*.jpeg"),
                           ("All Files", ".")])
            if not self.cover_image_path:
                self.cover_image_label.config(text="No cover image selected")
                return
            self.cover_image_label.config(text=self.cover_image_path)
        except Exception as e:
            print(f"Error during file selection: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def select_stego_image(self):
        self.stego_image_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"),
                       ("All Files", "*.*")])
        if not self.stego_image_path:
            self.stego_image_label.config(text="No stego image selected")
        else:
            self.stego_image_label.config(text=self.stego_image_path)
