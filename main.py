from imports import*

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
        'time_of_day': time_of_day
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

        return blocks, plants, inventory, time_of_day
    except FileNotFoundError:
        Generations.offset_x = 0
        Generations.offset_y = 0
        Generations.limit = 0
        for _ in range(510):
            blocks.append(Generations(0))
        return blocks, plants, inventory, 2300


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


blocks, plants, inventory, time_of_day = load_game()

play_btn = behaviors(SCREENSIZE[0]/2-108, SCREENSIZE[1]/2+80, 236, 108, p.image.load('img/ui/play.png'))
exit_btn = behaviors(SCREENSIZE[0]/2-108, SCREENSIZE[1]/2+220, 236, 108, p.image.load('img/ui/exit.png'))

font = p.font.Font('font.ttf', 250)
title_txt = font.render('farm', True, (255, 255, 255))

game = False
menu = True


while True:
    if menu:
        SCREEN.blit(menu_bg, (0, 0))
        SCREEN.blit(title_txt, (SCREENSIZE[0]/2-150, SCREENSIZE[1]/2-300))
        play_btn.draw()
        exit_btn.draw()

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
                
    if game and not menu:
        SCREEN.fill(white)

        for block in blocks:
            block.draw()
            block.dry()

        for plant in plants:
            plant.grow()
            plant.draw()

        player.draw()
        inventory.draw(SCREEN)

        if lpos:
            player.move(lpos)
            if walk_sound_time == 0 and player.state == 'walk':
                walk.play()
                walk_sound_time = random.randint(10, 20)
            walk_sound_time -= 1
        if player.state == 'stand':
            lpos = None
        
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
                        if block.id == 0:
                            if inventory.selected_item == 'shovel':
                                block.image = p.image.load('img/showeled.png')
                                block.image = p.transform.scale(block.image, block.size)
                                block.id = 1
                                shovel_sound.play()
                        elif block.id == 1:
                            if inventory.selected_item == 'shovel':
                                block.image = p.image.load('img/grass_img.png')
                                block.image = p.transform.scale(block.image, block.size)
                                block.id = 0
                                shovel_sound.play()
                            elif inventory.selected_item == 'watercan':
                                block.image = p.image.load('img/watered.png')
                                block.image = p.transform.scale(block.image, block.size)
                                block.id = 2
                                block.dry_timer = Generations.dry_timer
                                water_sound.play()
                        elif block.id == 2:
                            if inventory.selected_item == 'watercan':
                                block.image = p.image.load('img/watered.png')
                                block.image = p.transform.scale(block.image, block.size)
                                block.id = 2
                                block.dry_timer = Generations.dry_timer
                                water_sound.play()
                                        
                        if block.id == 1 or block.id == 2:
                            if  inventory.selected_item == 'carrot_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'carrot', block))
                            elif  inventory.selected_item == 'cabb_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'cabb', block))
                            elif  inventory.selected_item == 'garl_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'garl', block))
                            elif  inventory.selected_item == 'redis_bag':
                                plants.append(Plant(block.rect.x, block.rect.y, 'redis', block))

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
    CLOCK.tick()