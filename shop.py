from settings import*
from behaviors import behaviors


class Shop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.items = [
            {"name": "carrot_bag", "icon_path": "img/plants/carrot_bag.png", "price": 10},
            {"name": "shovel", "icon_path": "img/items/shovel.png", "price": 20},
            {"name": "watercan", "icon_path": "img/items/watercan.png", "price": 15}
        ]
        self.font = p.font.Font('font.ttf', 30)
        self.icon_size = (150, 150)
        self.item_size = (250, 250)

        for item in self.items:
            icon = p.image.load(item['icon_path'])
            item['icon'] = p.transform.scale(icon, self.icon_size)

    def draw(self):
        offset_x = 0
        for item in self.items:
            rect = p.Rect(self.x + offset_x, self.y, *self.item_size)
            p.draw.rect(SCREEN, (255, 220, 180), rect)

            SCREEN.blit(item['icon'], (self.x + offset_x + 50, self.y + 10))

            price_text = self.font.render(f"${item['price']}", True, (0, 0, 0))
            SCREEN.blit(price_text, (self.x + offset_x + 25, self.y + 65))

            buy_button = p.Rect(self.x + offset_x + 10, self.y + 80, 80, 20)
            p.draw.rect(SCREEN, (100, 255, 100), buy_button)
            buy_text = self.font.render("Придбати", True, (0, 0, 0))
            SCREEN.blit(buy_text, (self.x + offset_x + 30, self.y + 80))

            item['rect'] = rect
            item['buy_button'] = buy_button

            offset_x += 290

    def check_click(self, mouse_pos, inventory, player_money):
        for item in self.items:
            if item['buy_button'].collidepoint(mouse_pos):
                if player_money >= item['price']:
                    player_money -= item['price']
                    inventory.add_item(item['name'], item['icon_path'])

shop = Shop(100, 100)