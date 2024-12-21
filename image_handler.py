import cv2
import os

class ImageHandler:
    def __init__(self, input_folder=None, output_folder=None):
        """Initialize the ImageHandler class with input and output folder paths."""
        self.input_folder = input_folder
        self.output_folder = output_folder

    def load_image(self, image_path):
        """Loads a single image from the specified path."""
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            return image
        else:
            raise FileNotFoundError("The specified image file could not be found.")

    def save_image(self, image, filename):
        """Saves the encoded image to the specified output folder."""
        if self.output_folder and not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        save_path = os.path.join(self.output_folder if self.output_folder else '', filename)
        cv2.imwrite(save_path, image)
        return save_path