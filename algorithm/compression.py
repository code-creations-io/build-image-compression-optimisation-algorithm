from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
import io
import os

class Compressor:

    def __init__(self):
        self.temporary_store = os.getcwd()

    @staticmethod
    def _load_img_from_bytes_array(bytes_array: bytes = None):
        return Image.open(io.BytesIO(bytes_array))  # Fixed: removed base64 decoding

    @staticmethod
    def _img_shape(img: JpegImageFile = None):
        return img.size

    @staticmethod
    def _img_size(path):
        return os.path.getsize(path)

    @staticmethod
    def _save_img(
        img: JpegImageFile = None,
        path: str = "/tmp/",
        filename: str = "",
        quality: int = 100,
        optimize: bool = True
    ):
        save_path = f"{path}{filename}"
        img.save(save_path, quality=quality, optimize=optimize)
        return filename

    @staticmethod
    def _img_bytes_array(img: JpegImageFile = None):
        buff = io.BytesIO()
        img.save(buff, format='JPEG')
        return buff.getvalue()

    @staticmethod
    def _delete_img(
        path: str = "/tmp/",
        filename: str = ""
    ):
        to_remove = f"{path}{filename}"
        if os.path.exists(to_remove):
            os.remove(to_remove)

    def compress(
        self,
        img: JpegImageFile = None,
        img_size: int = None,
        img_path: str = "",
        filename: str = "",
        new_size_ratio: float = 1.0,
        quality: int = 80,
        width: int = None,
        height: int = None,
        to_jpg: bool = True
    ):
        if new_size_ratio < 1.0:
            img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.LANCZOS)
            print(f"New shape: {self._img_shape(img=img)}")

        elif width and height:
            img = img.resize((width, height), Image.LANCZOS)
            print(f"New shape: {self._img_shape(img=img)}")

        filename, ext = os.path.splitext(img_path)
        new_filename = f"{filename}_compressed.jpg" if to_jpg else f"{filename}_compressed{ext}"

        try:
            new_path = self._save_img(
                img=img,
                path=self.temporary_store,
                filename=new_filename,
                quality=quality,
                optimize=True
            )
        except OSError:
            img = img.convert("RGB")
            new_path = self._save_img(
                img=img,
                path=self.temporary_store,
                filename=new_filename,
                quality=quality,
                optimize=True
            )

        new_img_size = self._img_size(path=f"{self.temporary_store}{new_path}")
        new_img_bytes = self._img_bytes_array(img=img)
        print(f"New size: {new_img_size} bytes")

        self._delete_img(path=self.temporary_store, filename=img_path)
        self._delete_img(path=self.temporary_store, filename=new_path)

        saving_diff = new_img_size - img_size
        print(f"Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
        return new_img_bytes, new_img_size