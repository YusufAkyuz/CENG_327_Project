import cv2
import numpy as np
import os


class Steganography:
    @staticmethod
    def _int_to_bin(data):
        """
        Converts input string into its binary representation.
        """
        if isinstance(data, str):
            return [format(ord(char), "08b") for char in data]
        else:
            raise TypeError("Unsupported data type, please provide a string.")

    @staticmethod
    def _bin_to_str(binary_data):
        """
        Converts binary data back into a string, stopping at the null character.
        """
        text = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i + 8]
            char = chr(int(byte, 2))
            if char == "\0":
                break
            text += char
        return text

    def encode_text(self, cover_image, text):
        """
        Encodes a hidden text into an image using a difference-based approach.

        Parameters:
        cover_image: Original image (numpy array loaded using cv2.imread)
        text: Text to be hidden

        Method:
        This approach hides text by modifying the blue channel of pixels based
        on the binary representation of the text. For a binary '1', the blue
        channel value is incremented by 1 (unless it's already 255). For a
        binary '0', no change is made.
        """

        if not os.path.exists("StegoImages"):
            os.makedirs("StegoImages")

        # Convert text to binary and concatenate bits
        binary_text = ""
        for ch in self._int_to_bin(text):
            binary_text += ch
        # Add a terminal character to signify the end of the text
        binary_text += "00000000"

        # Create a copy of the cover image (Stego image)
        stego_image = cover_image.copy()
        h, w, c = cover_image.shape

        data_index = 0
        for y in range(h):
            for x in range(w):
                if data_index < len(binary_text):
                    bit = binary_text[data_index]
                    b, g, r = stego_image[y, x]

                    # If the bit is '1', increment the blue channel (if it's not 255)
                    if bit == '1':
                        if b < 255:
                            b += 1
                        else:
                            # If blue channel is already 255, decrement it to handle edge cases
                            b -= 1
                    # If the bit is '0', no changes are made
                    stego_image[y, x] = [b, g, r]
                    data_index += 1
                else:
                    break
            if data_index >= len(binary_text):
                break

        return stego_image

    def decode_text(self, cover_image, stego_image):
        """
        Decodes the hidden text from an image.

        Parameters:
        cover_image: Original image
        stego_image: Encoded image

        Method:
        Compares each pixel of the stego image with the corresponding pixel in the
        cover image. If the blue channel value differs, it indicates a binary '1';
        otherwise, it's a binary '0'. The binary string is then converted back into text.
        """
        h, w, c = cover_image.shape
        binary_data = ""

        for y in range(h):
            for x in range(w):
                cb, cg, cr = cover_image[y, x]
                sb, sg, sr = stego_image[y, x]

                # If the blue channel in the stego image differs, it's a '1'; otherwise, '0'
                if sb != cb:
                    binary_data += "1"
                else:
                    binary_data += "0"

        text = self._bin_to_str(binary_data)
        return text

    def distribute_text(self, images, text):
        """
        Placeholder for distributing text across multiple images.

        This function is not used in this approach but is kept for potential extensions.
        """
        raise NotImplementedError("The distribute_text method is not used in this approach.")