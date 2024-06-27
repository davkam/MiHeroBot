import logging

from handlers.temp_img_handler import TempImageHandler
from loggers.loggers import Loggers
from PIL import Image, ImageDraw, ImageFont

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

    RED_COLOR = (230, 15, 15)

    def __init__(self):
        self.logger: logging.Logger = Loggers.renderer
        self.image_folder: str = None

    async def render_title(self, image: Image.Image, title: str, font_size: int = None, x_axis: int = None, y_axis: int = None) -> Image.Image:
        if font_size == None:
            font_size = 64

        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)

        # Get title length and calculate axis to center title
        title_length = int(font.getlength(text=title))
        x_pos = x_axis or ((image.width - title_length) / 2)
        y_pos = y_axis or 16

        draw.text(xy=(x_pos, y_pos), text=title, fill=(255, 0, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))

        return image
    
    async def render_text(self, image: Image.Image, text: str, font_size: int, x: int = 0, y: int = 0, color: tuple = (255, 255, 255)) -> Image.Image:
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)

        draw.multiline_text(xy=(x, y), text=text, fill=color, font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        return image

    async def save_image(self, image: Image.Image) -> str:
        image_path = str()

        if self.image_folder == None:
            image_path, self.image_folder = await TempImageHandler.save_temp_image(image=image)
        else:
            image_path, _ = await TempImageHandler.save_temp_image(image=image, temp_dir=self.image_folder)

        return image_path

    async def del_image_folder(self) -> None:
        await TempImageHandler.del_temp_image(temp_path=self.image_folder)