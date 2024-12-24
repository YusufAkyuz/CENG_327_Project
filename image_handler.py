import cv2
import os

class ImageHandler:
    def __init__(self, input_folder=None, output_folder=None):
        """Initialize the ImageHandler class with input and output folder paths."""
        self.input_folder = input_folder
        self.output_folder = output_folder if output_folder else os.getcwd()

    def load_image(self, image_path):
        """Loads a single image from the specified path."""
        if os.path.exists(image_path):
            if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError("The file is not a valid image.")
                return image
            else:
                raise ValueError("Unsupported file format. Please select a valid image.")
        else:
            raise FileNotFoundError("The specified image file could not be found.")

    def save_image(self, image, filename):
        """Saves the encoded image to the specified output folder."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        save_path = os.path.join(self.output_folder, filename)
        cv2.imwrite(save_path, image)
        return save_path

    def resize_image(self, image, width=600, height=400):
        """Resizes the image to fit within the specified dimensions."""
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)