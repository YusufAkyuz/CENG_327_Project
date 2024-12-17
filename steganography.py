import cv2
import numpy as np


class Steganography:
    @staticmethod
    def _int_to_bin(data):
        """Veriyi ikili (binary) formatına dönüştür."""
        if isinstance(data, np.ndarray):
            return [format(value, "08b") for value in data.flatten()]
        elif isinstance(data, str):
            return [format(ord(char), "08b") for char in data]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Veri türü desteklenmiyor.")

    @staticmethod
    def encode_text(image, text):
        """Metni resmin içine LSB kullanarak gizle."""
        binary_text = Steganography._int_to_bin(text) + ['00000000']
        data_index = 0

        for row in image:
            for pixel in row:
                for i in range(3):
                    if data_index < len(binary_text):
                        pixel[i] = int(Steganography._int_to_bin(pixel[i])[:-1] + binary_text[data_index][-1], 2)
                        data_index += 1
        return image

    @staticmethod
    def decode_text(image):
        """Resimden gizlenmiş metni çıkar."""
        binary_data = ""
        for row in image:
            for pixel in row:
                for i in range(3):
                    binary_data += Steganography._int_to_bin(pixel[i])[-1]

        text = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i + 8]
            char = chr(int(byte, 2))
            if char == '\0':
                break
            text += char
        return text

    def distribute_text(self, images, text):
        """Metni resimlere böl ve sırayla şifrele."""
        num_images = len(images)
        split_text = []

        if " " in text:
            split_text = text.split()
        elif len(text) <= num_images:
            split_text = list(text)
        else:
            raise ValueError(f"Metin ya tek bir kelime ya da {num_images} kelime içermelidir.")

        if len(split_text) != num_images:
            raise ValueError(f"{num_images} adet kelime girmelisiniz.")

        encoded_images = []
        for idx, image_path in enumerate(images):
            image = cv2.imread(image_path)
            encoded_image = self.encode_text(image, split_text[idx])
            encoded_images.append(encoded_image)
        return encoded_images
