import cv2

from image_handler import ImageHandler
from steganography import Steganography

def main():
    input_folder = "InputImages"
    output_folder = "outputs"
    image_handler = ImageHandler(input_folder, output_folder)
    steganography = Steganography()

    while True:
        print("\n1. Şifrelenmiş resimleri göster")
        print("2. Şifrelenmiş ve şifrelenmemiş resimleri göster")
        print("3. Encode edilmiş bir resmi decode et")
        print("4. Çıkış\n")
        choice = input("Seçiminizi yapınız: ")

        if choice == "1":
            image_handler.read_images()
            encoded_images = steganography.distribute_text(image_handler.images, input("Metni giriniz: "))
            image_handler.save_images(encoded_images)
            image_handler.display_images(image_handler.images)
        elif choice == "2":
            image_handler.read_images()
            print("Bu seçenek henüz implement edilmedi.")
        elif choice == "3":
            path = input("Şifresi çözülecek resmin yolu: ")
            image = cv2.imread(path)
            hidden_text = steganography.decode_text(image)
            print(f"Gizlenen metin: {hidden_text}")
        elif choice == "4":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
