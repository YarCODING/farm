from settings import*
from behaviors import*

class Plant:
    def __init__(self, x:int, y:int, type:str):
        self.type = type
        self.stage = 1
        self.size = (48, 48)
        self.image = p.transform.scale(p.image.load(f'img/plants/{type}1.png'), self.size)
        self.rect = p.Rect(
            x,
            y,
            self.size[0], # ширина 
            self.size[1]  # высота
        )
    
    def draw(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

plants = []