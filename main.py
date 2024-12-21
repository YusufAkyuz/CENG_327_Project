import cv2
import os

from steganography import Steganography

def main():
    steganography = Steganography()

    cover_images_and_stego_images = {
        "InputImages/1.png": None,
        "InputImages/2.png": None,
        "InputImages/3.png": None,
        "InputImages/4.png": None,
        "InputImages/5.png": None,
        "InputImages/6.png": None,
        "InputImages/7.png": None,
        "InputImages/8.png": None,
        "InputImages/9.png": None
    }

    hidden_texts = []

    path_of_stego_images = ["StegoImages/1.png",
                            "StegoImages/2.png",
                            "StegoImages/3.png",
                            "StegoImages/4.png",
                            "StegoImages/5.png",
                            "StegoImages/6.png",
                            "StegoImages/7.png",
                            "StegoImages/8.png",
                            "StegoImages/9.png"]


    while True:

        print("Encode işlemi başlatmak için 'e' tuşuna basınız.")
        print("Decode işlemi başlatmak için 'd' tuşuna basınız.")
        print("Çıkış yapmak için 'q' tuşuna basınız.")
        user_input = input("Seçiminiz: ")

        if user_input == "e":
            print(f"\nCover images okundu. {len(cover_images_and_stego_images)} adet cover images var.\n")
            print("******************************************************************************************\n")
            print(f"Cover images için {len(cover_images_and_stego_images)} adet gizlenecek metin giriniz.")
            for i in range(len(cover_images_and_stego_images)):
                hidden_texts.append(input(f"\t{i + 1}. metni giriniz: "))
            print("*** Metinler kaydedildi ***\n")

            print("Resimler için encode işlemi başladı.")

            for i in range(len(cover_images_and_stego_images)):
                cover_image_path = list(cover_images_and_stego_images.keys())[i]
                cover_image = cv2.imread(cover_image_path)
                if cover_image is None:
                    print(f"{i+1}. cover image okunamadı.")
                    continue
                stego_image = steganography.encode_text(cover_image, hidden_texts[i])
                cv2.imwrite(path_of_stego_images[i], stego_image)
                cover_images_and_stego_images[cover_image_path] = stego_image
                print(f"\t{i+1} resim için encode işlemi tamamlandı.")

            print("*** Resimler encode edildi ***\n")
            print("******************************************************************************************\n")


        elif user_input == "d":
            if not hidden_texts:
                print("Hata: Decode işlemi için önce encode işlemi tamamlanmalı.")
                continue

            print("\n\nDecode işlemi başladı.")
            for i in range(len(cover_images_and_stego_images)):
                cover_image_path = list(cover_images_and_stego_images.keys())[i]
                cover_image = cv2.imread(cover_image_path)
                stego_image = cv2.imread(path_of_stego_images[i])
                if cover_image is None or stego_image is None:
                    print(f"{i+1}. resimler okunamadı.")
                    continue
                if cover_image.shape != stego_image.shape:
                    print(f"{i+1}. cover ve stego resimlerin boyutları uyuşmuyor.")
                    continue
                hidden_text = steganography.decode_text(cover_image, stego_image)
                print(f"\t{i+1}. resmin gizli metni: {hidden_text}")

            print("\n*** Tüm resimler için decode işlemi tamamlandı. ***\n")

        elif user_input == "q":
            print("Çıkış yapılıyor.")
            break

        else:
            print("Hata: Geçersiz seçim. Lütfen tekrar deneyin.")
            continue



if __name__ == "__main__":
    main()
