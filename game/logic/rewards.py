import random

from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player
from game.objects.items.items import Item

class Rewards():
    def __init__(self, winner: Character, loser: Character) -> None:
        self.winner: Character = winner
        self.loser: Character = loser
    
    async def pvm_rewards(self) -> tuple[list[int], list[Item], int]:
        xp_gain: list[int] = list()
        loot_gain: list[Item] = list()
        gold_lost = int()

        if isinstance(self.winner, Player) and isinstance(self.loser, Monster):
            if self.loser.rank == EnemyRank.LIGHT:
                xp_gain = await self.run_xp_generator(xp_index=1)

                if random.randint(0, 1000) < 500:
                    loot_gain = await self.run_loot_generator(loot_index=1)
            elif self.loser.rank == EnemyRank.MEDIUM:
                xp_gain = await self.run_xp_generator(xp_index=2)

                if random.randint(0, 1000) < 750:
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

    async def run_loot_generator(self, loot_index: int) -> list[Item]:
        loot_gain = list()
        return loot_gain