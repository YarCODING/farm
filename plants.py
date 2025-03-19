from settings import*
from behaviors import*

class Plant:
    def __init__(self, x:int, y:int, type:str, ground):
        self.type = type
        self.stage = 1
        self.size = (48, 48)
        self.grow_timer = random.randint(1500, 2000)
        self.quality = random.randint(5000, 8000)
        self.image = p.transform.scale(p.image.load(f'img/plants/{self.type}1.png'), self.size)
        self.rect = p.Rect(
            x,
            y,
            self.size[0],
            self.size[1]
        )
        self.ground = ground
    
    def draw(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
    
    def grow(self):
        global sunny
        if self.grow_timer == 0 and self.quality > 0:
            self.stage += 1
            if self.stage <= 4:
                self.image = p.transform.scale(p.image.load(f'img/plants/{self.type}{self.stage}.png'), self.size)
            self.grow_timer = random.randint(500, 800)
        elif self.quality <= 0:
            self.image = p.transform.scale(p.image.load(f'img/plants/{self.type}_r.png'), self.size)
        else:
            if self.ground.id == 2:
                if sunny:
                    self.grow_timer -= 2
                else:
                    self.grow_timer -= 1
            else:
                self.quality -= 1


plants = []