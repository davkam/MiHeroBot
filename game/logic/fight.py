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
        await self.fighter_a.set_fighter_stats()
        await self.fighter_b.set_fighter_stats()
        await self.fighter_a.set_fighter_hit_chance(opponent_fighter=self.fighter_b)
        await self.fighter_b.set_fighter_hit_chance(opponent_fighter=self.fighter_a)

    async def set_turn(self) -> None:
        if isinstance(self.fighter_b.character, Monster):
            self.turn = True
        else:
            rng = random.randint(0, 1000)
            if rng < 500:
                self.turn = True
            else:
                self.turn = False

    async def roll_fight(self) -> tuple[bool, int]:
        if self.turn:
            att_fighter = self.fighter_a
            def_fighter = self.fighter_b

            self.turn = False
        else:
            att_fighter = self.fighter_b
            def_fighter = self.fighter_a

            self.turn = True
     
        return await att_fighter.attack_fighter(fighter=def_fighter) 

class Fighter():
    def __init__(self, character: Character) -> None:
        self.character: Character = character

    async def set_fighter_stats(self) -> None:
        if isinstance(self.character, Player):
            offensive_bonus = 0 # min: 1 -> max: 800
            if self.character.equipment.sword:
                offensive_bonus += max(1, round(0.6 * (self.character.equipment.sword.tier.value * (self.character.equipment.sword.level.get_lvl() / 2)), 2))
            if self.character.equipment.amulet:
                offensive_bonus += max(1, round(0.2 * (self.character.equipment.amulet.tier.value * (self.character.equipment.amulet.level.get_lvl() / 2)), 2))
            if self.character.equipment.ring:
                offensive_bonus += max(1, round(0.2 * (self.character.equipment.ring.tier.value * (self.character.equipment.ring.level.get_lvl() / 2)), 2))

            defensive_bonus = 0 # min: 1 -> max: 800
            if self.character.equipment.shield:
                defensive_bonus += max(1, round(0.6 * (self.character.equipment.shield.tier.value * (self.character.equipment.shield.level.get_lvl() / 2)), 2))
            if self.character.equipment.head:
                defensive_bonus += max(1, round(0.2 * (self.character.equipment.head.tier.value * (self.character.equipment.head.level.get_lvl() / 2)), 2))
            if self.character.equipment.body:
                defensive_bonus += max(1, round(0.2 * (self.character.equipment.body.tier.value * (self.character.equipment.body.level.get_lvl() / 2)), 2))

            self.base_hit = round(((2 * self.character.attack.get_lvl()) * ((offensive_bonus + 1200) / 2)) / 100) # min: 12 -> max: 2,000
            self.att_roll = round(self.character.attack.get_lvl() * ((offensive_bonus + 1200) / 2)) # min: 600 -> max: 100,000
            self.def_roll = round(self.character.defense.get_lvl() * ((defensive_bonus +1200) / 2)) # min: 600 -> max: 100,000
            self.max_hp = self.character.health.get_health() # min: 100 -> max: 10,000
            self.hp = self.max_hp

            self.base_hit += offensive_bonus * 2
            self.att_roll += round(offensive_bonus * 100)
            self.def_roll += round(defensive_bonus * 100)

        elif isinstance(self.character, Monster):
            offensive_bonus = max(1, round(self.character.rank.value * (self.character.attack.get_lvl() / 2), 2))
            defensive_bonus = max(1, round(self.character.rank.value * (self.character.defense.get_lvl() / 2), 2))

            self.base_hit = round(((2 * self.character.attack.get_lvl()) * ((offensive_bonus + 1200) / 2)) / 100) # min: 12 -> max: 2,000
            self.att_roll = round(self.character.attack.get_lvl() * ((offensive_bonus + 1200) / 2)) # min: 600 -> max: 100,000
            self.def_roll = round(self.character.defense.get_lvl() * ((offensive_bonus + 1200) / 2)) # min: 600 -> max: 100,000
            self.max_hp = self.character.health.get_health() # min: 100 -> max: 10,000
            self.hp = self.max_hp

            self.base_hit += offensive_bonus * 2
            self.att_roll += round(offensive_bonus * 100)
            self.def_roll += round(defensive_bonus * 100)

    async def set_fighter_hit_chance(self, opponent_fighter) -> None:
        opponent_fighter: Fighter = opponent_fighter

        if self.att_roll > opponent_fighter.def_roll:
            self.hit_chance = round(1 - (opponent_fighter.def_roll + 2) / (2 * self.att_roll + 1), 2)
        else:
            self.hit_chance = round(self.att_roll / (2 * opponent_fighter.def_roll + 1), 2)

        print(f"{self.character.get_name()}: HIT_CHANCE: {self.hit_chance}")

    async def attack_fighter(self, fighter) -> tuple[bool, int]:
        fighter: Fighter = fighter
        is_hit: bool = None # Hit or miss
        actual_hit: int = 0

        if random.random() < self.hit_chance:
            min_hit = int(self.base_hit * 0.75)
            max_hit = int(self.base_hit * 1.25)
            actual_hit = random.randint(min_hit, max_hit)

            fighter.hp -= actual_hit
            is_hit = True
        else:
            min_hit = int(self.base_hit * 0)
            max_hit = int(self.base_hit * 0.25)
            actual_hit = random.randint(min_hit, max_hit)

            fighter.hp -= actual_hit
            is_hit = False
        
        return is_hit, actual_hit