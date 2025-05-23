from settings import*
from behaviors import*

class Player(behaviors):
    def __init__(self, x, y, w, h, image, speed:int, images:list):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.images = []
        for im in images:
            im = p.transform.scale(im, (w, h))
            self.images.append(im)
        self.state = 'stand'
        self.direction = 'r'
        self.reverse = False
        self.im_num = 0
        self.anim_timer = 10
        
        self.money = 100

        self.vect = None
    
    def move(self, pos):
        v1 = p.Vector2(self.rect.x, self.rect.y)
        v2 = p.Vector2(pos[0], pos[1])
        v3 = v2 - v1

        if pos:
            if v3.length() > self.speed:
                self.vect = v3.normalize()
                self.rect.x += self.vect[0] * self.speed
                self.rect.y += self.vect[1] * self.speed
                self.state = 'walk'
            else:
                self.rect.x, self.rect.y = pos
                self.state = 'stand'
        
            if pos[0] < self.rect.centerx:
                if self.direction == 'r':
                    self.reverse = True
                self.direction = 'l'
            else:
                if self.direction == 'l':
                    self.reverse = True
                self.direction = 'r'

    
    def animate(self):
        if self.reverse:
            for i in range(len(self.images)):
                self.images[i] = p.transform.flip(self.images[i], True, False)
            self.reverse = False


        if self.anim_timer == 0:
            if self.state == 'walk':
                if self.im_num > 7 or self.im_num < 4:
                    self.im_num = 4
            else:
                if self.im_num > 3:
                    self.im_num = 0
            self.image = self.images[self.im_num]
            self.im_num += 1
            self.anim_timer = 10
        else:
            self.anim_timer -= 1


images = [p.image.load("img/player/idle1.png"), p.image.load("img/player/idle2.png"), p.image.load("img/player/idle3.png"), p.image.load("img/player/idle4.png"), p.image.load("img/player/walk1.png"), p.image.load("img/player/walk2.png"), p.image.load("img/player/walk3.png"), p.image.load("img/player/walk4.png"), p.image.load("img/player/walk5.png")]
player = Player(SCREENSIZE[0]/2, SCREENSIZE[1]/2, 64, 64, p.image.load("img/player/idle1.png"), 10, images)