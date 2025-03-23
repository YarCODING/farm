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
        self.base_slots = 8
        self.extra_slots = 8

        self.slots = self.base_slots
        self.items = [None] * (self.base_slots + self.extra_slots)
        self.items[0] = {"name": "shovel", "icon": p.transform.scale(p.image.load('img/items/shovel.png'), self.size), "count": 1}
        self.items[1] = {"name": "watercan", "icon": p.transform.scale(p.image.load('img/items/watercan.png'), self.size), "count": 1}
        self.items[2] = {"name": "carrot_bag", "icon": p.transform.scale(p.image.load('img/plants/carrot_bag.png'), self.size), "count": 1}

        self.selected_item = None
        self.selected_index = None
        self.expanded = False

    def toggle_expand(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.slots = self.base_slots + self.extra_slots
        else:
            self.slots = self.base_slots

    def add_base_item(self, item_name: str, icondir: str):
        for i in range(self.base_slots):
            if self.items[i] is None:
                self.items[i] = {"name": item_name, "icon": p.transform.scale(p.image.load(icondir), self.size)}
                break

    def add_extra_item(self, item_name: str, icondir: str):
        for i in range(self.base_slots, self.base_slots + self.extra_slots):
            if self.items[i] is not None and self.items[i]["name"] == item_name:
                self.items[i]["count"] += 1

        for i in range(self.base_slots, self.base_slots + self.extra_slots):
            if self.items[i] is None:
                self.items[i] = {
                    "name": item_name,
                    "icon": p.transform.scale(p.image.load(icondir), self.size),
                    "count": 1
                }


    def draw(self, surface):
        for i in range(self.slots):
            if i < 8:
                x_i = i
            elif i == 8:
                x_i = 0
            else:
                x_i += 1


            x = inventory_start_x + x_i * (slot_size + slot_margin)
            y = inventory_y


            if self.expanded and i >= self.base_slots:
                y = inventory_y - slot_size - 20

            rect = p.Rect(x, y, slot_size, slot_size)
            p.draw.rect(surface, INVENTORYCOLOR, rect)
            if self.items[i] is not None:
                surface.blit(self.items[i]["icon"], (x, y))
                if self.items[i].get("count", 1) > 1:
                    count_text = font.render(str(self.items[i]["count"]), True, (0, 0, 0))
                    surface.blit(count_text, (x + slot_size - 20, y + slot_size - 20))
            if self.selected_index == i:
                p.draw.rect(surface, INVENTORYTAKE, rect, 3)
            num_text = font.render(str(i + 1), True, INVENTORYNUM)
            surface.blit(num_text, (x + 5, y + 5))


    def select_slot(self, index):
        if self.selected_index == index:
            self.selected_index = None
            self.selected_item = None
        else:
            self.selected_index = index
            if self.items[index] is not None:
                self.selected_item = self.items[index]["name"]
            else:
                self.selected_item = None

inventory = bag()