import cv2
import os

from steganography import Steganography


def main():
    steganography = Steganography()

    # Dictionary to store cover images and their corresponding stego images
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

    # List to store hidden texts
    hidden_texts = []

    # List of paths for stego images
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
        print("Press 'e' to start the encoding process.")
        print("Press 'd' to start the decoding process.")
        print("Press 'q' to exit.")
        user_input = input("Your choice: ")

        if user_input == "e":
            print(f"\nCover images loaded. There are {len(cover_images_and_stego_images)} cover images.\n")
            print("******************************************************************************************\n")
            print(f"Enter {len(cover_images_and_stego_images)} hidden texts for the cover images.")

            # Collect hidden texts from the user
            for i in range(len(cover_images_and_stego_images)):
                hidden_texts.append(input(f"\tEnter hidden text {i + 1}: "))
            print("*** Texts saved ***\n")

            print("Encoding process started for images.")

            # Perform encoding for each cover image
            for i in range(len(cover_images_and_stego_images)):
                cover_image_path = list(cover_images_and_stego_images.keys())[i]
                cover_image = cv2.imread(cover_image_path)
                if cover_image is None:
                    print(f"Cover image {i + 1} could not be read.")
                    continue
                stego_image = steganography.encode_text(cover_image, hidden_texts[i])
                cv2.imwrite(path_of_stego_images[i], stego_image)
                cover_images_and_stego_images[cover_image_path] = stego_image
                print(f"\tEncoding completed for image {i + 1}.")

            print("*** All images encoded ***\n")
            print("******************************************************************************************\n")

        elif user_input == "d":
            if not hidden_texts:
                print("Error: Encoding must be completed before decoding.")
                continue

            print("\n\nDecoding process started.")
            # Perform decoding for each pair of cover and stego images
            for i in range(len(cover_images_and_stego_images)):
                cover_image_path = list(cover_images_and_stego_images.keys())[i]
                cover_image = cv2.imread(cover_image_path)
                stego_image = cv2.imread(path_of_stego_images[i])
                if cover_image is None or stego_image is None:
                    print(f"Images for pair {i + 1} could not be read.")
                    continue
                if cover_image.shape != stego_image.shape:
                    print(f"Dimensions mismatch for pair {i + 1}.")
                    continue
                hidden_text = steganography.decode_text(cover_image, stego_image)
                print(f"\tHidden text for image {i + 1}: {hidden_text}")

            print("\n*** Decoding completed for all images. ***\n")

        elif user_input == "q":
            print("Exiting.")
            break

        else:
            print("Error: Invalid choice. Please try again.")
            continue


if __name__ == "__main__":
    main()