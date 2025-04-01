from settings import*
from behaviors import*


class ANIMAL(behaviors):
    def __init__(self):
        super().__init__(random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]), 32, 32, p.image.load('img/ant/idle1.png'))
        self.speed = 5
        self.images_list = [p.image.load('img/ant/idle1.png'), p.image.load('img/ant/idle2.png'), p.image.load('img/ant/idle3.png'), p.image.load('img/ant/idle4.png'), p.image.load('img/ant/walk1.png'), p.image.load('img/ant/walk2.png'), p.image.load('img/ant/walk3.png'), p.image.load('img/ant/walk4.png')]
        self.images = []
        for im in self.images_list:
            im = p.transform.scale(im, (32, 32))
            self.images.append(im)
        self.state = 'stand'
        self.direction = 'r'
        self.reverse = False
        self.im_num = 0
        self.stand_timer = 100
        self.anim_timer = 10
        
        self.pos = (random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]))
        self.vect = None

    
    def move(self):
        v1 = p.Vector2(self.rect.x, self.rect.y)
        v2 = p.Vector2(self.pos[0], self.pos[1])
        v3 = v2 - v1

        if v3.length() > self.speed:
            self.vect = v3.normalize()
            self.rect.x += self.vect[0] * self.speed
            self.rect.y += self.vect[1] * self.speed
            self.state = 'walk'
        else:
            self.rect.x, self.rect.y = self.pos
            self.state = 'stand'
            self.stand_timer -= 1

        if self.stand_timer == 0:
            self.pos = (random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]))
            self.stand_timer = random.randint(50, 200)

        if self.pos[0] < self.rect.centerx:
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
                if self.im_num > 6 or self.im_num < 4:
                    self.im_num = 4
            else:
                if self.im_num > 3:
                    self.im_num = 0
            self.image = self.images[self.im_num]
            self.im_num += 1
            self.anim_timer = 10
        else:
            self.anim_timer -= 1




ant_img = [p.image.load('img/ant/idle1.png'), p.image.load('img/ant/idle2.png'), p.image.load('img/ant/idle3.png'), p.image.load('img/ant/idle4.png'), p.image.load('img/ant/walk1.png'), p.image.load('img/ant/walk2.png'), p.image.load('img/ant/walk3.png'), p.image.load('img/ant/walk4.png')]
ants = [ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL(), ANIMAL()]