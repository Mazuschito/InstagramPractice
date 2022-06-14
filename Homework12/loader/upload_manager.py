import os
from random import randint

from Homework12.loader.exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError


class UploadManager:
    def get_free_filename(self, folder, file_type):
        attempts = 0
        range_of_free_numbers = 100
        limit_of_attempts = 1000

        while True:
            pic_name = str(randint(0, range_of_free_numbers))
            filename_to_save = f"{pic_name}.{file_type}"
            os_path = os.path.join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)

            if not is_filename_occupied:
                return filename_to_save

            attempts += 1

            if attempts > limit_of_attempts:
                raise OutOfFreeNamesError("No free names to save picture")

    def is_file_type_valid(self, file_type):
        if file_type.lower() in ["jpeg", "jpg", "gif", "png", "webp", "tiff"]:
            return True
        return False

    def save_with_random_name(self, picture):

        # Get data from the picture
        filename = picture.filename
        file_type = filename.split(".")[-1]

        # Check if file type is valid
        if not self.is_file_type_valid(file_type):
            raise PictureFormatNotSupportedError(f"Format {file_type} is not supported")

        # Get free name
        folder = os.path.join(".", "uploads", "images")
        filename_to_save = self.get_free_filename(folder, file_type)

        # Save with new name
        try:
            picture.save(os.path.join(folder, filename_to_save))
        except FileNotFoundError:
            raise PictureNotUploadedError(f"{folder, filename_to_save}")

        # Form path for client browser
        web_path = f"/uploads/images/{filename_to_save}"

        return filename_to_save
