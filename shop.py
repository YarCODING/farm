from settings import*
from behaviors import behaviors
from player import player
from bag import inventory

class Shop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.goods = [
            {"name": "carrot_bag", "icon_path": "img/plants/carrot_bag.png", "price": 10},
            {"name": "garl_bag", "icon_path": "img/plants/garl_bag.png", "price": 15},
            {"name": "redis_bag", "icon_path": "img/plants/redis_bag.png", "price": 20},
            {"name": "cabb_bag", "icon_path": "img/plants/cabb_bag.png", "price": 40}
        ]
        self.goods2 = [
            {"name": "carrot", "icon_path": "img/plants/carrot.png", "price": 1},
            {"name": "garl", "icon_path": "img/plants/garl.png", "price": 3},
            {"name": "redis", "icon_path": "img/plants/redis.png", "price": 5},
            {"name": "cabb", "icon_path": "img/plants/cabb.png", "price": 10}
        ]
        self.font = p.font.Font('font.ttf', 30)
        self.icon_size = (150, 150)
        self.item_size = (200, 280)

        for item in self.goods:
            icon = p.image.load(item['icon_path'])
            item['icon'] = p.transform.scale(icon, self.icon_size)
        for item in self.goods2:
            icon = p.image.load(item['icon_path'])
            item['icon'] = p.transform.scale(icon, self.icon_size)

    def draw(self):
        # Купівля
        offset_x = 0
        for item in self.goods:
            rect = p.Rect(self.x + offset_x, self.y, *self.item_size)
            p.draw.rect(SCREEN, (255, 220, 180), rect)

            SCREEN.blit(item['icon'], (rect.centerx - self.icon_size[0]/2, rect.topleft[1]+10))

            price_text = self.font.render(f"¢{item['price']}", True, (0, 0, 0))
            SCREEN.blit(price_text, (rect.centerx - 20, rect.bottomleft[1] - 70))

            buy_button = p.Rect(rect.centerx - 45, self.y + 240, 90, 30)
            p.draw.rect(SCREEN, (100, 255, 100), buy_button)

            buy_text = self.font.render("Придбати", True, (0, 0, 0))
            SCREEN.blit(buy_text, (rect.centerx - 40, rect.bottomleft[1] - 40))

            item['rect'] = rect
            item['buy_button'] = buy_button

            name = ''
            match item["name"]:
                case "cabb_bag":
                    name = 'Насіння капусти'
                case "carrot_bag":
                    name = 'Насіння моркви'
                case "garl_bag":
                    name = 'Насіння часнику'
                case "redis_bag":
                    name = 'Насіння редису'
                case _:
                    name = "NAME NOT FOUND ERROR"

            name_text = self.font.render(name, True, (0, 0, 0))
            SCREEN.blit(name_text, (rect.x + 25, rect.bottomleft[1] - 100))

            offset_x += 250

        # Продаж
        offset_x = 0
        for item in self.goods2:
            rect = p.Rect(self.x + offset_x, SCREENSIZE[1]/1.9, *self.item_size)
            p.draw.rect(SCREEN, (255, 220, 180), rect)

            SCREEN.blit(item['icon'], (rect.centerx - self.icon_size[0]/2, rect.topleft[1]+10))

            price_text = self.font.render(f"¢{item['price']}", True, (0, 0, 0))
            SCREEN.blit(price_text, (rect.centerx - 20, rect.bottomleft[1] - 70))

            sell_button = p.Rect(rect.centerx - 45, rect.bottomleft[1] - 40, 90, 30)
            p.draw.rect(SCREEN, (100, 255, 100), sell_button)

            sell_text = self.font.render("Продати", True, (0, 0, 0))
            SCREEN.blit(sell_text, (rect.centerx - 35, rect.bottomleft[1] - 40))

            item['rect'] = rect
            item['sell_button'] = sell_button

            name = ''
            match item["name"]:
                case "cabb":
                    name = 'Капуста'
                case "carrot":
                    name = 'Морква'
                case "garl":
                    name = 'Часник'
                case "redis":
                    name = 'Редис'
                case _:
                    name = "NAME NOT FOUND ERROR"

            name_text = self.font.render(name, True, (0, 0, 0))
            SCREEN.blit(name_text, (rect.x + 70, rect.bottomleft[1] - 100))

            offset_x += 250
            
    def check_click(self, mouse_pos, items):
        for item in self.goods:
            if item['buy_button'].collidepoint(mouse_pos):
                if player.money >= item['price']:
                    player.money -= item['price']
                    inventory.add_base_item(item['name'], item['icon_path'])
        
        for item in self.goods2:
            if item['sell_button'].collidepoint(mouse_pos):
                for inv_item in items:
                    if inv_item:
                        if inv_item["name"] == item["name"]:
                            player.money += item['price']
                            inv_item['count'] -= 1
                            break
                        


shop = Shop(100, 100)