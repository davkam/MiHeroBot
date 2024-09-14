from game.objects.items.equipables import *

class Equipment():
    __slots__ = ['sword', 'shield', 'head', 'body', 'amulet', 'ring']
    
    def __init__(self, sword: Sword = None, shield: Shield = None, head: HeadArmor = None, body: BodyArmor = None, amulet: Amulet = None, ring: Ring = None):
        self.sword: Sword = sword or Sword()
        self.shield: Shield = shield or Shield()
        self.head: HeadArmor = head
        self.body: BodyArmor = body
        self.amulet: Amulet = amulet
        self.ring: Ring = ring