from game.objects.characters.characters import Character
from interface.renderers.renderer import Renderer
from PIL import Image, ImageDraw, ImageFont
from tools.tools import Bar

class RewardRenderer(Renderer):
    __slots__ = ['winner', 'loser', 'image']
    
    def __init__(self, winner: Character, loser: Character) -> None:
        super().__init__()
        self.winner: Character = winner
        self.loser: Character = loser
        self.image: Image.Image = None

    async def get_xp_reward_image(self, image_type: int = None, image_info: str = None) -> str:
        if image_type == 0:     # ATTACK
            prog = await self.winner.attack.get_progress()
            prog_bar = await Bar.get_shortbar(act_val=prog, max_val=100)

            await self.render_xp(xp_type="ATTACK", xp_lvl=self.winner.attack.get_lvl(), xp_prog_bar=prog_bar, xp_prog=prog, xp_points=image_info, is_total_level=False, y_pos=64)
        elif image_type == 1:   # DEFENSE
            prog = await self.winner.defense.get_progress()
            prog_bar = await Bar.get_shortbar(act_val=prog, max_val=100)

            await self.render_xp(xp_type="DEFENSE", xp_lvl=self.winner.defense.get_lvl(), xp_prog_bar=prog_bar, xp_prog=prog, xp_points=image_info, is_total_level=False, y_pos=120)
        elif image_type == 2:   # HEALTH
            prog = await self.winner.health.get_progress()
            prog_bar = await Bar.get_shortbar(act_val=prog, max_val=100)

            await self.render_xp(xp_type="HEALTH", xp_lvl=self.winner.health.get_lvl(), xp_prog_bar=prog_bar, xp_prog=prog, xp_points=image_info, is_total_level=False, y_pos=176)
        elif image_type == 3:   # LEVEL
            prog = await self.winner.level.get_progress()
            prog_bar = await Bar.get_shortbar(act_val=prog, max_val=100)

            await self.render_xp(xp_type="LEVEL", xp_lvl=self.winner.level.get_lvl(), xp_prog_bar=prog_bar, xp_prog=prog, xp_points=image_info, is_total_level=True, y_pos=232)
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

    async def render_xp(self, xp_type: str, xp_lvl: int, xp_prog_bar: str, xp_prog: int, xp_points: int, is_total_level: bool, y_pos: int) -> None:
        self.image = await self.render_text(image=self.image, text=xp_type, font_size=32, x=16, y=y_pos)
        self.image = await self.render_text(image=self.image, text=f"{xp_lvl:<3} {xp_prog_bar} ({xp_prog}%)", font_size=32, x=128, y=y_pos)
        if not is_total_level:
            self.image = await self.render_text(image=self.image, text=f"+{xp_points} points", font_size=32, x=128, y=y_pos+28, color=(0, 255, 0))