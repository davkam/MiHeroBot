# -*- coding: ISO-8859-15 -*-

from extras.string_manager import StringManager
import asyncio
import discord

class FightEmbed(discord.Embed):
    def __init__(self, msg: discord.message.Message, log: list[str]):
        super().__init__()
        self.msg = msg
        self.log = log

    async def run_embed(self):
            nameA = await StringManager.cap_string(string = self.log[1][0], max_length = 11)
            nameB = await StringManager.cap_string(string = self.log[2][0], max_length = 13)

            self.set_image(url = self.log[0])
            self.add_field(name=f"**{nameA}**", value=f"`LVL: {self.log[1][1]}`\n`ATT: {self.log[1][2]}`\n`DEF: {self.log[1][3]}`\n`HP:  {self.log[1][4]}`", inline=True)
            self.add_field(name="`||||||| STATUS |||||||`", value=f"`-FIGHT ABOUT TO BEGIN-`\n`-   DECIDING TURN... -`", inline=True)
            self.add_field(name=f"**{nameB}**", value=f"`LVL: {self.log[2][1]}`\n`ATT: {self.log[2][2]}`\n`DEF: {self.log[2][3]}`\n`HP:  {self.log[2][4]}`", inline=True)
            self.add_field(name="**IIIIIIIIIIIIIIIIIIII**\r\n       `(100%)`", value=f"`{self.log[3][0]}`\n`{self.log[3][1]}`", inline=True)
            self.add_field(name="", value="", inline=True)
            self.add_field(name="**IIIIIIIIIIIIIIIIIIII**\r\n       `(100%)`", value=f"`{self.log[4][0]}`\n{self.log[4][1]}", inline=True)
            
            await asyncio.sleep(2)
            await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
            await asyncio.sleep(2)
            
            for i in range(5, len(self.log), 4):
                if self.log[i+2][1] <= 0: self.log[i+2][1] = 0
                if self.log[i+3][1] <= 0: self.log[i+3][1] = 0

                self.set_image(url = self.log[i])
                self.set_field_at(index=1, name="`||||||| STATUS |||||||`", value=f"**`{self.log[i+1]}`**", inline=True)
                self.set_field_at(index=3, name=f"**{self.log[i+2][0]}**\r\n       `({self.log[i+2][1]}%)`", value=f"`{self.log[3][0]}`\n`{self.log[3][1]}`", inline=True)
                self.set_field_at(index=5, name=f"**{self.log[i+3][0]}**\r\n       `({self.log[i+3][1]}%)`", value=f"`{self.log[4][0]}`\n{self.log[4][1]}", inline=True)
    
                await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
                await asyncio.sleep(1)

                self.set_image(url = self.log[0])
                
                await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
                await asyncio.sleep(1)

                if self.log[i+2][1] <= 0 or self.log[i+3][1] <= 0: break
                await asyncio.sleep(1)

            self.set_image(url = self.log[i+4])
            self.set_field_at(index=1, name=f"`||||||| WINNER |||||||`", value=f"**`{self.log[i+5][0]}`**", inline=True)
            self.set_field_at(index=4, name=f"`||||||| LOSER  |||||||`", value=f"**`{self.log[i+5][1]}`**", inline=True)
           
            await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
            await asyncio.sleep(1)

            # end_msg = await self.msg.channel.send(log[i+7])
            # await asyncio.sleep(1)
            # if log[i+8] != "NONE":
            #     sum_log = log[i+8]
            #     if log[i+9] != "NONE":
            #         sum_log += log[i+9]
            #         await end_msg.edit(content = sum_log)
            #     else:
            #         await end_msg.edit(content = sum_log)

