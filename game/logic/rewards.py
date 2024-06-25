import random

from game.objects.characters.characters import Character
from game.objects.characters.enemies import Monster, EnemyRank
from game.objects.characters.players import Player

class Rewards():
    def __init__(self, winner: Character, loser: Character) -> None:
        self.winner: Character = winner
        self.loser: Character = loser
    
    async def pvm_rewards(self) -> None:
        if isinstance(self.winner, Player) and isinstance(self.loser, Monster):
            if self.loser.rank == EnemyRank.LIGHT:
                await self.run_xp_generator(xp_index=1)

                if random.randint(0, 1000) < 500:
                    await self.run_loot_generator(loot_index=1)
            elif self.loser.rank == EnemyRank.MEDIUM:
                await self.run_xp_generator(xp_index=2)

                if random.randint(0, 1000) < 750:
                    await self.run_loot_generator(loot_index=2)
            else:
                await self.run_xp_generator(xp_index=3)
                await self.run_loot_generator(loot_index=3)

        else:
            pass

    async def pvp_rewards(self) -> None:
        pass

    async def run_xp_generator(self, xp_index: int) -> None:
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

    async def run_loot_generator(self, loot_index: int) -> None:
        pass