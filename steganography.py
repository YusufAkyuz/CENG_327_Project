import cv2
import numpy as np


class Steganography:
    @staticmethod
    def _int_to_bin(data):
        if isinstance(data, str):
            return [format(ord(char), "08b") for char in data]
        else:
            raise TypeError("Veri türü desteklenmiyor, lütfen string girin.")

    @staticmethod
    def _bin_to_str(binary_data):
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
        cover_image: Orijinal resim (cv2.imread ile okunmuş bir numpy array)
        text: Gizlenecek metin

        Bu yöntem LSB yerine iki resim arasındaki farkı kullanarak
        metni gizler. Cover resmi temel alınarak, bit '1' olan
        piksellerin mavi kanal değerini +1 artırıyoruz.
        Bit '0' olanlarda değişiklik yapmıyoruz.
        """
        # Metni binary formatına çevir ve bitlere aç
        binary_text = ""
        for ch in self._int_to_bin(text):
            binary_text += ch
        # Mesaj sonuna terminal karakteri ekleniyor
        binary_text += "00000000"

        # Cover resmin kopyasını al (Stego resim)
        stego_image = cover_image.copy()
        h, w, c = cover_image.shape

        data_index = 0
        for y in range(h):
            for x in range(w):
                if data_index < len(binary_text):
                    bit = binary_text[data_index]
                    b, g, r = stego_image[y, x]

                    # bit '1' ise mavi kanalı 1 artır (eğer 255 değilse)
                    if bit == '1':
                        if b < 255:
                            b += 1
                        else:
                            # eğer b zaten 255 ise, b'yi 1 azalt.
                            # (Bu durum çok ender olacak, ama önlem olarak)
                            b -= 1
                    # bit '0' için değişiklik yok
                    stego_image[y, x] = [b, g, r]
                    data_index += 1
                else:
                    break
            if data_index >= len(binary_text):
                break

        return stego_image

    def decode_text(self, cover_image, stego_image):
        """
        cover_image: Orijinal resim
        stego_image: Encode edilmiş resim

        İki resmi piksel piksel karşılaştırır.
        Eğer stego pikselin mavi kanalı coverdan farklı ise bit '1', aynı ise bit '0'.
        Bu şekilde binary string elde edilip metne dönüştürülür.
        """
        h, w, c = cover_image.shape
        binary_data = ""

        for y in range(h):
            for x in range(w):
                cb, cg, cr = cover_image[y, x]
                sb, sg, sr = stego_image[y, x]

                # Eğer stego resimdeki piksel coverdan farklıysa bit '1', değilse '0'
                if sb != cb:
                    binary_data += "1"
                else:
                    binary_data += "0"

        text = self._bin_to_str(binary_data)
        return text

    def distribute_text(self, images, text):
        # Bu fonksiyon bu yaklaşımda kullanılmıyor ancak varlığını koruyoruz.
        raise NotImplementedError("Bu yöntemde distribute_text kullanılmıyor.")
