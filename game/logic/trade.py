import asyncio

from data.database import Database
from discord.message import Message
from game.objects.items import Item
from interface.embeds.trade_embed import TradeEmbed
from interface.selects.trade_selects import *
from interface.views.trade_view import TradeView
from users.users import User

class Trade():
    def __init__(self, msg: Message, db: Database, sender_trader: User):
        self.msg: Message = msg
        self.db: Database = db 
        self.sender_trader: User = sender_trader
        self.receiver_trader: User = None
        self.sender_items_offer: list[Item] = list()
        self.receiver_items_offer: list[Item] = list()
        self.sender_gold_offer: int = 0
        self.receiver_gold_offer: int = 0
        self.sender_trade_status: bool = None   # True if trade accepted, false if declined, none if undecided.
        self.receiver_trade_status: bool = None # True if trade accepted, false if declined, none if undecided.

    async def run_trade(self):
        trade_view = TradeView(db=self.db, trade=self, user=self.sender_trader)
        await trade_view.set_initial_items()

        trade_msg = await self.msg.channel.send(view=trade_view, silent=True)

        # Wait for trade view to finish, return if time out.
        if await trade_view.wait():
            await trade_msg.edit(content="`Trading window timed out!`", view=None)
            return
        
        trade_view = None   

        trade_embed = TradeEmbed(trade=self)
        await trade_embed.set_embed()

        embed_msg = await self.msg.channel.send(embed=trade_embed, silent=True)

        sender_task = asyncio.create_task(self.sender_loop(trade_embed=trade_embed, embed_msg=embed_msg))
        receiver_task = asyncio.create_task(self.receiver_loop(trade_embed=trade_embed, embed_msg=embed_msg))

        await sender_task
        # Delay to ensure sender task run before receiver task.
        await asyncio.sleep(delay=0.5)
        await receiver_task

        if self.sender_trade_status and self.receiver_trade_status:
            await self.complete_trade()

    async def sender_loop(self, trade_embed: TradeEmbed, embed_msg: Message):
        sender_view = TradeView(db=self.db, trade=self, user=self.sender_trader)
        await sender_view.set_followup_items()

        sender_msg = await self.msg.channel.send(content=f"**{self.sender_trader.player.get_name()}'s** `OFFER:`", view=sender_view, silent=True)

        trade = True
        while trade:
            if not await sender_view.wait():
                await trade_embed.update_embed()
                await embed_msg.edit(embed=trade_embed)

                if self.sender_trade_status != None:
                    if self.sender_trade_status:
                        await sender_msg.edit(content=f"**{self.sender_trader.player.get_name()}'s** `has accepted the trade!`", view=None)  
                        trade = False   
                    else:
                        await sender_msg.edit(content=f"**{self.sender_trader.player.get_name()}'s** `has declined the trade!`", view=None)
                        trade = False
                else:
                    sender_view = TradeView(db=self.db, trade=self, user=self.sender_trader)

                    await sender_view.set_followup_items()
                    await sender_msg.edit(content=f"**{self.sender_trader.player.get_name()}'s** `OFFER:`", view=sender_view)
            else:
                await sender_msg.edit(content="`Trading window timed out!`", view=None)
                trade = False

    async def receiver_loop(self, trade_embed: TradeEmbed, embed_msg: Message):
        receiver_view = TradeView(db=self.db, trade=self, user=self.receiver_trader)
        await receiver_view.set_followup_items()

        receiver_msg = await self.msg.channel.send(content=f"**{self.receiver_trader.player.get_name()}'s** `OFFER:`", view=receiver_view, silent=True)

        trade = True
        while trade:
            if not await receiver_view.wait():
                await trade_embed.update_embed()
                await embed_msg.edit(embed=trade_embed)

                if self.receiver_trade_status != None:
                    if self.receiver_trade_status:
                        await receiver_msg.edit(content=f"**{self.receiver_trader.player.get_name()}'s** `has accepted the trade!`", view=None)  
                        trade = False   
                    else:
                        await receiver_msg.edit(content=f"**{self.receiver_trader.player.get_name()}'s** `has declined the trade!`", view=None)
                        trade = False
                else:
                    receiver_view = TradeView(db=self.db, trade=self, user=self.receiver_trader)

                    await receiver_view.set_followup_items()
                    await receiver_msg.edit(content=f"**{self.receiver_trader.player.get_name()}'s** `OFFER:`", view=receiver_view)
            else:
                await receiver_msg.edit(content="`Trading window timed out!`", view=None)
                trade = False

    async def complete_trade(self):
        sender_items_received = ""
        receiver_items_received = ""

        # Return if no item or gold is traded. 
        if len(self.sender_items_offer) == 0 and len(self.receiver_items_offer) == 0 and self.sender_gold_offer == 0 and self.receiver_gold_offer == 0: return

        # Trade items from sender to receiver.
        if len(self.sender_items_offer) != 0:
            for item in self.sender_items_offer:
                # Check receiver trader inventory space.
                if self.receiver_trader.player.inventory.slots >= len(self.receiver_trader.player.inventory.items) + 1:
                    await self.receiver_trader.player.inventory.add_item(item=item)
                    await self.sender_trader.player.inventory.rem_item(item=item)
                    receiver_items_received += f"||||| `ITEM:`**`{item.name}`**\n"
                else:
                    await self.msg.channel.send(content=f"**{self.receiver_trader.player.get_name()}'s `inventory is full, trade wasn't complete.`**")
                    break
                
        # Trade items from receiver to sender.
        if len(self.receiver_items_offer) != 0:
            for item in self.receiver_items_offer:
                # Check receiver trader inventory space.
                if self.sender_trader.player.inventory.slots >= len(self.sender_trader.player.inventory.items) + 1:
                    await self.sender_trader.player.inventory.add_item(item=item)
                    await self.receiver_trader.player.inventory.rem_item(item=item)
                    sender_items_received += f"||||| `ITEM:`**`{item.name}`**\n"
                else:
                    await self.msg.channel.send(content=f"**{self.sender_trader.player.get_name()}'s `inventory is full, trade wasn't complete.`**")
                    break

        if self.sender_gold_offer != 0:
            self.receiver_trader.player.gold += self.sender_gold_offer
            self.sender_trader.player.gold -= self.sender_gold_offer

        if self.receiver_gold_offer != 0:
            self.sender_trader.player.gold += self.sender_gold_offer
            self.receiver_trader.player.gold -= self.sender_gold_offer


        receiver_gold_received = f"||||| `GOLD:`**`{self.sender_gold_offer} GOLD`** "
        sender_gold_received = f"||||| `GOLD:`**`{self.receiver_gold_offer} GOLD`** "

        trade_msg = f"**```arm\r\n{self.sender_trader.player.name} !ReceiveTrade\r\n```**\n"
        trade_msg += sender_items_received
        trade_msg += sender_gold_received

        trade_msg += f"**```arm\r\n{self.receiver_trader.player.name} !ReceiveTrade\r\n```**\n"
        trade_msg += receiver_items_received
        trade_msg += receiver_gold_received

        await self.msg.channel.send(content=trade_msg, silent=True)

        # ADD LOGGER!

        await self.db.save_temp_data(user=self.sender_trader)
        await self.db.save_temp_data(user=self.receiver_trader)