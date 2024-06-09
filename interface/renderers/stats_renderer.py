from interface.renderers.renderer import Renderer
from PIL import Image, ImageDraw, ImageFont
from users.users import User

class StatsRenderer(Renderer):
    STATS_TEMP = "game/assets/templates/stats_tmpl.png"

    CHAR_PATH = "game/assets/characters/players/player_%s.png"
    SWORD_PATH = "game/assets/equipments/swords/sword_%s.png"
    SHIELD_PATH = "game/assets/equipments/shields/shield_%s.png"
    HEAD_PATH = "game/assets/equipments/head_armors/head_%s.png"
    BODY_PATH = "game/assets/equipments/body_armors/body_%s.png"
    AMULET_PATH = "game/assets/equipments/amulets/amulet_%s.png"

    def __init__(self) -> None:
        super().__init__()

    async def render_stats(self, user: User):
        image = Image.open(fp=StatsRenderer.STATS_TEMP)
        char = await self.render_char(user=user)
        name = await self.render_name(user=user)
        equipments = await self.render_equips(user=user)
        player_stats = await self.render_player_stats(user=user)

        image.paste(im=char, box=(56, 28), mask=char)
        image.paste(im=name, box=(354, 32), mask=name) # 352, 32 
        image.paste(im=equipments, box=(352, 112), mask=equipments) 
        image.paste(im=player_stats, box=(32, 304), mask=player_stats)

        image.show()

    async def render_char(self, user: User) -> Image.Image:
        image = Image.new(mode="RGBA", size=(256, 256), color=(0, 0, 0, 0))

        char = Image.open(fp=StatsRenderer.CHAR_PATH % str(user.player.color.value))

        if user.player.equipment.sword:
            sword = Image.open(fp=StatsRenderer.SWORD_PATH % str(user.player.equipment.sword.tier.value))
            image.paste(im=sword, box=(140, 8), mask=sword)

        image.paste(im=char, box=(-16, 0), mask=char)

        if user.player.equipment.head:
            head = Image.open(fp=StatsRenderer.HEAD_PATH % str(user.player.equipment.head.tier.value))
            image.paste(im=head, box=(-16, 0), mask=head)

        if user.player.equipment.body:
            body = Image.open(fp=StatsRenderer.BODY_PATH % str(user.player.equipment.body.tier.value))
            image.paste(im=body, box=(-16, 0), mask=body)

        if user.player.equipment.shield:
            shield = Image.open(fp=StatsRenderer.SHIELD_PATH % str(user.player.equipment.shield.tier.value))
            image.paste(im=shield, box=(-12, 124), mask=shield)

        return image
    
    async def render_name(self, user: User) -> Image.Image: # 256, 64
        name = user.player.get_name()
        font_size = 64

        image = Image.new(mode="RGBA", size=(256, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=StatsRenderer.FONT_PATH, size=font_size)
        
        name_length = int(font.getlength(text=name))

        while name_length > 240:
            font_size -= 4
            font = ImageFont.truetype(font=StatsRenderer.FONT_PATH, size=font_size)
            name_length = int(font.getlength(text=name))

        x = int((image.width - name_length) / 2)
        y = int((image.height - font_size) / 2 + 4)

        draw.text(xy=(x, y), text=name, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
        
        return image
    
    async def render_equips(self, user: User) -> Image.Image: # 256, 160
        image = Image.new(mode="RGBA", size=(256, 160), color=(0, 0, 0, 0))
        
        if user.player.equipment.sword:
            sword = Image.open(fp=StatsRenderer.SWORD_PATH % str(user.player.equipment.sword.tier.value))
            sword = sword.resize(size=(32, 64), resample=Image.Resampling.BOX)
            image.paste(im=sword, box=(16, 16))
        if user.player.equipment.shield:
            shield = Image.open(fp=StatsRenderer.SHIELD_PATH % str(user.player.equipment.shield.tier.value))
            shield = shield.resize(size=(32, 32), resample=Image.Resampling.BOX)
            image.paste(im=shield, box=(16, 112), mask=shield)
        if user.player.equipment.head:
            head = Image.open(fp=StatsRenderer.HEAD_PATH % str(user.player.equipment.head.tier.value))
            head = head.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=head, box=(96, 16), mask=head)
        if user.player.equipment.body:
            body = Image.open(fp=StatsRenderer.BODY_PATH % str(user.player.equipment.body.tier.value))
            body = body.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=body, box=(96, 76), mask=body)
        if user.player.equipment.amulet:
            amulet = Image.open(fp=StatsRenderer.AMULET_PATH % str(user.player.equipment.amulet.tier.value))
            amulet = amulet.resize(size=(64, 64), resample=Image.Resampling.BOX)
            image.paste(im=amulet, box=(192, 16), mask=amulet)

        return image
    
    async def render_player_stats(self, user: User) -> Image.Image: # 288, 144
        image = Image.new(mode="RGBA", size=(288, 144), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(font=StatsRenderer.FONT_PATH, size=32)

        level = user.player.level.get_lvl()
        level_prog = f"{await user.player.level.get_progress()}%"
        draw.text(xy=(24, 8), text="LEVEL:", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(128, 8), text=str(level), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(176, 8), text=level_prog, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if level < 100:
            next_level = f"> {level + 1}"
            draw.text(xy=(224, 8), text=next_level, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        attack = user.player.attack.get_lvl()
        attack_prog = f"{await user.player.attack.get_progress()}%"
        draw.text(xy=(24, 40), text="ATTACK:", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(128, 40), text=str(attack), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(176, 40), text=attack_prog, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if attack < 100:
            next_attack = f"> {attack + 1}"
            draw.text(xy=(224, 40), text=next_attack, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        defense = user.player.defense.get_lvl()
        defense_prog = f"{await user.player.defense.get_progress()}%"
        draw.text(xy=(24, 72), text="DEFENSE:", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(128, 72), text=str(defense), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(176, 72), text=defense_prog, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if defense < 100:
            next_defense = f"> {defense + 1}"
            draw.text(xy=(224, 72), text=next_defense, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        health = user.player.health.get_lvl()
        health_prog = f"{await user.player.health.get_progress()}%"
        draw.text(xy=(24, 104), text="HEALTH:", fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(128, 104), text=str(health), fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text(xy=(176, 104), text=health_prog, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        if health < 100:
            next_health = f"> {health + 1}"
            draw.text(xy=(224, 104), text=next_health, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

        return image