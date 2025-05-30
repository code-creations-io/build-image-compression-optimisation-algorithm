# build-image-compression-optimisation-algorithm

- Created at: 2025-05-29
- Created by: `🐢 Arun Godwin Patel @ Code Creations`

## Table of contents

- [Setup](#setup)
  - [System](#system)
  - [Installation](#installation)
- [Walkthrough](#walkthrough)
  - [Code Structure](#code-structure)
  - [Tech stack](#tech-stack)
  - [Build from scratch](#build-from-scratch)
    - [1. Create a virtual environment](#1-create-a-virtual-environment)
    - [2. Activate the virtual environment](#2-activate-the-virtual-environment)
    - [3. Install the required packages](#3-install-the-required-packages)
    - [4. Create the image processing classes](#4-create-the-image-processing-classes)
    - [5. Create the Python module](#5-create-the-python-module)

## Setup

### System

This code repository was tested on the following computers:

- Windows 11

At the time of creation, this code was built using `Python 3.13.3`

### Installation

1. Install `virtualenv`

```bash
# 1. Open a CMD terminal
# 2. Install virtualenv globally
pip install virtualenv
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

```bash
# Windows
.\venv\Scripts\activate
# Mac
source venv/bin/activate
```

4. Install the required packages

```bash
pip install -r requirements.txt
```

5. Run the module

```bash
python main.py
```

## Walkthrough

### Code Structure

The code directory structure is as follows:

```plaintext
create-qr-code-generator
└───algorithm
|   └──compression.py
|   └──optimisation.py
│   __init__.py
│   .gitignore
│   main.py
│   README.md
│   requirements.txt
```

The `main.py` file is a module that you can run to generate a QR code.

The `algorithm/` folder contains files for algorithms to process images.

The `.gitignore` file specifies the files and directories that should be ignored by Git.

The `requirements.txt` file lists the Python packages required by the application.

### Tech stack

**Image processing**

- `Pillow`

### Build from scratch

This project was built using Python and `Pillow`. A file location can be specified within the `main.py` file which when run, will load this image file for compression.

#### 1. Create a virtual environment

```bash
python -m venv venv
```

#### 2. Activate the virtual environment

```bash
# Windows
.\venv\Scripts\activate
# Mac
source venv/bin/activate
```

#### 3. Install the required packages

```bash
pip install -r requirements.txt
```

#### 4. Create the image processing classes

Create a file named `compression.py` in the `algorithm/` directory. This file will contain the `Compressor` class that will handle the compression of images.

First we will add some helper methods to the class.

```python
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
```

Then, we will add the primary method that'll be called when compressing images.

```python
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
```

Now let's populate thee `optimisation.py` file in the `algorithm/` directory. This file will contain the `Optimiser` class that will handle the loop to optimise the compresion of the image until it is a suitable size.

```python
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
```

#### 5. Create the Python module

Next, we will create the `main.py` file in the root directory. This file will be the entry point of the application and will contain the code to compress an image.

```python
import os
import uuid
import logging

from algorithm.optimisation import Optimiser

logger = logging.getLogger()
logger.setLevel(logging.INFO)

IMAGE_FILE = "image.jpg"

if __name__ == "__main__":

    # Load image as bytes
    with open(IMAGE_FILE, 'rb') as f:
        img_bytes = f.read()

    original_size = len(img_bytes)
    print(f"Original image size: {original_size} bytes")

    # Optimise image with compression
    extension = IMAGE_FILE.split('.')[-1]
    optimiser = Optimiser()
    optimised_img = optimiser.optimise(
        bytes_array=img_bytes,
        filename=f"{uuid.uuid4()}.{extension}"
    )

    output_path = os.path.join(os.getcwd(), f'image_compressed.{extension}')
    with open(output_path, 'wb') as f:
        f.write(optimised_img)

    compressed_size = os.path.getsize(output_path)
```

This completes the setup of our image compression & optimisation algorithm!

## Happy coding! 🚀

```bash
🐢 Arun Godwin Patel @ Code Creations
```
