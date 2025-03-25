from settings import*
from behaviors import behaviors


class Shop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.items = [
            {"name": "carrot_bag", "icon_path": "img/plants/carrot_bag.png", "price": 10},
            {"name": "redis_bag", "icon_path": "img/plants/redis_bag.png", "price": 20},
            {"name": "garl_bag", "icon_path": "img/plants/garl_bag.png", "price": 15},
            {"name": "cabb_bag", "icon_path": "img/plants/cabb_bag.png", "price": 15}
        ]
        self.font = p.font.Font('font.ttf', 30)
        self.icon_size = (150, 150)
        self.item_size = (200, 280)

        for item in self.items:
            icon = p.image.load(item['icon_path'])
            item['icon'] = p.transform.scale(icon, self.icon_size)

    def draw(self):
        offset_x = 0
        for item in self.items:
            rect = p.Rect(self.x + offset_x, self.y, *self.item_size)
            p.draw.rect(SCREEN, (255, 220, 180), rect)

            SCREEN.blit(item['icon'], (rect.centerx - self.icon_size[0]/2, self.y + 10))

            price_text = self.font.render(f"¢{item['price']}", True, (0, 0, 0))
            SCREEN.blit(price_text, (rect.centerx - 20, self.y + 210))

            buy_button = p.Rect(rect.centerx - 45, self.y + 240, 90, 30)
            p.draw.rect(SCREEN, (100, 255, 100), buy_button)

            buy_text = self.font.render("Придбати", True, (0, 0, 0))
            SCREEN.blit(buy_text, (rect.centerx - 40, self.y + 235))

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

            name_text = self.font.render(name, True, (0, 0, 0))
            SCREEN.blit(name_text, (rect.x + 25, self.y + 180))

            offset_x += 250

    def check_click(self, mouse_pos, inventory, player_money):
        for item in self.items:
            if item['buy_button'].collidepoint(mouse_pos):
                if player_money >= item['price']:
                    player_money -= item['price']
                    inventory.add_base_item(item['name'], item['icon_path'])

shop = Shop(100, 100)