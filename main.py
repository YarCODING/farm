from imports import*

p.mixer.music.load('music.mp3')
p.mixer.music.set_volume(0.1)
# p.mixer.music.set_endevent(p.USEREVENT)
p.mixer.music.play(-1)

lpos = None
rpos = None

while True:
    SCREEN.fill(white)

    for block in blocks:
        block.draw()
    for plant in plants:
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
            p.quit()
            sys.exit()
        elif event.type == p.USEREVENT:
                p.mixer.music.play()
        if event.type == p.MOUSEBUTTONDOWN and event.button == 3:
            rpos = event.pos
        if event.type == p.KEYDOWN:
            if p.K_1 <= event.key <= p.K_8:
                slot_index = event.key - p.K_1
                inventory.select_slot(slot_index)
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
                            water_sound.play()
                        elif  inventory.selected_item == 'carrot_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'carrot'))
                        elif  inventory.selected_item == 'cabb_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'cabb'))
                        elif  inventory.selected_item == 'garl_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'garl'))
                        elif  inventory.selected_item == 'redis_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'redis'))
                        
                    elif block.id == 2:
                        if inventory.selected_item == 'carrot_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'carrot'))
                        elif  inventory.selected_item == 'cabb_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'cabb'))
                        elif  inventory.selected_item == 'garl_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'garl'))
                        elif  inventory.selected_item == 'redis_bag':
                            plants.append(Plant(block.rect.centerx - 48 // 2, block.rect.centery - 48 // 2, 'redis'))
        rpos = None
    
    p.display.flip()
    CLOCK.tick()