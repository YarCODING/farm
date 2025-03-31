from settings import*


class CAMERA:
    def __init__(self, x, y, speed):
        self.rect = p.Rect(x, y, SCREENSIZE[0], SCREENSIZE[1])
        self.speed = speed

    def move(self, player):
        if player.rect.x >= int((self.rect.x +self.rect.w)*0.7):
            self.rect.x += self.speed


camera = CAMERA(0, 0, 50)