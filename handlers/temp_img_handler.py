import os
import shutil
import tempfile

from PIL import Image

class TempImageHandler():
    async def save_temp_image(image: Image.Image, temp_dir: str = None) -> tuple[str, str]:
        if temp_dir == None:
            temp_dirpath = tempfile.mkdtemp(prefix="mhb_")
        else:
            temp_dirpath = temp_dir

        # Create a temporary image and get its path
        with tempfile.NamedTemporaryFile(suffix=".png", prefix="mhb_", dir=temp_dirpath, delete=False) as temp:
            temp_filepath = temp.name

        # Save image object as temp image
        with open(temp_filepath, "wb") as path:
            image.save(fp=path)

        return temp_filepath, temp_dirpath

    async def del_temp_image(temp_path: str):
        if os.path.exists(path=temp_path):
            shutil.rmtree(path=temp_path)