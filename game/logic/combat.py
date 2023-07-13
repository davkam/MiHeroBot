# -*- coding: ISO-8859-15 -*-

from extras.string_manager import StringManager
from game.features.features import Features
from game.objects.characters import Character, Monster, Player
from images.image_links import ImageLinks
import random

class Combat():
    def __init__ (self, objA: Player, objB: Character):
        self.objA: Combatant = Combatant(objA)
        self.objB: Combatant = Combatant(objB)
        self.log: list[str] = list()
        self.images: list[str] = ImageLinks.instance.links

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

        if type(self.objB.character) == Player:
            objA: Player = self.objA.character
            objB: Player = self.objB.character

            self.log += [pvp_idle]
            self.log.append([objA.name, objA.lvl.get_lvl(), objA.attack.get_lvl(), objA.defense.get_lvl(), objA.health.get_hp()])
            self.log.append([objB.name, objB.lvl.get_lvl(), objB.attack.get_lvl(), objB.defense.get_lvl(), objB.health.get_hp()])
            self.log.append([f"WEP: {objA.weapon.weapon_class.name.upper()} \n   (LVL.{objA.weapon.attack.get_lvl()})", f"ARM: {objA.armor.armor_class.name.upper()} \n   (LVL.{objA.armor.defense.get_lvl()})"])
            self.log.append([f"WEP: {objB.weapon.weapon_class.name.upper()} \n   (LVL.{objB.weapon.attack.get_lvl()})", f"`ARM: {objB.armor.armor_class.name.upper()} \n   (LVL.{objB.armor.defense.get_lvl()})`"])
        else:
            objA: Player = self.objA.character
            objB: Monster = self.objB.character

            self.log += [pvm_idle]
            self.log.append([objA.name, objA.lvl.get_lvl(), objA.attack.get_lvl(), objA.defense.get_lvl(), objA.health.get_hp()])
            self.log.append([objB.name, objB.lvl.get_lvl(), objB.attack.get_lvl(), objB.defense.get_lvl(), objB.health.get_hp()])
            self.log.append([f"WEP: {objA.weapon.weapon_class.name.upper()} \n   (LVL.{objA.weapon.attack.get_lvl()})", f"ARM: {objA.armor.armor_class.name.upper()} \n   (LVL.{objA.armor.defense.get_lvl()})"])
            self.log.append([f"MONSTER: {objB.monster_class.name.upper()}", ""])

    async def main_combat(self):
        pvp_hitA = self.images[1]
        pvp_hitB = self.images[2]
        pvm_hitA = self.images[6]
        pvm_hitB = self.images[7]

        if type(self.objB.character) == Player:
            rng = random.randint(0, 1000)
            if rng < 500: turn = True
            else: turn = False
        else:
            turn = True

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

                    hit_log = await StringManager.center_string(string = f"CRITICAL HIT: {dmg}", max_length = 22)
                else:
                    rng = random.randint(0, 500) / 1000
                    hit = self.objA.base_att * rng

                    rng = random.randint(0, 500) / 1000
                    block = self.objB.base_def * rng

                    dmg = round((hit * 100) / (block + 100))
                    self.objB.hp -= dmg

                    hit_log = await StringManager.center_string(string = f"BLUNT HIT: {dmg}", max_length = 22)

                hp_barA = await Features.get_bar(self.objA.hp, self.objA.max_hp)
                hp_barB = await Features.get_bar(self.objB.hp, self.objB.max_hp)
                hp_percA = round((self.objA.hp / self.objA.max_hp) * 100)
                hp_percB = round((self.objB.hp / self.objB.max_hp) * 100)

                if type(self.objB.character) == Player:
                    self.log += [pvp_hitA]
                else:
                    self.log += [pvm_hitA]

                self.log += [hit_log]
                self.log.append([hp_barA, hp_percA])
                self.log.append([hp_barB, hp_percB])

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

                    hit_log = await StringManager.center_string(string = f"CRITICAL HIT: {dmg}", max_length = 22)
                else:
                    rng = random.randint(0, 500) / 1000
                    hit = self.objB.base_att * rng

                    rng = random.randint(0, 500) / 1000
                    block = self.objA.base_def * rng

                    dmg = round((hit * 100) / (block + 100))
                    self.objA.hp -= dmg

                    hit_log = await StringManager.center_string(string = f"BLUNT HIT: {dmg}", max_length = 22)

                hp_barA = await Features.get_bar(self.objA.hp, self.objA.max_hp)
                hp_barB = await Features.get_bar(self.objB.hp, self.objB.max_hp)
                hp_percA = round((self.objA.hp / self.objA.max_hp) * 100)
                hp_percB = round((self.objB.hp / self.objB.max_hp) * 100)

                if type(self.objB.character) == Player:
                    self.log += [pvp_hitB]
                else:
                    self.log += [pvm_hitB]

                self.log += [hit_log]
                self.log.append([hp_barA, hp_percA])
                self.log.append([hp_barB, hp_percB])

                turn = True

    async def post_combat(self):
        pvp_deadA = self.images[3]
        pvp_deadB = self.images[4]
        pvm_deadA = self.images[8]
        pvm_deadB = self.images[9]

        if self.objA.hp <= 0:
            if type(self.objB.character) == Player:
                winner: Player = self.objB.character
                loser: Player = self.objA.character

                self.log += [pvp_deadA]
                w_name = await StringManager.center_string(string = winner.name, max_length = 22)
                l_name = await StringManager.center_string(string = loser.name, max_length = 22)
                self.log.append([w_name, l_name])

                if loser.gold > 0:
                    rng = random.randint(250, 500) / 1000
                    gold = int(loser.gold * rng)
                    loser.gold -= gold
                    winner.gold += gold

                    self.log += [f"**{winner.name}** `looks around and steals` **{gold}** `gold from` **{loser.name}**"]
                    
                else:
                    # TBD: Code to add/remove weapon.

                    self.log += [f"**{winner.name}** `looks around and finds no gold.`\n**{winner.name}** `takes` **{loser.name}'s** `weapon instead.`"]
            else:
                winner: Monster = self.objB.character
                loser: Player = self.objA.character

                self.log += [pvm_deadA]
                w_name = await StringManager.center_string(string = winner.name, max_length = 22)
                l_name = await StringManager.center_string(string = loser.name, max_length = 22)
                self.log.append([w_name, l_name])
                
                if loser.gold > 0:
                    rng = random.randint(0, 250) / 1000
                    gold = int(loser.gold * rng)
                    loser.gold -= gold

                    self.log += [f"**{loser.name}** `stumbles away and loses` **{gold}** `gold...`"]
                else:
                    self.log += [f"**{loser.name}** `stumbles away from the battle...`"]
        else:
            if type(self.objB.character) == Player:
                winner: Player = self.objA.character
                loser: Player = self.objB.character

                self.log += [pvp_deadB]
                w_name = await StringManager.center_string(string = winner.name, max_length = 22)
                l_name = await StringManager.center_string(string = loser.name, max_length = 22)
                self.log.append([w_name, l_name])
                
                if loser.gold > 0:
                    rng = random.randint(250, 500) / 1000
                    gold = int(loser.gold * rng)
                    loser.gold -= gold
                    winner.gold += gold

                    self.log += [f"**{winner.name}** `looks around and steals` **{gold}** `gold from` **{loser.name}**"]
                    
                else:
                    # TBD: Code to add/remove weapon.

                    self.log += [f"**{winner.name}** `looks around and finds no gold.`\n**{winner.name}** `takes` **{loser.name}'s** `weapon instead.`"]
            else:
                winner: Player = self.objA.character
                loser: Monster = self.objB.character

                self.log += [pvm_deadB]
                w_name = await StringManager.center_string(string = winner.name, max_length = 22)
                l_name = await StringManager.center_string(string = loser.name, max_length = 22)
                self.log.append([w_name, l_name])
                self.log += [f"**{winner.name}** `looks around to find something valuable...`"]
                # if loser.monster_class == MonsterClass.Light:
                #     # xp_log = await xp_gainer(argX, 1)
                #     self.log.append(xp_log)

                #     rng = random.randint(0, 1000)
                #     if rng <= 500:
                #         # loot_log = await loot_gen(argX, 1)
                #         # self.log.append(loot_log)
                #     else:
                #         self.log += ["NONE"]
                #         pass

                # if loser.monster_class == MonsterClass.Medium:
                #     # xp_log = await xp_gainer(argX, 2)
                #     # self.log.append(xp_log)

                #     rng = random.randint(0, 1000)
                #     if rng <= 750:
                #         # loot_log = await loot_gen(argX, 2)
                #         # self.log.append(loot_log)
                #     else:
                #         # self.log += ["NONE"]
                #         pass

                # if loser.monster_class == MonsterClass.Heavy:
                #     # xp_log = await xp_gainer(argX, 3)
                #     # loot_log = await loot_gen(argX, 3)
                #     # self.log.append(xp_log)
                #     # self.log.append(loot_log)

class Combatant():
    def __init__(self, character: Character):
        self.character: Character = character

    async def combat_stats(self):
        if type(self.character) == Player:
            self.base_att = round((10 * self.character.attack.get_lvl() + self.character.weapon.weapon_class.value * self.character.weapon.attack.get_lvl() / 2 ), 2)
            self.att_acc = round((1 / 100) * (5 * self.character.attack.get_lvl() + self.character.weapon.weapon_class.value * self.character.weapon.attack.get_lvl() * 2), 4)
            self.base_def = round((1 / 5) * (10 * self.character.defense.get_lvl() + self.character.armor.armor_class.value * self.character.armor.defense.get_lvl() / 2), 2)
            self.def_acc = round((1 / 500) * (5 * self.character.defense.get_lvl() + self.character.armor.armor_class.value * self.character.armor.defense.get_lvl() * 2), 4)
            self.max_hp = self.character.health.get_hp()
            self.hp = self.max_hp
        elif type(self.character) == Monster:
            self.base_att = round((10 * self.character.attack.get_lvl() + self.character.monster_class.value * self.character.attack.get_lvl() / 2), 2)
            self.att_acc = round((1 / 100) * (5 * self.character.attack.get_lvl() + self.character.monster_class.value * self.character.attack.get_lvl() * 2), 4)
            self.base_def = round((1 / 5) * (10 * self.character.defense.get_lvl() + self.character.monster_class.value * self.character.defense.get_lvl() / 2), 2)
            self.def_acc = round((1 / 500) * (5 * self.character.defense.get_lvl() + self.character.monster_class.value * self.character.defense.get_lvl() * 2), 4)
            self.max_hp = self.character.health.get_hp()
            self.hp = self.max_hp

    async def comparative_stats(self, combatant):
        combatant: Combatant = combatant
        self.acc = round((self.att_acc / combatant.def_acc) * 100)
        self.inacc = round((combatant.def_acc / self.att_acc) * 100)