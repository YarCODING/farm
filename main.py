from imports import*
from PyQt5.QtWidgets import QMessageBox, QApplication

p.mixer.music.load('music.mp3')
p.mixer.music.set_volume(0.1)
p.mixer.music.play(-1)

lpos = None
rpos = None

"""
Керування:
Esc - віхід у меню
Tab - відкривання/закривання додаткового інвентарю
L клік - переміщення
R клік - взаємодія
1-8 - вибір слоту інвентаря
"""

#saves
def save_game(blocks, plants, inventory, time_of_day):
    data = {
        'blocks': [],
        'plants': [],
        'inventory': [],
        'time_of_day': time_of_day,
        'money': player.money
    }
    
    # Сохраняем блоки
    for block in blocks:
        data['blocks'].append({'id': block.id, 'dry_timer': block.dry_timer})
    
    # Сохраняем растения
    for plant in plants:
        data['plants'].append({
            'type': plant.type,
            'stage': plant.stage,
            'x': plant.rect.x,
            'y': plant.rect.y,
            'grow_timer': plant.grow_timer,
            'quality': plant.quality,
            'ground_id': plant.ground.id
        })
    
    # Сохраняем инвентарь
    inventory_data = []
    for item in inventory.items:
        if item is None:
            inventory_data.append(None)
        else:
            inventory_data.append({"name": item["name"], "count": item["count"]})
    data["inventory"] = inventory_data

    with open('save.json', 'w') as f:
        json.dump(data, f)


def load_game():
    blocks = []
    plants = []
    inventory = bag()
    time_of_day = 0
    
    try:
        with open('save.json', 'r') as f:
            data = json.load(f)
        
        # Загружаем блоки
        Generations.offset_x = 0
        Generations.offset_y = 0
        Generations.limit = 0
        for block_data in data['blocks']:
            block = Generations(block_data['id'], block_data['dry_timer'])
            blocks.append(block)
        
        # Загружаем растения
        for plant_data in data['plants']:
            # Найти землю, на которой растение
            ground_block = next((b for b in blocks if b.rect.x == plant_data['x'] and b.rect.y == plant_data['y']), None)
            if ground_block:
                plant = Plant(plant_data['x'], plant_data['y'], plant_data['type'], ground_block)
                plant.stage = plant_data['stage']
                plant.grow_timer = plant_data['grow_timer']
                plant.quality = plant_data['quality']
                plant.image = p.transform.scale(p.image.load(f'img/plants/{plant.type}{plant.stage}.png'), plant.size)
                plants.append(plant)
        
        # Загружаем инвентарь
        inventory.items = []
        for item_data in data['inventory']:
            if item_data is None:
                inventory.items.append(None)
            else:
                name = item_data["name"]
                count = item_data["count"]
                if name == "shovel":
                    icon = p.image.load('img/items/shovel.png')
                elif name == "watercan":
                    icon = p.image.load('img/items/watercan.png')
                elif name == "carrot_bag":
                    icon = p.image.load('img/plants/carrot_bag.png')
                elif name == "cabb_bag":
                    icon = p.image.load('img/plants/cabb_bag.png')
                elif name == "garl_bag":
                    icon = p.image.load('img/plants/garl_bag.png')
                elif name == "redis_bag":
                    icon = p.image.load('img/plants/redis_bag.png')
                elif name == "carrot":
                    icon = p.image.load('img/plants/carrot.png')
                elif name == "cabb":
                    icon = p.image.load('img/plants/cabb.png')
                elif name == "garl":
                    icon = p.image.load('img/plants/garl.png')
                elif name == "redis":
                    icon = p.image.load('img/plants/redis.png')
                else:
                    icon = None
                inventory.items.append({
                    "name": name,
                    "icon": p.transform.scale(icon, inventory.size),
                    "count": count
                })

        # Загружаем время дня
        time_of_day = data.get('time_of_day', 0)

        money = data.get('money', 0)

        return blocks, plants, inventory, time_of_day, money
    except FileNotFoundError:
        Generations.offset_x = 0
        Generations.offset_y = 0
        Generations.limit = 0
        for _ in range(510):
            blocks.append(Generations(0))
        return blocks, plants, inventory, 2300, 0


# Настройки
DAY_LENGTH = 10000
HALF_DAY = DAY_LENGTH // 2

def update_day_night():
    global time_of_day, sunny
    time_of_day = (time_of_day + 1) % DAY_LENGTH

    overlay = p.Surface(SCREEN.get_size(), p.SRCALPHA)

    # Определяем, день или ночь
    if time_of_day < HALF_DAY:
        sunny = True
        # Рассчитываем уровень затемнения (0 ночью, минимально днём)
        darkness = int(200 * abs((time_of_day - HALF_DAY) / HALF_DAY))
    else:
        sunny = False
        darkness = int(200 * abs((time_of_day - HALF_DAY) / HALF_DAY))

    # Затемняющий слой
    overlay.fill((0, 0, 0, darkness))
    SCREEN.blit(overlay, (0, 0))


blocks, plants, inventory, time_of_day, player.money = load_game()

play_btn = behaviors(SCREENSIZE[0]/2-108, SCREENSIZE[1]/2+80, 236, 108, p.image.load('img/ui/play.png'))
exit_btn = behaviors(SCREENSIZE[0]/2-108, SCREENSIZE[1]/2+220, 236, 108, p.image.load('img/ui/exit.png'))
shop_exit_btn = behaviors(SCREENSIZE[0]-74, 10, 64, 64, p.image.load('img/ui/shop_exit.png'))
reset_btn = behaviors(SCREENSIZE[0]-42, SCREENSIZE[1]- 42, 32, 32, p.image.load('img/ui/reset.png'))
info_btn = behaviors(SCREENSIZE[0]-92, SCREENSIZE[1]- 42, 32, 32, p.image.load('img/ui/info.png'))

shop_building = behaviors(SCREENSIZE[0]-256, 0, 256, 256, p.image.load('img/shop.png'))
coin_UI = behaviors(10, 10, 32, 32, p.image.load('img/ui/coin.png'))

app = QApplication([])
reset_confirm = QMessageBox()
reset_confirm.setWindowTitle("reset")
reset_confirm.setText("Скинути прогрес?\n(Cancel - відміняє сброс)")
reset_confirm.setIcon(QMessageBox.Warning)
reset_confirm.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)

info_win = QMessageBox()
info_win.setWindowTitle("info")
info_win.setText(
    "\n🎮 Управління:"
    "\nПересування: WASD"
    "\nВикористання предметів: ЛКМ (ліва кнопка миші)"
    "\nРозширення інвентаря: Tab"
    "\nВибір предмета в інвентарі: Цифри 1-8"
    "\nЗбереження гри: Автоматично"
    
    "\n\n🌱 Як грати?"
    "\n1. Підготуйте землю: Використовуйте лопату, щоб розчистити місце для посадки."
    "\n2. Посадіть насіння: Виберіть насіння в інвентарі та посадіть його на підготовлену землю."
    "\n   На одному блоці може рости тільки одна рослина!"
    "\n3. Поливайте рослини: Використовуйте лійку, щоб рослини не засохли та росли швидше."
    "\n   Поливати можна навіть не повністю висохлу землю."
    "\n4. Збирайте врожай: Коли рослина дозріє, натисніть ПКМ, щоб зібрати її."
    "\n   Овочі автоматично додаються у додаткові слоти інвентаря."
    "\n5. Продавайте врожай та купуйте предмети:"
    "\n   - Зайдіть магазин."
    "\n   - У продажу з'являться ваші овочі – натисніть 'Продати', щоб отримати монети."
    "\n   - У покупці доступні нові інструменти та насіння – натисніть 'Купити', щоб їх придбати."
    
    "\n\n🌞 Слідкуйте за часом доби:"
    "\nВ грі змінюється день і ніч. Вночі: темніше, рослини ростуть повільніше, земля сохне повільніше, а вдень: сонячно, рослини ростуть швидше, земля сохне швидше."
    "\n\n🎯 Ваша мета:"
    "\nЗаробити якомога більше монет, вирощуючи та продаючи овочі та покращувати свою ферму🚜🌿"
    
    "\n\nБажаємо успіху, фермере! 🌾🔥"
)
info_win.setStandardButtons(QMessageBox.Ok)

def reset():
    global blocks, plants, inventory, time_of_day, player
    Generations.offset_x = 0
    Generations.offset_y = 0
    Generations.limit = 0
    for _ in range(510):
        blocks.append(Generations(0))

    plants = []
    inventory = bag()
    time_of_day = 2300
    player.money = 0


game = False
menu = True
in_shop = False
was_in_shop = False

while True:
    if menu:
        SCREEN.blit(menu_bg, (0, 0))
        SCREEN.blit(title_txt, (SCREENSIZE[0]/2-600, SCREENSIZE[1]/2-300))
        play_btn.draw()
        exit_btn.draw()
        reset_btn.draw()
        info_btn.draw()

        for event in p.event.get():
            if event.type == p.QUIT:
                save_game(blocks, plants, inventory, time_of_day)
                p.quit()
                sys.exit()
            if menu and event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if play_btn.rect.collidepoint(x, y):
                    menu = False
                    game = True
                elif exit_btn.rect.collidepoint(x, y):
                    save_game(blocks, plants, inventory, time_of_day)
                    p.quit()
                    sys.exit()
                elif reset_btn.rect.collidepoint(x, y):
                    result = reset_confirm.exec_()
                    if result == QMessageBox.Yes:
                        reset()
                    elif result == QMessageBox.Cancel:
                        p.quit()
                        sys.exit()
                elif info_btn.rect.collidepoint(x, y):
                    info_win.exec_()
    if in_shop and not was_in_shop:
        SCREEN.fill((168, 102, 74))
        write(20, 30, 'Купівля', (235, 188, 129), 72)
        write(20, SCREENSIZE[1]/2 - 50, 'Продаж', (235, 188, 129), 72)
        inventory.draw()
        coin_UI.draw()
        write(45, 3, str(player.money), (235, 188, 129), 48)
        shop_exit_btn.draw()
        shop.draw()

        for event in p.event.get():
            if event.type == p.QUIT:
                save_game(blocks, plants, inventory, time_of_day)
                p.quit()
                sys.exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    menu = True
                    game = False
                    in_shop = False
                if event.key == p.K_TAB:
                    inventory.toggle_expand()
                if p.K_1 <= event.key <= p.K_8:
                    slot_index = event.key - p.K_1
                    inventory.select_slot(slot_index)
                    
            if in_shop and event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if shop_exit_btn.rect.collidepoint(x, y):
                    game = True
                    in_shop = False
                    was_in_shop = True
                    
                shop.check_click(event.pos, inventory)
    if game and not menu and not in_shop:
        SCREEN.fill(white)

        for block in blocks:
            block.draw()
            block.dry()

        for ant in ants:
            ant.draw()
            ant.move()
            ant.animate()

        for plant in plants:
            plant.grow()
            plant.draw()

        shop_building.draw()

        player.draw()
        inventory.draw()
        coin_UI.draw()
        write(45, 3, str(player.money), (235, 188, 129), 48)

        if lpos:
            player.move(lpos)
            if walk_sound_time == 0 and player.state == 'walk':
                walk.play()
                walk_sound_time = random.randint(10, 20)
            walk_sound_time -= 1
        if player.state == 'stand':
            lpos = None

        if player.rect.colliderect(shop_building.rect) and not was_in_shop:
            in_shop = True
        elif not player.rect.colliderect(shop_building.rect) and was_in_shop:
            was_in_shop = False
        
        player.animate()
        

        for event in p.event.get():
            if event.type == p.QUIT:
                save_game(blocks, plants, inventory, time_of_day)
                p.quit()
                sys.exit()

            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    menu = True
                    game = False
                if event.key == p.K_TAB:
                    inventory.toggle_expand()
                if p.K_1 <= event.key <= p.K_8:
                    slot_index = event.key - p.K_1
                    inventory.select_slot(slot_index)
                
            
            if event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                rpos = event.pos
                
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                lpos = event.pos

            for block in blocks:
                to_player_distance = p.Vector2(player.rect.centerx, player.rect.centery).distance_to(p.Vector2(block.rect.centerx, block.rect.centery))

                if rpos:
                    if block.rect.collidepoint(rpos) and to_player_distance <= 200:
                        match inventory.selected_item:
                            case 'shovel':
                                match block.id:
                                    case 0:
                                        block.image = p.image.load('img/showeled.png')
                                        block.image = p.transform.scale(block.image, block.size)
                                        block.id = 1
                                        shovel_sound.play()
                                    case 1:
                                        block.image = p.image.load('img/grass_img.png')
                                        block.image = p.transform.scale(block.image, block.size)
                                        block.id = 0
                                        shovel_sound.play()
                            case 'watercan':
                                match block.id:
                                    case 1:
                                        block.image = p.image.load('img/watered.png')
                                        block.image = p.transform.scale(block.image, block.size)
                                        block.id = 2
                                        block.dry_timer = Generations.dry_timer
                                        water_sound.play()
                                    case 2:
                                        block.image = p.image.load('img/watered.png')
                                        block.image = p.transform.scale(block.image, block.size)
                                        block.id = 2
                                        block.dry_timer = Generations.dry_timer
                                        water_sound.play()

                            case 'carrot_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'carrot', block))
                            case 'cabb_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'cabb', block))
                            case 'redis_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'redis', block))
                            case 'garl_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'garl', block))
                                

            for plant in plants:
                to_player_distance = p.Vector2(player.rect.centerx, player.rect.centery).distance_to(p.Vector2(plant.rect.centerx, plant.rect.centery))

                if rpos:
                    if plant.rect.collidepoint(rpos) and to_player_distance <= 200:
                        if inventory.selected_item == None:
                            if plant.quality <= 0:
                                plants.remove(plant)
                            elif plant.quality > 0 and plant.stage == 4:
                                inventory.add_extra_item(f'{plant.type}', f'img/plants/{plant.type}.png')
                                plants.remove(plant)
        rpos = None

        update_day_night()
        
    p.display.flip()
    CLOCK.tick(FPS)