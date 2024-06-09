import os

from interface.renderers.renderer import Renderer
from PIL import Image, ImageDraw, ImageFont

class InfoRenderer(Renderer):
    ABOUT_TMPL = "game/assets/templates/about_tmpl.png"

    HELP_PATH = "game/assets/menus/help.png"
    ABOUT_PATH = "game/assets/menus/about_%s.png"

    HELP_TXT = "txt/help.txt"
    ABOUT_TXT = "txt/about.txt"

    def __init__(self):
        super().__init__()

    async def render_help(self):
        image = Image.open(fp=InfoRenderer.BG1_PATH)

        await self.__render_title(image=image, title="COMMANDS")

        with open(file=InfoRenderer.HELP_TXT) as file:
            string = file.read()

        text = string.split("#")
        
        try:
            image = await self.__render_text(image=image, text=text[2].strip(), font_size=32, x=48, y=76)
            image = await self.__render_text(image=image, text=text[4].strip(), font_size=32, x=192, y=76)

            await self.save_image(image=image, path=InfoRenderer.HELP_PATH)

            self.logger.info(msg=f"Successfully rendered new 'help' image. FILE: '{InfoRenderer.HELP_PATH}'")
        except Exception as exception:
            self.logger.error(msg=f"Failed to render new 'help' image. EXCEPTION: {str(exception)}")

    async def render_about(self):
        with open(file=InfoRenderer.ABOUT_TXT) as file:
            string = file.read()

        text = string.split("#")

        try:
            text_size = 28
            text_x = 32
            text_y = 72
            for index, text in enumerate(text):
                if index % 2 != 0 and index != 0:
                    if index == 1:
                        text_y += 182
                        image = Image.open(fp=InfoRenderer.ABOUT_TMPL)
                        image = await self.__render_title(image=image, title=text.strip(), y=196)
                    else:
                        text_y = 72
                        image = Image.open(fp=InfoRenderer.BG1_PATH)
                        image = await self.__render_title(image=image, title=text.strip())
                elif index % 2 == 0 and index != 0:
                    image = await self.__render_text(image=image, text=text.strip(), font_size=text_size, x=text_x, y=text_y)
                    image = await self.__render_text(image=image, text=f"{int(index / 2)}/5", font_size=text_size, x=300, y=450)
                    await self.save_image(image=image, path=InfoRenderer.ABOUT_PATH % int(index / 2))
            
            self.logger.info(msg=f"Successfully rendered new 'about' images. FILES: '{InfoRenderer.ABOUT_PATH}'")
        except Exception as exception:
            self.logger.error(msg=f"Failed to render new 'about' images. EXCEPTION: {str(exception)}")       

    async def __render_title(self, image: Image.Image, title: str, x: int = None, y: int = None) -> Image.Image:
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=InfoRenderer.FONT_PATH, size=64)

        # Get title length and calculate axis to center title
        title_length = int(font.getlength(text=title))
        x_axis = x or ((image.width - title_length) / 2)
        y_axis = y or 16

        draw.text(xy=(x_axis, y_axis), text=title, fill=(230, 15, 15), font=font, stroke_width=2, stroke_fill=(0, 0, 0))

        return image
    
    async def __render_text(self, image: Image.Image, text: str, font_size: int, x: int = 0, y: int = 0) -> Image.Image:
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=InfoRenderer.FONT_PATH, size=font_size)

        draw.multiline_text(xy=(x, y), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        return image
    
    async def save_image(self, image: Image.Image, path: str) -> str:
        if not os.path.exists(path="game/assets/menus"):
            os.makedirs(name="game/assets/menus")
            
            self.logger.warning(msg=f"No directory found 'game/assets/menus', new directory created")

        image.save(fp=path)

        return path