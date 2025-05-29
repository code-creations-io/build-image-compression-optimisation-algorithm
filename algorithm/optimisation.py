from .compression import Compressor

class Optimiser:

    def __init__(self, quality: int = 80):
        self.increment = 0.01
        self.quality = quality
        self.threshold = 99000
        self.compressor = Compressor()

    def optimise(self, bytes_array: bytes = None, filename: str = ""):
        print(f"Optimising image size by compression")

        print(f"Loading image \"{filename}\"")
        img = self.compressor._load_img_from_bytes_array(bytes_array=bytes_array)
        img_path = self.compressor._save_img(
            img=img,
            path=self.compressor.temporary_store, 
            filename=f"{filename}",
        )

        shape = self.compressor._img_shape(img=img)
        img_size = self.compressor._img_size(path=f"{self.compressor.temporary_store}{img_path}")
        print(f"Original shape: {shape}")
        print(f"Original size: {img_size} bytes")

        cnt = 0
        while True:
            ratio = 1 - (cnt * self.increment)
            print(f"Trying: round = {cnt}, ratio = {ratio}, quality = {self.quality}")
            new_img_bytes, new_img_size = self.compressor.compress(
                img=img,
                img_size=img_size,
                img_path=img_path,
                filename=filename,
                new_size_ratio=ratio,
                quality=self.quality,
                to_jpg=True
            )

            if new_img_size > self.threshold:
                cnt += 1
                continue
            
            print(f"\n---> Optimisation complete at ratio {ratio}")
            print(f"---> New size: {new_img_size} bytes")
            break
        
        return new_img_bytes
