from settings import*
from behaviors import*

class Bag(behaviors):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h, image)




class Item(behaviors):
    def __init__(self, x, y, w, h, image, speed:int, type:str):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.type = type
    
    def move(self, player):
        v1 = p.Vector2(self.rect.x, self.rect.y)
        v2 = p.Vector2(player.rect.left, player.rect.centery)
        v3 = v2 - v1

        if self.rect.x != player.rect.left and self.rect.y != player.rect.centery:
            self.vect = v3.normalize()
            self.rect.x += self.vect[0]*self.speed
            self.rect.y += self.vect[1]*self.speed