import logging

from handlers.temp_img_handler import TempImageHandler
from loggers.loggers import Loggers
from PIL import Image

class Renderer():
    FONT_PATH = "game/assets/font/m5x7_font.ttf"

    BG1_PATH = "game/assets/backgrounds/bg_1.png"
    BG2_PATH = "game/assets/backgrounds/bg_2.png"
    BG3_PATH = "game/assets/backgrounds/bg_3.png"

    MONSTER_PATH = "game/assets/characters/enemies/monster_%s_%s.png"
    PLAYER_PATH = "game/assets/characters/players/player_%s_%s.png"
    SWORD_PATH = "game/assets/equipments/swords/sword_%s.png"
    SHIELD_PATH = "game/assets/equipments/shields/shield_%s.png"
    HEAD_PATH = "game/assets/equipments/head_armors/head_%s.png"
    BODY_PATH = "game/assets/equipments/body_armors/body_%s.png"
    AMULET_PATH = "game/assets/equipments/amulets/amulet_%s.png"
    RING_PATH = "game/assets/equipments/rings/ring_%s.png"

    def __init__(self):
        self.logger: logging.Logger = Loggers.renderer
        self.image_folder: str = None

    async def save_image(self, image: Image.Image) -> str:
        image_path = str()

        if self.image_folder == None:
            image_path, self.image_folder = await TempImageHandler.save_temp_image(image=image)
        else:
            image_path, _ = await TempImageHandler.save_temp_image(image=image, temp_dir=self.image_folder)

        return image_path

    async def del_images(self) -> None:
        await TempImageHandler.del_temp_image(temp_path=self.image_folder)