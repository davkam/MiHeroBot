# -*- coding: ISO-8859-15 -*-

from discord.embeds import Embed
from discord.message import Message
from tools.tools import StringManager
import asyncio

class FightEmbed(Embed):
    def __init__(self, msg: Message, log: list[str]):
        super().__init__()
        self.msg: Message = msg
        self.log: list[str] = log

    async def run_embed(self): # TBD: Add remaining health next to percentage health.
            nameA = await StringManager.cap_string(string = self.log[1][0], max_length = 12)
            nameB = await StringManager.cap_string(string = self.log[2][0], max_length = 14)

            self.set_image(url = self.log[0])
            self.add_field(name=f"{nameA}", value=f"`\U00002B50 LVL: {self.log[1][1]}`\n`\U00002694\uFE0F ATT: {self.log[1][2]}`\n`\U0001F6E1\uFE0F DEF: {self.log[1][3]}`\n`\U00002764\uFE0F HP:  {self.log[1][4]}`", inline=True)
            self.add_field(name="`|||||| STATUS ||||||`", value=f"`- PREPARING FIGHT  -`\n`- DECIDING TURN... -`", inline=True)
            self.add_field(name=f"{nameB}", value=f"`\U00002B50 LVL: {self.log[2][1]}`\n`\U00002694\uFE0F ATT: {self.log[2][2]}`\n`\U0001F6E1\uFE0F DEF: {self.log[2][3]}`\n`\U00002764\uFE0F HP:  {self.log[2][4]}`", inline=True)
            self.add_field(name="IIIIIIIIIIIIIIIIIIII`100%`", value=f"`{self.log[3][0]}`\n`{self.log[3][1]}`", inline=True)
            self.add_field(name="", value="", inline=True)
            self.add_field(name="IIIIIIIIIIIIIIIIIIII`100%`", value=f"`{self.log[4][0]}`\n{self.log[4][1]}", inline=True)
            
            await asyncio.sleep(delay=2)
            await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
            end_msg = await self.msg.channel.send(content = "\u200b", silent=True)
            await asyncio.sleep(delay=2)
            
            for i in range(5, len(self.log), 4):
                if self.log[i+2][1] <= 0: self.log[i+2][1] = 0
                if self.log[i+3][1] <= 0: self.log[i+3][1] = 0

                self.set_image(url = self.log[i])
                self.set_field_at(index=1, name="`|||||| STATUS ||||||`", value=f"**`{self.log[i+1]}`**", inline=True)
                self.set_field_at(index=3, name=f"{self.log[i+2][0]}`{self.log[i+2][1]}%`", value=f"`{self.log[3][0]}`\n`{self.log[3][1]}`", inline=True)
                self.set_field_at(index=5, name=f"{self.log[i+3][0]}`{self.log[i+3][1]}%`", value=f"`{self.log[4][0]}`\n{self.log[4][1]}", inline=True)
    
                await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
                await asyncio.sleep(delay=1)

                self.set_image(url = self.log[0])
                
                await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
                await asyncio.sleep(delay=1)

                if self.log[i+2][1] <= 0 or self.log[i+3][1] <= 0: break
                await asyncio.sleep(delay=1)

            self.set_image(url = self.log[i+4])
            self.set_field_at(index=1, name=f"`|||||| WINNER ||||||`", value=f"**`{self.log[i+5][0]}`**", inline=True)
            self.set_field_at(index=4, name=f"`|||||| LOSER  ||||||`", value=f"**`{self.log[i+5][1]}`**", inline=True)
           
            await self.msg.edit(content = "**```arm\r\nMiHero !Fight\r\n```**\n", embed = self)
            await asyncio.sleep(delay=0.5)

            await end_msg.edit(content = self.log[i+6])
            await asyncio.sleep(delay=1)
            if self.log[i+7] != "NONE":
                sum_log = self.log[i+7]
                if self.log[i+8] != "NONE":
                    sum_log += self.log[i+8]
                    await end_msg.edit(content = sum_log)
                else:
                    await end_msg.edit(content = sum_log)