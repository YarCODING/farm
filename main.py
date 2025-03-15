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

    inventory.draw(SCREEN)
    player.draw()

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
        rpos = None
    
    p.display.flip()
    CLOCK.tick()