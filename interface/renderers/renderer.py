from loggers.loggers import Loggers

class Renderer():
    FONT_PATH = "game/assets/font/m5x7_font.ttf"

    BG1_PATH = "game/assets/backgrounds/bg_1.png"
    BG2_PATH = "game/assets/backgrounds/bg_2.png"
    BG3_PATH = "game/assets/backgrounds/bg_3.png"

    def __init__(self):
        self.logger = Loggers.renderer
        pass 