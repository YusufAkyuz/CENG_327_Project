import cv2
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from steganography import Steganography

import os
import platform

# MacOS version compatibility adjustments
if platform.system() == "Darwin":
    os.environ["TK_SILENCE_DEPRECATION"] = "1"
    os.environ["NO_AT_BRIDGE"] = "1"

class SteganographyApp:
    """
    A GUI-based application for encoding and decoding hidden text within images using steganography.

    Attributes:
        root (Tk): The root Tkinter window.
        steganography (Steganography): An instance of the Steganography class for encoding and decoding text.
        cover_image_path (str): Path to the selected cover image for encoding.
        stego_image_path (str): Path to the stego image for decoding.
        cover_image_label (Label): Label to display the selected cover image path.
        stego_image_label (Label): Label to display the selected stego image path.
        text_input (Entry): Input field for entering the text to encode.
        result_label (Label): Label to display the decoded text or status messages.
    """

    def __init__(self, root):
        """
        Initializes the SteganographyApp with Tkinter widgets and attributes.

        Args:
            root (Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Steganography Tool")
        self.steganography = Steganography()

        self.cover_image_path = None
        self.stego_image_path = None

        # Title
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
        """
        Opens a file dialog to select a cover image for encoding text.
        Updates the label with the selected file path.
        """
        try:
            self.cover_image_path = filedialog.askopenfilename(
                title="Select Cover Image",
                initialdir="/",
                filetypes=[("PNG Files", ".png"), ("JPEG Files", ".jpg"), ("JPEG Files", "*.jpeg"),
                           ("All Files", ".*")]
            )
            if not self.cover_image_path:
                self.cover_image_label.config(text="No cover image selected")
                return
            self.cover_image_label.config(text=self.cover_image_path)
        except Exception as e:
            print(f"Error during file selection: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def select_stego_image(self):
        """
        Opens a file dialog to select a stego image for decoding text.
        Updates the label with the selected file path.
        """
        self.stego_image_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"),
                       ("All Files", "*.*")]
        )
        if not self.stego_image_path:
            self.stego_image_label.config(text="No stego image selected")
        else:
            self.stego_image_label.config(text=self.stego_image_path)

    def encode_text(self):
        """
        Encodes text into the selected cover image and saves the resulting stego image.

        Prompts the user to select a save location for the stego image.
        Displays error messages if prerequisites are not met or an error occurs.
        """
        if not self.cover_image_path or not self.text_input.get():
            messagebox.showerror("Error", "Please select a cover image and enter text to encode.")
            return

        cover_image = cv2.imread(self.cover_image_path)
        if cover_image is None:
            messagebox.showerror("Error", "Failed to load cover image.")
            return

        text = self.text_input.get()
        stego_image = self.steganography.encode_text(cover_image, text)

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if not save_path:
            messagebox.showerror("Error", "No file path specified.")
            return

        cv2.imwrite(save_path, stego_image)
        messagebox.showinfo("Success", f"Stego image saved to {save_path}")

    def decode_text(self):
        """
        Decodes hidden text from the selected stego image using the original cover image.

        Displays the decoded text in the result label or an error message if decoding fails.
        """
        if not self.cover_image_path or not self.stego_image_path:
            messagebox.showerror("Error", "Please select both a cover image and a stego image.")
            return

        cover_image = cv2.imread(self.cover_image_path)
        stego_image = cv2.imread(self.stego_image_path)

        if cover_image is None or stego_image is None:
            messagebox.showerror("Error", "Failed to load images.")
            return

        if cover_image.shape != stego_image.shape:
            messagebox.showerror("Error", "Image dimensions do not match.")
            return

        hidden_text = self.steganography.decode_text(cover_image, stego_image)
        self.result_label.config(text=f"Decoded Text: {hidden_text}")


if __name__ == "__main__":
    # Initialize the Tkinter application
    root = Tk()
    app = SteganographyApp(root)
    root.mainloop()