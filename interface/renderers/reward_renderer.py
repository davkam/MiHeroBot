import asyncio

from game.objects.characters.characters import Character
from interface.renderers.renderer import Renderer
from PIL import Image, ImageDraw, ImageFont
from tools.bar import Bar

class RewardRenderer(Renderer):
    def __init__(self, winner: Character, loser: Character) -> None:
        super().__init__()
        self.winner: Character = winner
        self.loser: Character = loser
        self.image: Image.Image = None

    async def get_xp_reward_image(self, image_type: int = None, image_info: str = None) -> str:
        if image_type == 0:
            att_prog = await self.winner.attack.get_progress()
            att_prog_bar = await Bar.get_shortbar(act_val=att_prog, max_val=100)

            self.image = await self.render_text(image=self.image, text="ATTACK", font_size=32, x=16, y=64)
            self.image = await self.render_text(image=self.image, text=f"{self.winner.attack.get_lvl():<3} {att_prog_bar} ({att_prog}%)", font_size=32, x=128, y=64)
            self.image = await self.render_text(image=self.image, text=f"+{image_info} points", font_size=32, x=128, y=92, color=(0, 255, 0))

        elif image_type == 1:
            def_prog = await self.winner.defense.get_progress()
            def_prog_bar = await Bar.get_shortbar(act_val=def_prog, max_val=100)

            self.image = await self.render_text(image=self.image, text="DEFENSE", font_size=32, x=16, y=120)
            self.image = await self.render_text(image=self.image, text=f"{self.winner.defense.get_lvl():<3} {def_prog_bar} ({def_prog}%)", font_size=32, x=128, y=120)
            self.image = await self.render_text(image=self.image, text=f"+{image_info} points", font_size=32, x=128, y=148, color=(0, 255, 0))

        elif image_type == 2:
            hp_prog = await self.winner.health.get_progress()
            hp_prog_bar = await Bar.get_shortbar(act_val=hp_prog, max_val=100)

            self.image = await self.render_text(image=self.image, text="HEALTH", font_size=32, x=16, y=176)
            self.image = await self.render_text(image=self.image, text=f"{self.winner.health.get_lvl():<3} {hp_prog_bar} ({hp_prog}%)", font_size=32, x=128, y=176)
            self.image = await self.render_text(image=self.image, text=f"+{image_info} points", font_size=32, x=128, y=204, color=(0, 255, 0))

        elif image_type == 3:
            lvl_prog = await self.winner.level.get_progress()
            lvl_prog_bar = await Bar.get_shortbar(act_val=lvl_prog, max_val=100)

            self.image = await self.render_text(image=self.image, text="LEVEL", font_size=32, x=16, y=232)
            self.image = await self.render_text(image=self.image, text=f"{self.winner.level.get_lvl():<3} {lvl_prog_bar} ({lvl_prog}%)", font_size=32, x=128, y=232)

        else:
            pass

        return await self.save_image(image=self.image)
    
    async def get_loot_reward_image(self) -> str:
        pass

    async def render_reward(self) -> None:
        self.image = Image.open(fp=Renderer.BG3_PATH)
        image_left = Image.new(mode="RGBA", size=(320, 270), color=(0, 0, 0, 0))
        image_right = Image.new(mode="RGBA", size=(320, 270), color=(0, 0, 0, 0))

        image_left = await self.render_title(image=image_left, title="!XPGAIN", y_axis=8)
        image_right = await self.render_title(image=image_right, title="!LOOTDROP", y_axis=8)

        self.image.paste(im=image_left, box=(0, 0), mask=image_left)
        self.image.paste(im=image_right, box=(320, 0), mask=image_right)

    async def render_xp(self) -> None:
        pass