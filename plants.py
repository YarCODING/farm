from settings import*
from behaviors import*

class Plant:
    def __init__(self, x:int, y:int, type:str, ground):
        self.type = type
        self.stage = 1
        self.size = (48, 48)
        self.grow_speed = random.randint(500, 800)
        self.quality = random.randint(800, 1200)
        self.image = p.transform.scale(p.image.load(f'img/plants/{self.type}1.png'), self.size)
        self.rect = p.Rect(
            x,
            y,
            self.size[0], # ширина 
            self.size[1]  # высота
        )
        self.ground = ground
    
    def draw(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
    
    def grow(self):
        if self.grow_speed == 0 and self.quality > 0:
            self.stage += 1
            if self.stage <= 4:
                self.image = p.transform.scale(p.image.load(f'img/plants/{self.type}{self.stage}.png'), self.size)
            self.grow_speed = random.randint(500, 800)
        elif self.quality <= 0:
            self.image = p.transform.scale(p.image.load(f'img/plants/{self.type}_r.png'), self.size)
        else:
            if self.ground.id == 2:
                self.grow_speed -= 1
            else:
                self.quality -= 1


plants = []