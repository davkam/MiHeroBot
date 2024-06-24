import logging
import random

from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player
from loggers.loggers import Loggers

class Fight():
    def __init__ (self, fighter_a: Player, fighter_b: Character) -> None:
        self.fighter_a: Fighter = Fighter(fighter_a)
        self.fighter_b: Fighter = Fighter(fighter_b)
        self.turn: bool = None # Decide turn, True = fighter A turn, False = fighter B turn
        self.logger: logging.Logger = Loggers.game

    async def set_stats(self) -> None:
        await self.fighter_a.fight_stats()
        await self.fighter_b.fight_stats()
        await self.fighter_a.relative_stats(opponent=self.fighter_b)
        await self.fighter_b.relative_stats(opponent=self.fighter_a)

    async def set_turn(self):
        if isinstance(self.fighter_b.character, Monster):
            self.turn = True
        else:
            rng = random.randint(0, 1000)
            if rng < 500:
                self.turn = True
            else:
                self.turn = False

    async def fight_turn(self) -> tuple[bool, int]:
        if self.turn:
            att_fighter = self.fighter_a
            def_fighter = self.fighter_b

            self.turn = False
        else:
            att_fighter = self.fighter_b
            def_fighter = self.fighter_a

            self.turn = True
     
        return await att_fighter.attack_opponent(opponent=def_fighter) 

class Fighter():
    def __init__(self, character: Character) -> None:
        self.character: Character = character

    async def fight_stats(self) -> None:
        if isinstance(self.character, Player):
            offensive_bonus = 0
            if self.character.equipment.sword:
                offensive_bonus += round(0.8 * (self.character.equipment.sword.tier.value * self.character.equipment.sword.level.get_lvl()), 2)
            if self.character.equipment.amulet:
                offensive_bonus += round(0.2 * (self.character.equipment.amulet.tier.value * self.character.equipment.amulet.level.get_lvl()), 2)

            defensive_bonus = 0
            if self.character.equipment.shield:
                defensive_bonus += round(0.6 * (self.character.equipment.shield.tier.value * self.character.equipment.shield.level.get_lvl()), 2)
            if self.character.equipment.head:
                defensive_bonus += round(0.2 * (self.character.equipment.head.tier.value * self.character.equipment.head.level.get_lvl()), 2)
            if self.character.equipment.body:
                defensive_bonus += round(0.2 * (self.character.equipment.body.tier.value * self.character.equipment.body.level.get_lvl()), 2)
            
            self.base_att = round((10 * self.character.attack.get_lvl() + offensive_bonus / 2 ), 2)
            self.att_acc = round((1 / 100) * (5 * self.character.attack.get_lvl() + offensive_bonus), 4)
            self.base_def = round((1 / 5) * (10 * self.character.defense.get_lvl() + defensive_bonus / 2), 2)
            self.def_acc = round((1 / 500) * (5 * self.character.defense.get_lvl() + defensive_bonus), 4)
            self.max_hp = self.character.health.get_health()
            self.hp = self.max_hp

        elif isinstance(self.character, Monster):
            self.base_att = round((10 * self.character.attack.get_lvl() + self.character.rank.value * self.character.attack.get_lvl() / 2), 2)
            self.att_acc = round((1 / 100) * (5 * self.character.attack.get_lvl() + self.character.rank.value * self.character.attack.get_lvl()), 4)
            self.base_def = round((1 / 5) * (10 * self.character.defense.get_lvl() + self.character.rank.value * self.character.defense.get_lvl() / 4), 2)
            self.def_acc = round((1 / 500) * (5 * self.character.defense.get_lvl() + self.character.rank.value * self.character.defense.get_lvl() / 2), 4)
            self.max_hp = self.character.health.get_health()
            self.hp = self.max_hp

    async def relative_stats(self, opponent) -> None:
        opponent: Fighter = opponent
        self.acc = round((self.att_acc / opponent.def_acc) * 100)
        self.inacc = round((opponent.def_acc / self.att_acc) * 100) # Not needed!

    async def attack_opponent(self, opponent) -> tuple[bool, int]:
        opponent: Fighter = opponent
        att_dmg: int = 0
        hit: bool = None

        rng = random.randint(0, 1000)
        if rng <= self.acc:
            rng = random.randint(500, 1500) / 1000
            hit = self.base_att + (self.base_att * self.att_acc * rng)

            rng = random.randint(500, 1500) / 1000
            block = opponent.base_def + (opponent.base_def * opponent.def_acc * rng)

            att_dmg = round((hit * 100) / (block + 100))
            opponent.hp -= att_dmg
            hit = True
        else:
            rng = random.randint(0, 500) / 1000
            hit = self.base_att * rng

            rng = random.randint(0, 500) / 1000
            block = opponent.base_def * rng

            att_dmg = round((hit * 100) / (block + 100))
            opponent.hp -= att_dmg
            hit = False
        
        return hit, att_dmg