from settings import *

maps = [0] * 800

class Generations:
    offset_x = 0
    offset_y = 0
    limit = 0 #max_lim 48
    def __init__(self, id:int):
        self.id = id
        self.size = (64, 64)
        self.image = p.image.load('img/grass_img.png')
        self.speed = 5
        self.rect = p.Rect(
            Generations.offset_x,
            Generations.offset_y,
            self.size[0], # ширина 
            self.size[1]  # высота
        )


        if self.id == 0: # трава
            self.image = p.image.load('img/grass_img.png')
        elif self.id == 1: # спахана земля
            self.image = p.image.load('img/showeled.png')
        elif self.id == 2: # полита земля
            self.image = p.image.load('img/watered.png')
        
        self.image = p.transform.scale(self.image, self.size)


        Generations.limit +=1
        if Generations.limit != 48:
            Generations.offset_x += self.size[0]
        else:
            Generations.offset_x = 0
            Generations.offset_y += self.size[1]
            Generations.limit = 0
          


    def draw(self):
        SCREEN.blit(self.image, self.rect)

blocks = []

for block in maps:
    blocks.append(Generations(block))