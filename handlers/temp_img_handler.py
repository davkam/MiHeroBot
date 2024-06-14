import os
import tempfile

from PIL import Image

class TempImageHandler():
    async def new_temp_image(image: Image.Image) -> str:
        # Create a temporary image and get its path
        with tempfile.NamedTemporaryFile(suffix=".png", prefix="mhb_", delete=False) as temp:
            temp_path = temp.name

        # Save image object as temp image
        with open(temp_path, "wb") as path:
            image.save(fp=path)

        return temp_path

    async def del_temp_image(path: str):
        if os.path.exists(path=path):
            os.remove(path=path)