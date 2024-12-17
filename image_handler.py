import os
import cv2
import matplotlib.pyplot as plt


class ImageHandler:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.images = []

    def read_images(self):
        """Klasördeki resimleri oku ve listele."""
        self.images = [os.path.join(self.input_folder, file)
                       for file in os.listdir(self.input_folder) if file.endswith('.png')]
        print(f"{len(self.images)} adet resim okundu.")

    def save_images(self, images):
        """Resimleri belirtilen klasöre kaydet."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        for idx, img in enumerate(images):
            output_path = os.path.join(self.output_folder, f"encoded_{idx + 1}.png")
            cv2.imwrite(output_path, img)
            print(f"Resim kaydedildi: {output_path}")

    def display_images(self, images):
        """Resimleri tek tek göster."""
        for img_path in images:
            image = cv2.imread(img_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # RGB formatına dönüştür
            plt.imshow(image_rgb)
            plt.title("Resim Görüntüleme")
            plt.axis("off")  # Eksenleri gizle
            plt.show()
            print("Sonraki resim için 'y' tuşuna basınız.")
            key = input()
            if key.lower() != 'y':
                break
