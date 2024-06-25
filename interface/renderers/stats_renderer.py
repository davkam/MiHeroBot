from handlers.temp_img_handler import TempImageHandler
from interface.renderers.renderer import Renderer
from PIL import Image, ImageDraw, ImageFont
from tools.bar import Bar
from users.users import User

class StatsRenderer(Renderer):
    STATS_TEMP = "game/assets/templates/stats_tmpl.png"
    ITEM_BG = "game/assets/templates/item_bg.png"

    def __init__(self, user: User) -> None:
        super().__init__()
        self.user: User = user
        self.image: Image.Image = None

    async def get_stats_image(self) -> str:
        return await self.save_image(image=self.image)

    async def render_stats(self) -> None:
        image = Image.open(fp=StatsRenderer.STATS_TEMP)

        name = await self.render_name()
        char = await self.render_char()
        equipments = await self.render_equips()
        stats = await self.render_player_stats()
        equip_stats = await self.render_equip_stats()

        image.paste(im=char, box=(48, 24), mask=char)
        image.paste(im=name, box=(354, 32), mask=name)
        image.paste(im=equipments, box=(352, 112), mask=equipments) 
        image.paste(im=stats, box=(32, 304), mask=stats)
        image.paste(im=equip_stats, box=(352, 304), mask=equip_stats)

        self.image = image

    async def render_name(self) -> Image.Image:
        name = self.user.player.get_name()
        font_size = 64

        image = Image.new(mode="RGBA", size=(256, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)
        
        name_length = int(font.getlength(text=name))

        while name_length > 240:
            font_size -= 4
            font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)
            name_length = int(font.getlength(text=name))

        x = int((image.width - name_length) / 2)
        y = int((image.height - font_size) / 2 + 4)

        draw.text(xy=(x, y), text=name, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
        
        return image

    async def render_char(self) -> Image.Image:
        image = Image.new(mode="RGBA", size=(264, 256), color=(0, 0, 0, 0))

        char = Image.open(fp=Renderer.PLAYER_PATH % (self.user.player.color.value, 0))

        if self.user.player.equipment.sword:
            sword = Image.open(fp=Renderer.SWORD_PATH % str(self.user.player.equipment.sword.tier.value))
            image.paste(im=sword, box=(148, 8), mask=sword)

        image.paste(im=char, box=(-16, 0), mask=char)

        if self.user.player.equipment.head:
            head = Image.open(fp=Renderer.HEAD_PATH % str(self.user.player.equipment.head.tier.value))
            image.paste(im=head, box=(-16, 0), mask=head)

        if self.user.player.equipment.body:
            body = Image.open(fp=Renderer.BODY_PATH % str(self.user.player.equipment.body.tier.value))
            image.paste(im=body, box=(-16, 0), mask=body)

        if self.user.player.equipment.shield:
            shield = Image.open(fp=Renderer.SHIELD_PATH % str(self.user.player.equipment.shield.tier.value))
            image.paste(im=shield, box=(-12, 124), mask=shield)

        return image
    
    async def render_equips(self) -> Image.Image:
        image = Image.new(mode="RGBA", size=(256, 160), color=(0, 0, 0, 0))
        item_bg = Image.open(fp=StatsRenderer.ITEM_BG)
        
        if self.user.player.equipment.sword:
            sword = Image.open(fp=Renderer.SWORD_PATH % str(self.user.player.equipment.sword.tier.value))
            sword = sword.resize(size=(32, 64), resample=Image.Resampling.BOX)
            image.paste(im=item_bg, box=(0, 16))
            image.paste(im=sword, box=(16, 16), mask=sword)
        if self.user.player.equipment.shield:
            shield = Image.open(fp=Renderer.SHIELD_PATH % str(self.user.player.equipment.shield.tier.value))
            shield = shield.resize(size=(32, 32), resample=Image.Resampling.BOX)
            image.paste(im=item_bg, box=(0, 96))
            image.paste(im=shield, box=(16, 112), mask=shield)
        if self.user.player.equipment.head:
            head = Image.open(fp=Renderer.HEAD_PATH % str(self.user.player.equipment.head.tier.value))
            head = head.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=item_bg, box=(96, 16))
            image.paste(im=head, box=(96, 20), mask=head)
        if self.user.player.equipment.body:
            body = Image.open(fp=Renderer.BODY_PATH % str(self.user.player.equipment.body.tier.value))
            body = body.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=item_bg, box=(96, 96))
            image.paste(im=body, box=(96, 76), mask=body)
        if self.user.player.equipment.amulet:
            amulet = Image.open(fp=Renderer.AMULET_PATH % str(self.user.player.equipment.amulet.tier.value))
            amulet = amulet.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=item_bg, box=(192, 16))
            image.paste(im=amulet, box=(192, 16), mask=amulet)
        if self.user.player.equipment.ring:
            ring = Image.open(fp=Renderer.RING_PATH % str(self.user.player.equipment.ring.tier.value))
            ring = ring.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=item_bg, box=(192, 96))
            image.paste(im=ring, box=(192, 96), mask=ring)

        return image
    
    async def render_player_stats(self) -> Image.Image:
        image = Image.new(mode="RGBA", size=(288, 144), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=Renderer.FONT_PATH, size=32)

        level = self.user.player.level.get_lvl()
        level_prog = await self.user.player.level.get_progress()
        level_bar = await Bar.get_shortbar(act_val=level_prog, max_val=100)
        draw.text(xy=(24, 8), text="LEVEL", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(120, 8), text=str(level), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(164, 8), text=f"{level_bar} ({level_prog}%)", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        attack = self.user.player.attack.get_lvl()
        attack_prog = await self.user.player.attack.get_progress()
        attack_bar = await Bar.get_shortbar(act_val=attack_prog, max_val=100)                     
        draw.text(xy=(24, 40), text="ATTACK", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(120, 40), text=str(attack), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(164, 40), text=f"{attack_bar} ({attack_prog}%)", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        defense = self.user.player.defense.get_lvl()
        defense_prog = await self.user.player.defense.get_progress()
        defense_bar = await Bar.get_shortbar(act_val=defense_prog, max_val=100)
        draw.text(xy=(24, 72), text="DEFENSE", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(120, 72), text=str(defense), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(164, 72), text=f"{defense_bar} ({defense_prog}%)", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        health = self.user.player.health.get_lvl()
        health_prog = await self.user.player.health.get_progress()
        health_bar = await Bar.get_shortbar(act_val=health_prog, max_val=100)
        draw.text(xy=(24, 104), text="HEALTH", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(120, 104), text=str(health), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(164, 104), text=f"{health_bar} ({health_prog}%)", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        return image
    
    async def render_equip_stats(self) -> Image.Image:
        image = Image.new(mode="RGBA", size=(256, 160), color=(255, 0, 0, 0))
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=Renderer.FONT_PATH, size=28)

        if self.user.player.equipment.sword:
            text = self.user.player.equipment.sword.get_name()
            draw.text(xy=(12, 10), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if self.user.player.equipment.shield:
            text = self.user.player.equipment.shield.get_name()
            draw.text(xy=(12, 30), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if self.user.player.equipment.head:
            text = self.user.player.equipment.head.get_name()
            draw.text(xy=(12, 50), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if self.user.player.equipment.body:
            text = self.user.player.equipment.body.get_name()
            draw.text(xy=(12, 70), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if self.user.player.equipment.amulet:
            text = self.user.player.equipment.amulet.get_name()
            draw.text(xy=(12, 90), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if self.user.player.equipment.ring:
            text = self.user.player.equipment.ring.get_name()
            draw.text(xy=(12, 110), text=text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        

        return image      