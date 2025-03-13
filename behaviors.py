from settings import*

class behaviors:
    def __init__(self, x, y, w, h, image):
        self.rect = p.Rect(x, y, w, h)
        image = p.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))