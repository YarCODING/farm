from settings import*
from behaviors import*

font = p.font.Font(None, 28)

slot_size = 70
slot_margin = 10

inventory_start_x = (SCREENSIZE[0] - (8 * (slot_size + slot_margin) - slot_margin)) // 2
inventory_y = SCREENSIZE[1] - slot_size - 20


class bag:
    def __init__(self):
        self.size = (70, 70) 
        self.slots = 8
        self.items = [None] * self.slots
        self.items[0] = {"name": "Лопата", "icon": p.transform.scale(p.image.load('img/items/shovel.png'), self.size)}
        self.items[1] = {"name": "Лейка", "icon": p.transform.scale(p.image.load('img/items/watercan.png'), self.size)}
        self.selected_item = None
        self.selected_index = None

    def add_item(self, item_name:str, icondir:str):
        """Добавляет новый предмет в первый свободный слот инвентаря."""
        for i in range(self.slots):
            if self.items[i] is None:
                self.items[i] = {"name": item_name, "icon": p.transform.scale(p.image.load(icondir), self.size)}
                break

    def draw(self, surface):
        """Отрисовывает слоты инвентаря, иконки предметов и выделяет выбранный слот."""
        for i in range(self.slots):
            x = inventory_start_x + i * (slot_size + slot_margin)
            rect = p.Rect(x, inventory_y, slot_size, slot_size)
            p.draw.rect(surface, GRAY, rect)
            if self.items[i] is not None:
                surface.blit(self.items[i]["icon"], (x, inventory_y))
            if self.selected_index == i:
                p.draw.rect(surface, RED, rect, 3)
            num_text = font.render(str(i + 1), True, WHITE)
            surface.blit(num_text, (x + 5, inventory_y + 5))

    def select_slot(self, index):
        """Выбирает слот по индексу и сохраняет название предмета (если слот не пустой)."""
        self.selected_index = index
        if self.items[index] is not None:
            self.selected_item = self.items[index]["name"]
        else:
            self.selected_item = None

inventory = bag()

# class Item(behaviors):
#     def __init__(self, x, y, w, h, speed:int, type:str):
#         self.rect = p.Rect(x, y, w, h)
#         self.size = (w, h)
#         self.image = p.image.load('img/grass_img.png')
#         self.speed = speed
#         self.type = type

#         if self.type == 'shovel':
#             self.image = p.image.load('img/items/shovel.png')

#         self.image = p.transform.scale(self.image, self.size)

# shovel = Item(0, 0, 32, 32, 100, 'shovel')