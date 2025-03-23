from settings import*
from behaviors import behaviors

class SHOP(behaviors):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h, image)


shop = SHOP(SCREENSIZE[0]-256, 0, 256, 256, p.image.load('img/shop.png'))