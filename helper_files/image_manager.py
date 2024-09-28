from os import listdir
from copy import copy
from PIL import Image, ImageTk
from tkinter import Image as TkImage
from typing import Optional


class ImageManager:
    __valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    def __init__(self, folder_path: str = "images"):
        self.__folder_path = folder_path
        self.__stored_images = self.__load_images()

    def __load_images(self) -> dict[str, Image.Image]:
        """Load images from the folder and return a dictionary of image names and PIL Images."""
        image_names = self.__get_image_names_in_folder()
        pil_images = self.__load_pil_images(image_names)
        return dict(zip(image_names, pil_images))

    def __get_image_names_in_folder(self) -> list[str]:
        """Get valid image filenames from the folder."""
        return [
            filename for filename in listdir(self.__folder_path)
            if filename.lower().endswith(self.__valid_extensions)
        ]

    def __load_pil_images(self, image_names: list[str]) -> list[Image.Image]:
        """Load PIL images from the folder."""
        return [Image.open(f"{self.__folder_path}/{name}") for name in image_names]

    def get_image(self, name: str, size: Optional[tuple[int, int]] = None) -> Optional[Image.Image]:
        """Retrieve an image by name, optionally resizing it."""
        image = self.__stored_images.get(name)
        if image is None:
            return None
        return copy(image) if size is None else image.resize(size)

    def get_tkinter_image(self, name: str, size: Optional[tuple[int, int]] = None) -> Optional[ImageTk.PhotoImage |
                                                                                               TkImage]:
        """Retrieve a Tkinter-compatible PhotoImage, optionally resizing it."""
        pil_image = self.get_image(name, size)
        return ImageTk.PhotoImage(pil_image) if pil_image else None


