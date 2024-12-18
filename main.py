import cv2
import os
from steganography import Steganography

def main():
    steganography = Steganography()

    while True:
        print("\n1. İki resmi kullanarak metin encode et (cover -> stego)")
        print("2. İki resmin farkından metin decode et (cover ve stego)")
        print("3. Çıkış\n")
        choice = input("Seçiminizi yapınız: ")

        if choice == "1":
            cover_path = input("Cover resmin yolunu girin: ")
            if not os.path.exists(cover_path):
                print("Cover resmi bulunamadı.")
                continue

            text = input("Gizlenecek metni girin: ")
            cover_image = cv2.imread(cover_path)
            if cover_image is None:
                print("Cover resmi okunamadı.")
                continue

            stego_image = steganography.encode_text(cover_image, text)

            output_path = "stego_image.png"
            cv2.imwrite(output_path, stego_image)
            print(f"Encode işlemi tamamlandı. Yeni resim '{output_path}' olarak kaydedildi.")

        elif choice == "2":
            cover_path = input("Cover resmin yolunu girin: ")
            stego_path = input("Stego resmin yolunu girin: ")
            if not os.path.exists(cover_path) or not os.path.exists(stego_path):
                print("Cover veya stego resmi bulunamadı.")
                continue

            cover_image = cv2.imread(cover_path)
            stego_image = cv2.imread(stego_path)
            if cover_image is None or stego_image is None:
                print("Resim(ler) okunamadı.")
                continue

            if cover_image.shape != stego_image.shape:
                print("Cover ve stego resimlerin boyutları aynı olmalı.")
                continue

            hidden_text = steganography.decode_text(cover_image, stego_image)
            print(f"Gizlenen metin: {hidden_text}")

        elif choice == "3":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
