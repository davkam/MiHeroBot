from game.interface.views import TradeView
from discord.ui import Modal

class TradeModal(Modal):
    def __init__(self) -> None:
        super().__init__(title="TRADE TITLE", timeout=60)