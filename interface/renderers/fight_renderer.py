from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player
from interface.renderers.renderer import Renderer
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tools.bar import Bar

class FightRenderer(Renderer):
    def __init__(self, fighter_one: Player, fighter_two: Character) -> None:
        super().__init__()
        self.fighter_one: Player = fighter_one
        self.fighter_two: Character = fighter_two
        self.fight_images: dict[int, Image.Image] = dict()
        self.stats_image: Image.Image = None

    async def get_fight_images(self, image: int, image_info: str, image_variant: bool = None) -> list[str]:
        if image < 0 or image >= len(self.fight_images):
            return False
        
        image_path: list[str] = list()
        
        if image_info == "countdown":
            for i in range(5):
                fight_image = self.fight_images[image].copy()
                image_draw = ImageDraw.Draw(im=fight_image)
                image_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=128)
                image_text = None

                if i == 4:
                    image_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=96)
                    image_text = "FIGHT"
                else:
                    image_text = str(3 - i)

                text_length = int(image_font.getlength(text=image_text))
                x_pos = int((fight_image.width - text_length) / 2)

                image_draw.text(xy=(x_pos, 48), text=image_text, fill=(255, 255, 255), font=image_font, stroke_width=4, stroke_fill=(0, 0, 0))

                image_path.append(await self.save_image(image=fight_image))

        elif image_info == "idle":
            image_path.append(await self.save_image(image=self.fight_images[image]))

        elif image_info.startswith("winner"):
            fight_image = self.fight_images[image].copy()
            image_draw = ImageDraw.Draw(im=fight_image)
            image_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=64)

            if image_info.endswith("left"):
                image_draw.text(xy=(56, 48), text="WINNER", fill=(0, 255, 0), font=image_font, stroke_width=2, stroke_fill=(0, 0, 0))
                image_draw.text(xy=(444, 48), text="LOSER", fill=(255, 0, 0), font=image_font, stroke_width=2, stroke_fill=(0, 0, 0))
            else:
                image_draw.text(xy=(424, 48), text="WINNER", fill=(0, 255, 0), font=image_font, stroke_width=2, stroke_fill=(0, 0, 0))
                image_draw.text(xy=(68, 48), text="LOSER", fill=(255, 0, 0), font=image_font, stroke_width=2, stroke_fill=(0, 0, 0)) 
            
            image_path.append(await self.save_image(image=fight_image))

        else:
            fight_image = self.fight_images[image].copy()
            font_size = 64
            text_color = (0, 255, 0)

            if image_variant:
                font_size = 80
                text_color = (255, 0, 0)
            
            image_draw = ImageDraw.Draw(im=fight_image)
            image_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)

            text_length = int(image_font.getlength(text=image_info))
            x_pos = int((fight_image.width - text_length) / 2)

            image_draw.text(xy=(x_pos, 48), text=image_info, fill=text_color, font=image_font, stroke_width=2, stroke_fill=(0, 0, 0))

            image_path.append(await self.save_image(image=fight_image))

        return image_path

    async def get_stats_image(self, remaining_left_health: int = None, remaining_right_heath: int = None) -> str:
        if remaining_left_health == None or remaining_right_heath == None:
            left_health = self.fighter_one.health.get_health()
            right_health = self.fighter_two.health.get_health()
        else:
            left_health = remaining_left_health
            right_health = remaining_right_heath

        left_bar = await Bar.get_longbar(act_val=left_health, max_val=self.fighter_one.health.get_health())
        right_bar = await Bar.get_longbar(act_val=right_health, max_val=self.fighter_two.health.get_health())

        left_percentage = int((left_health / self.fighter_one.health.get_health()) * 100)
        right_percentage = int((right_health / self.fighter_two.health.get_health()) * 100)

        stats_image = self.stats_image.copy()
        stats_draw = ImageDraw.Draw(im=stats_image)
        stats_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=64)

        stats_draw.text(xy=(32, 8), text=f"{left_bar}", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))
        stats_draw.text(xy=(416, 8), text=f"{right_bar}", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))

        stats_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=48)

        x_pos = 0
        if right_percentage < 100 and right_percentage >= 10:
            x_pos = 18
        elif right_percentage < 10:
            x_pos = 36

        if left_percentage < 0:
            left_percentage = 0
        if right_percentage < 0:
            right_percentage = 0

        stats_draw.text(xy=(196, 16), text=f"({left_percentage}%)", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))
        stats_draw.text(xy=(320 + x_pos, 16), text=f"({right_percentage}%)", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))

        return await self.save_image(image=stats_image)

    async def render_fight(self) -> None:
        fighter_left = await self.render_player(is_left=True)
        fighter_left_name = await self.render_name(name=self.fighter_one.get_name())

        if isinstance(self.fighter_two, Player):
            fighter_right = await self.render_player(is_left=False)
            fighter_right_name = await self.render_name(name=self.fighter_two.get_name())
        else:
            fighter_right = await self.render_monster()
            fighter_right_name = await self.render_name(name=self.fighter_two.get_name())

        idle = Image.open(fp=Renderer.BG2_PATH)
        fighter_left_att_miss = Image.open(fp=Renderer.BG2_PATH)
        fighter_left_att_hit = Image.open(fp=Renderer.BG2_PATH)
        fighter_right_att_miss = Image.open(fp=Renderer.BG2_PATH)
        fighter_right_att_hit = Image.open(fp=Renderer.BG2_PATH)
        fighter_left_dead = Image.open(fp=Renderer.BG2_PATH)
        fighter_right_dead = Image.open(fp=Renderer.BG2_PATH)

        idle.paste(im=fighter_left[0], box=(8, 64), mask=fighter_left[0])
        idle.paste(im=fighter_right[0], box=(248, 64), mask=fighter_right[0])

        fighter_left_att_hit.paste(im=fighter_right[3], box=(248, 64), mask=fighter_right[3])
        fighter_left_att_hit.paste(im=fighter_left[1], box=(136, 64), mask=fighter_left[1])

        fighter_left_att_miss.paste(im=fighter_right[2], box=(248, 64), mask=fighter_right[2])
        fighter_left_att_miss.paste(im=fighter_left[1], box=(136, 64), mask=fighter_left[1])

        fighter_right_att_hit.paste(im=fighter_left[3], box=(8, 64), mask=fighter_left[3])
        fighter_right_att_hit.paste(im=fighter_right[1], box=(120, 64), mask=fighter_right[1])

        fighter_right_att_miss.paste(im=fighter_left[2], box=(8, 64), mask=fighter_left[2])
        fighter_right_att_miss.paste(im=fighter_right[1], box=(120, 64), mask=fighter_right[1])

        fighter_left_dead.paste(im=fighter_left[4], box=(8, 96), mask=fighter_left[4])
        fighter_left_dead.paste(im=fighter_right[0], box=(248, 64), mask=fighter_right[0])

        fighter_right_dead.paste(im=fighter_left[0], box=(8, 64), mask=fighter_left[0])
        fighter_right_dead.paste(im=fighter_right[4], box=(248, 96), mask=fighter_right[4])

        self.fight_images[0] = idle
        self.fight_images[1] = fighter_left_att_hit
        self.fight_images[2] = fighter_left_att_miss
        self.fight_images[3] = fighter_right_att_hit
        self.fight_images[4] = fighter_right_att_miss
        self.fight_images[5] = fighter_right_dead
        self.fight_images[6] = fighter_left_dead

        # Paste rendered names to images
        for image in self.fight_images.values():
            image.paste(im=fighter_left_name, box=(8, 0), mask=fighter_left_name)
            image.paste(im=fighter_right_name, box=(376, 0), mask=fighter_right_name)
    
    async def render_stats(self) -> Image.Image:
        stats_image = Image.open(fp=Renderer.BG3_PATH)
        stats_draw = ImageDraw.Draw(im=stats_image)
        stats_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=48)

        fighters = list()
        fighters.append(self.fighter_one)
        fighters.append(self.fighter_two)

        x_pos = 0
        for fighter in fighters:
            fighter: Character = fighter

            level = fighter.level.get_lvl()
            stats_draw.text(xy=(32 + x_pos, 64), text="LEVEL", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))
            stats_draw.text(xy=(176 + x_pos, 64), text=str(level), fill=(0, 255, 0), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))

            attack = fighter.attack.get_lvl()               
            stats_draw.text(xy=(32 + x_pos, 112), text="ATTACK", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))
            stats_draw.text(xy=(176 + x_pos, 112), text=str(attack), fill=(0, 255, 0), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))

            defense = fighter.defense.get_lvl()
            stats_draw.text(xy=(32 + x_pos, 160), text="DEFENSE", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))
            stats_draw.text(xy=(176 + x_pos, 160), text=str(defense), fill=(0, 255, 0), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))

            health = fighter.health.get_lvl()
            stats_draw.text(xy=(32 + x_pos, 208), text="HEALTH", fill=(255, 255, 255), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))
            stats_draw.text(xy=(176 + x_pos, 208), text=str(health), fill=(0, 255, 0), font=stats_font, stroke_width=1, stroke_fill=(0, 0, 0))

            x_pos += 384

        self.stats_image = stats_image

    async def render_player(self, is_left: bool) -> dict[int, Image.Image]:
        player_images: dict[int, Image.Image] = dict()

        for i in range(5):
            image = Image.new(mode="RGBA", size=(384, 256), color=(0, 0, 0, 0))

            if is_left:
                player = self.fighter_one
            else:
                player = self.fighter_two

            char = Image.open(fp=Renderer.PLAYER_PATH % (player.color.value, i))

            x_hit_pos = 0
            if i == 3: # Hit image
                x_hit_pos = 8

            if player.equipment.sword and i != 4:
                sword = Image.open(fp=Renderer.SWORD_PATH % player.equipment.sword.tier.value)
                if i == 1: # Attack image
                    sword = sword.rotate(angle=-45, expand=True)
                    image.paste(im=sword, box=(132, 8), mask=sword)
                else:
                    image.paste(im=sword, box=(148, 8 + x_hit_pos), mask=sword)

            if i == 4: # Dead image
                image.paste(im=char, box=(48, -40), mask=char)
            else:
                image.paste(im=char, box=(-16, 0), mask=char)

            if player.equipment.head:
                head = Image.open(fp=Renderer.HEAD_PATH % player.equipment.head.tier.value)
                if i == 4: # Dead image
                    head = head.rotate(angle=90, expand=True)
                    image.paste(im=head, box=(-8, 24), mask=head)
                else: 
                    image.paste(im=head, box=(-16, 0 + x_hit_pos), mask=head)

            if player.equipment.body:
                body = Image.open(fp=Renderer.BODY_PATH % player.equipment.body.tier.value)
                if i == 4: # Dead image
                    body = body.rotate(angle=90, expand=True)
                    image.paste(im=body, box=(-8, 24), mask=body)
                else: 
                    image.paste(im=body, box=(-16, 0 + x_hit_pos), mask=body)

            if player.equipment.shield and i != 4:
                shield = Image.open(fp=Renderer.SHIELD_PATH % player.equipment.shield.tier.value)
                if i == 2: # Defense image
                    image.paste(im=shield, box=(116, 116), mask=shield)
                else:
                    image.paste(im=shield, box=(-12, 124 + x_hit_pos), mask=shield)

            if is_left:
                player_images[i] = image
            else:
                player_images[i] = ImageOps.mirror(image)

        return player_images
    
    async def render_monster(self) -> dict[int, Image.Image]:
        monster_images: dict[int, Image.Image] = dict()

        monster: Monster = self.fighter_two
        monster_rank = 0
        if monster.rank == EnemyRank.LIGHT:
            monster_rank = 1
        elif monster.rank == EnemyRank.MEDIUM:
            monster_rank = 2
        elif monster.rank == EnemyRank.HEAVY:
            monster_rank = 3

        for i in range(5):
            image = Image.new(mode="RGBA", size=(384, 256), color=(0, 0, 0, 0))
            monster_image  = Image.open(fp=Renderer.MONSTER_PATH % (monster_rank, i))
            image.paste(im=monster_image, box=(128, 0), mask=monster_image)
            monster_images[i] = image
        
        return monster_images
   
    async def render_name(self, name: str) -> Image.Image:
        font_size = 64

        name_image = Image.new(mode="RGBA", size=(256, 64), color=(0, 0, 0, 0))
        name_draw = ImageDraw.Draw(im=name_image)
        name_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)
        
        name_length = int(name_font.getlength(text=name))

        while name_length > 240:
            font_size -= 4
            name_font = ImageFont.truetype(font=Renderer.FONT_PATH, size=font_size)
            name_length = int(name_font.getlength(text=name))

        x = int((name_image.width - name_length) / 2)
        y = int((name_image.height - font_size) / 2 + 4)

        name_draw.text(xy=(x, y), text=name, fill=(255, 255, 255), font=name_font, stroke_width=2, stroke_fill=(0, 0, 0))
        
        return name_image