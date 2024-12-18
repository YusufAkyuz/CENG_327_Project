import cv2
import os

class ImageHandler:
    def __init__(self, input_folder=None, output_folder=None):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def load_image(self, image_path):
        """Tek bir resmi yükler."""
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            return image
        else:
            raise FileNotFoundError("Belirtilen resim dosyası bulunamadı.")

    def save_image(self, image, filename):
        """Encode edilmiş resmi kaydeder."""
        if self.output_folder and not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        save_path = os.path.join(self.output_folder if self.output_folder else '', filename)
        cv2.imwrite(save_path, image)
        return save_path
