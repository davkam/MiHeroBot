# -*- coding: ISO-8859-15 -*-

from tools.tools import Bar, StringManager
from game.objects.characters import Character, Monster, Player, MonsterClass
from images.image_links import ImageLinks
from log.logger import Logger
import random

class Combat():
    def __init__ (self, objA: Player, objB: Character):
        self.objA: Combatant = Combatant(objA)
        self.objB: Combatant = Combatant(objB)
        self.notes: list[str] = list()
        self.images: list[str] = ImageLinks.instance.links
        self.log: Logger = Logger.combat_logger

    async def set_stats(self):
        await self.objA.combat_stats()
        await self.objB.combat_stats()
        await self.objA.comparative_stats(combatant = self.objB)
        await self.objB.comparative_stats(combatant = self.objA)

    async def run_combat(self):
        await self.pre_combat()
        await self.main_combat()
        await self.post_combat()

    async def pre_combat(self):
        pvp_idle = self.images[0]
        pvm_idle = self.images[5]

        if type(self.objB.character) == Monster:
            objA: Player = self.objA.character
            objB: Monster = self.objB.character

            self.notes += [pvm_idle]
            self.notes.append([objA.get_name(), objA.lvl.get_lvl(), objA.attack.get_lvl(), objA.defense.get_lvl(), objA.health.get_hp()])
            self.notes.append([objB.get_name(), objB.lvl.get_lvl(), objB.attack.get_lvl(), objB.defense.get_lvl(), objB.health.get_hp()])
            self.notes.append([f"\U00002694\uFE0F WEAPON:\nLVL.{objA.weapon.attack.get_lvl()} {objA.weapon.weapon_class.name}", f"\U0001F6E1\uFE0F ARMOR:\nLVL.{objA.armor.defense.get_lvl()} {objA.armor.armor_class.name.upper()}"])
            self.notes.append([f"\U0001F47E MONSTER: {objB.monster_class.name}", ""])
        else:
            objA: Player = self.objA.character
            objB: Player = self.objB.character

            self.notes += [pvp_idle]
            self.notes.append([objA.get_name(), objA.lvl.get_lvl(), objA.attack.get_lvl(), objA.defense.get_lvl(), objA.health.get_hp()])
            self.notes.append([objB.get_name(), objB.lvl.get_lvl(), objB.attack.get_lvl(), objB.defense.get_lvl(), objB.health.get_hp()])
            self.notes.append([f"\U00002694\uFE0F WEAPON:\nLVL.{objA.weapon.attack.get_lvl()} {objA.weapon.weapon_class.name}", f"\U0001F6E1\uFE0F ARMOR:\nLVL.{objA.armor.defense.get_lvl()} {objA.armor.armor_class.name.upper()}"])
            self.notes.append([f"\U00002694\uFE0F WEAPON:\nLVL.{objB.weapon.attack.get_lvl()} {objB.weapon.weapon_class.name}", f"`\U0001F6E1\uFE0F ARMOR:\nLVL.{objB.armor.defense.get_lvl()} {objB.armor.armor_class.name.upper()}`"])

    async def main_combat(self):
        pvp_hitA = self.images[1]
        pvp_hitB = self.images[2]
        pvm_hitA = self.images[6]
        pvm_hitB = self.images[7]

        if type(self.objB.character) == Monster:
            turn = True
        else:
            rng = random.randint(0, 1000)
            if rng < 500: turn = True
            else: turn = False

        while self.objA.hp > 0 and self.objB.hp > 0:
            if turn == True:
                rng = random.randint(0, 1000)
                if rng <= self.objA.acc:
                    rng = random.randint(500, 1500) / 1000
                    hit = self.objA.base_att + (self.objA.base_att * self.objA.att_acc * rng)

                    rng = random.randint(500, 1500) / 1000
                    block = self.objB.base_def + (self.objB.base_def * self.objB.def_acc * rng)

                    dmg = round((hit * 100) / (block + 100))
                    self.objB.hp -= dmg

                    hit_log = await StringManager.center_string(string = f"CRIT HIT: {dmg}", max_length = 20)
                else:
                    rng = random.randint(0, 500) / 1000
                    hit = self.objA.base_att * rng

                    rng = random.randint(0, 500) / 1000
                    block = self.objB.base_def * rng

                    dmg = round((hit * 100) / (block + 100))
                    self.objB.hp -= dmg

                    hit_log = await StringManager.center_string(string = f"BLUNT HIT: {dmg}", max_length = 20)

                hp_barA = await Bar.get_bar(self.objA.hp, self.objA.max_hp)
                hp_barB = await Bar.get_bar(self.objB.hp, self.objB.max_hp)
                hp_percA = round((self.objA.hp / self.objA.max_hp) * 100)
                hp_percB = round((self.objB.hp / self.objB.max_hp) * 100)

                if type(self.objB.character) == Monster:
                    self.notes += [pvm_hitA]
                else:
                    self.notes += [pvp_hitA]

                self.notes += [hit_log]
                self.notes.append([hp_barA, hp_percA])
                self.notes.append([hp_barB, hp_percB])

                turn = False
            else:
                rng = random.randint(0, 1000)
                if rng <= self.objB.acc:
                    rng = random.randint(500, 1500) / 1000
                    hit = self.objB.base_att + (self.objB.base_att * self.objB.att_acc * rng)

                    rng = random.randint(500, 1500) / 1000
                    block = self.objA.base_def + (self.objA.base_def * self.objA.def_acc * rng)

                    dmg = round((hit * 100) / (block + 100))
                    self.objA.hp -= dmg

                    hit_log = await StringManager.center_string(string = f"CRIT HIT: {dmg}", max_length = 20)
                else:
                    rng = random.randint(0, 500) / 1000
                    hit = self.objB.base_att * rng

                    rng = random.randint(0, 500) / 1000
                    block = self.objA.base_def * rng

                    dmg = round((hit * 100) / (block + 100))
                    self.objA.hp -= dmg

                    hit_log = await StringManager.center_string(string = f"BLUNT HIT: {dmg}", max_length = 20)

                hp_barA = await Bar.get_bar(self.objA.hp, self.objA.max_hp)
                hp_barB = await Bar.get_bar(self.objB.hp, self.objB.max_hp)
                hp_percA = round((self.objA.hp / self.objA.max_hp) * 100)
                hp_percB = round((self.objB.hp / self.objB.max_hp) * 100)

                if type(self.objB.character) == Monster:
                    self.notes += [pvm_hitB]
                else:
                    self.notes += [pvp_hitB]

                self.notes += [hit_log]
                self.notes.append([hp_barA, hp_percA])
                self.notes.append([hp_barB, hp_percB])

                turn = True

    async def post_combat(self):
        pvp_deadA = self.images[3]
        pvp_deadB = self.images[4]
        pvm_deadA = self.images[8]
        pvm_deadB = self.images[9]

        winner: Character
        loser: Character

        # Setting winner, loser and log according to outcome.
        if self.objA.hp <= 0:
            winner = self.objB.character
            loser = self.objA.character

            if type(self.objB.character) == Monster:
                self.notes += [pvm_deadA]
            else:
                self.notes += [pvp_deadA]

            w_name = await StringManager.center_string(string = winner.get_name(), max_length = 20)
            l_name = await StringManager.center_string(string = loser.get_name(), max_length = 20)
            self.notes.append([w_name, l_name])
        else:
            winner = self.objA.character
            loser = self.objB.character

            if type(self.objB.character) == Monster:
                self.notes += [pvm_deadB]
            else:
                self.notes += [pvp_deadB]
            
            w_name = await StringManager.center_string(string = winner.get_name(), max_length = 20)
            l_name = await StringManager.center_string(string = loser.get_name(), max_length = 20)
            self.notes.append([w_name, l_name])

        await self.log.write_log(log_data=f"{self.objA.character.name} initiated combat with {self.objB.character.name}. WINNER: {winner.name}, LOSER: {loser.name}")

        # Setting outcome according to winner/loser types.
        if type(winner) == Player and type(loser) == Monster:
            self.notes += [f"**{winner.get_name()}** `looks around to find something valuable...`"]
            if loser.monster_class == MonsterClass.LIGHT:
                xp_log = await winner.xp_gainer(xp_index=1)
                self.notes.append(xp_log)
                rng = random.randint(0, 1000)
                if rng <= 500:
                    loot_log = await winner.loot_generator(loot_index=1)
                    self.notes.append(loot_log)
                else:
                    self.notes += ["NONE"]
            elif loser.monster_class == MonsterClass.MEDIUM:
                xp_log = await winner.xp_gainer(xp_index=2)
                self.notes.append(xp_log)
                rng = random.randint(0, 1000)
                if rng <= 750:
                    loot_log = await winner.loot_generator(loot_index=2)
                    self.notes.append(loot_log)
                else:
                    self.notes += ["NONE"]
            else: # loser.monster_class == MonsterClass.Heavy
                xp_log = await winner.xp_gainer(xp_index=3)
                loot_log = await winner.loot_generator(loot_index=3)
                self.notes.append(xp_log)
                self.notes.append(loot_log)
        elif type(winner) == Player and type(loser) == Player:
            if loser.gold > 0:
                rng = random.randint(250, 500) / 1000
                gold = round(loser.gold * rng)
                loser.gold -= gold
                winner.gold += gold

                self.notes += [f"**{winner.get_name()}** `looks around and steals` **{gold}** `gold from` **{loser.get_name()}**"]
            else:
                # TBD: Code to add/remove weapon.
                self.notes += [f"**{winner.get_name()}** `looks around and finds no gold.`\n**{winner.get_name()}** `takes` **{loser.get_name()}'s** `weapon instead.`"]
            self.notes += ["NONE"]
            self.notes += ["NONE"]
        else: # type(winner) == Monster and type(loser) == Player.
            if loser.gold > 0:
                rng = random.randint(0, 250) / 1000
                gold = round(loser.gold * rng)
                loser.gold -= gold

                self.notes += [f"**{loser.get_name()}** `stumbles away and loses` **{gold}** `gold...`"]
            else:
                self.notes += [f"**{loser.get_name()}** `stumbles away from the battle...`"]
            self.notes += ["NONE"]
            self.notes += ["NONE"]

class Combatant():
    def __init__(self, character: Character):
        self.character: Character = character

    async def combat_stats(self):
        if type(self.character) == Player:
            self.base_att = round((10 * self.character.attack.get_lvl() + self.character.weapon.weapon_class.value * self.character.weapon.attack.get_lvl() / 2 ), 2)
            self.att_acc = round((1 / 100) * (5 * self.character.attack.get_lvl() + self.character.weapon.weapon_class.value * self.character.weapon.attack.get_lvl()), 4)
            self.base_def = round((1 / 5) * (10 * self.character.defense.get_lvl() + self.character.armor.armor_class.value * self.character.armor.defense.get_lvl() / 2), 2)
            self.def_acc = round((1 / 500) * (5 * self.character.defense.get_lvl() + self.character.armor.armor_class.value * self.character.armor.defense.get_lvl()), 4)
            self.max_hp = self.character.health.get_hp()
            self.hp = self.max_hp
        elif type(self.character) == Monster:
            self.base_att = round((10 * self.character.attack.get_lvl() + self.character.monster_class.value * self.character.attack.get_lvl() / 2), 2)
            self.att_acc = round((1 / 100) * (5 * self.character.attack.get_lvl() + self.character.monster_class.value * self.character.attack.get_lvl()), 4)
            self.base_def = round((1 / 5) * (10 * self.character.defense.get_lvl() + self.character.monster_class.value * self.character.defense.get_lvl() / 2), 2)
            self.def_acc = round((1 / 500) * (5 * self.character.defense.get_lvl() + self.character.monster_class.value * self.character.defense.get_lvl()), 4)
            self.max_hp = self.character.health.get_hp()
            self.hp = self.max_hp

    async def comparative_stats(self, combatant):
        combatant: Combatant = combatant
        self.acc = round((self.att_acc / combatant.def_acc) * 100)
        self.inacc = round((combatant.def_acc / self.att_acc) * 100) # Not needed!