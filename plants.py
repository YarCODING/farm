from settings import*
from behaviors import*

class Plant(behaviors):
    def __init__(self, x, y, w, h, image, speed:int, images:list):
        super().__init__(x, y, w, h, image)