import random

from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player
from game.objects.items.items import Item

class Rewards():
    __slots__ = ['winner', 'loser']

    def __init__(self, winner: Character, loser: Character) -> None:
        self.winner: Character = winner
        self.loser: Character = loser
    
    async def pvm_rewards(self) -> tuple[list[int], tuple[int, list[Item], bool], int]:
        xp_gain: list[int] = list()
        loot_gain: list[Item] = list()
        gold_lost = int()

        if isinstance(self.winner, Player) and isinstance(self.loser, Monster):
            if self.loser.rank == EnemyRank.LIGHT:
                xp_gain = await self.run_xp_generator(xp_index=1)

                if random.randint(0, 1000) < 750:
                    loot_gain = await self.run_loot_generator(loot_index=1)
            elif self.loser.rank == EnemyRank.MEDIUM:
                xp_gain = await self.run_xp_generator(xp_index=2)
                loot_gain = await self.run_loot_generator(loot_index=2)
            else:
                xp_gain = await self.run_xp_generator(xp_index=3)
                loot_gain = await self.run_loot_generator(loot_index=3)
        else:
            pass

        return xp_gain, loot_gain, gold_lost

    async def pvp_rewards(self) -> None:
        pass

    async def run_xp_generator(self, xp_index: int) -> list[int]:
        # Set rng variables according to index
        if xp_index == 1: min = 1000; max = 2500; multiplier = 10
        elif xp_index == 2: min = 2500; max = 5000; multiplier = 25
        else: min = 5000; max = 10000; multiplier = 50

        # Set experience gains randomly according to rng variables
        lvl = self.winner.level.get_lvl()
        rng_xp = random.randint(min, max)
        att_gain = int(rng_xp + (lvl ** 1.5) * multiplier)
        rng_xp = random.randint(min, max)
        def_gain = int(rng_xp + (lvl ** 1.5) * multiplier)
        rng_xp = random.randint(min, max)
        hp_gain = int(rng_xp + (lvl ** 1.5) * multiplier)

        self.winner.attack.add_xp(value=att_gain)
        self.winner.defense.add_xp(value=def_gain)
        self.winner.health.add_xp(value=hp_gain)
        self.winner.level.update_lvl()

        xp_gain = [att_gain, def_gain, hp_gain]

        return xp_gain

    async def run_loot_generator(self, loot_index: int) -> tuple[int, list[Item], bool]:
        self.winner: Player = self.winner

        loot_roll = None    # Determine amount of times to roll for loot
        loot_equips = None  # Determine amount of equipables allowed in loot rolls
        
        # Set loot variables and gold according to loot index
        if loot_index == 1:
            gold = random.randint(500, 1000)
            loot_roll = random.randint(1, 3)
            loot_equips = 1
        elif loot_index == 2:
            gold = random.randint(1000, 2000)
            loot_roll = random.randint(2, 4)
            loot_equips = random.randint(1, 2)
        elif loot_index == 3:
            gold = random.randint(2000, 4000)
            loot_roll = random.randint(3, 5)
            loot_equips = random.randint(1, 3)

        self.winner.gold += gold
        attack = self.winner.attack.get_lvl()
        defense = self.winner.defense.get_lvl()
        health = self.winner.health.get_lvl()
        avg_stats = round((attack + defense + health) / 3, 2)

        inv_full = await self.winner.inventory.check_inv_space()

        if inv_full:
            return gold, None, inv_full

        loot_gain: list[Item] = list()
        item = Item()
        while loot_roll > 0:
            if loot_equips > 0:
                equips_enabled = True
                loot_equips -= 1
            else:
                equips_enabled = False

            random_item = await item.get_random_item(item_index=loot_index, equips_allowed=equips_enabled, avg_stats=avg_stats)
            loot_gain.append(random_item)
            loot_roll -= 1

            if not self.winner.inventory.add_item(item=random_item):
                pass

        return gold, loot_gain, inv_full