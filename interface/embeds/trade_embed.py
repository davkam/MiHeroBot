from discord.embeds import Embed
from game.objects.items import Item

class TradeEmbed(Embed):
    def __init__(self, trade):
        super().__init__()
        from game.logic.trade import Trade
        self.trade: Trade = trade 

    async def set_embed(self):
        sender_name = self.trade.sender_trader.player.get_name()
        receiver_name = self.trade.receiver_trader.player.get_name()

        self.add_field(name=f"- {sender_name} -", value="`\U0001F4B2 TRADE VALUE: 0 gold`", inline=True)
        self.add_field(name="", value="")
        self.add_field(name=f"- {receiver_name} -", value="`\U0001F4B2 TRADE VALUE: 0 gold`", inline=True)
        self.add_field(name=f"`- ITEM OFFER -`", value=f"`NONE`", inline=True)
        self.add_field(name="", value="")
        self.add_field(name=f"`- ITEM OFFER -`", value=f"`NONE`", inline=True)
        self.add_field(name=f"`- GOLD OFFER -`", value=f"`\U0001F4B0 GOLD: 0 gold`", inline=True)
        self.add_field(name="", value="")
        self.add_field(name=f"`- GOLD OFFER -`", value=f"`\U0001F4B0 GOLD: 0 gold`", inline=True)

    async def update_embed(self):
        sender_name = self.trade.sender_trader.player.get_name()
        receiver_name = self.trade.receiver_trader.player.get_name()

        sender_trade_val = await self.get_value(item_list=self.trade.sender_items_offer, gold=self.trade.sender_gold_offer)
        receiver_trade_val = await self.get_value(item_list=self.trade.receiver_items_offer, gold=self.trade.receiver_gold_offer)
        sender_items = await self.get_items_offer(item_list=self.trade.sender_items_offer)
        receiver_items = await self.get_items_offer(item_list=self.trade.receiver_items_offer)

        self.set_field_at(index=0, name=f"- {sender_name} -", value=f"`\U0001F4B2 TRADE VALUE: {sender_trade_val} gold`", inline=True)
        self.set_field_at(index=2, name=f"- {receiver_name} -", value=f"`\U0001F4B2 TRADE VALUE: {receiver_trade_val} gold` ", inline=True)
        self.set_field_at(index=3, name=f"`- ITEM OFFER -`", value=f"`{sender_items}`", inline=True)
        self.set_field_at(index=5, name=f"`- ITEM OFFER -`", value=f"`{receiver_items}`", inline=True)
        self.set_field_at(index=6, name=f"`- GOLD OFFER -`", value=f"`\U0001F4B0 GOLD: {self.trade.sender_gold_offer} gold`", inline=True)
        self.set_field_at(index=8, name=f"`- GOLD OFFER -`", value=f"`\U0001F4B0 GOLD: {self.trade.receiver_gold_offer} gold`", inline=True)

    async def get_items_offer(self, item_list: list[Item] = None) -> str:
        item_offer = ""
        if item_list != None and len(item_list) != 0:
            for item in item_list:
                item_offer += f"{item.name}\n"
            return item_offer
        else: 
            return "NONE"
    
    async def get_value(self, item_list: list[Item] = None, gold: int = 0) -> int:
        total_val = 0
        total_val += gold

        # if item_list != None:
        #     for item in item_list:
        #         total_val += item.value 

        return total_val
        