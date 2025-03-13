from imports import*

p.mixer.music.load('music.mp3')
p.mixer.music.set_volume(0.1)
# p.mixer.music.set_endevent(p.USEREVENT)
p.mixer.music.play(-1)

while True:
    SCREEN.fill(white)

    for block in blocks:
        block.draw()

    player.draw()
    #player.move(pos)
    player.animate()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        elif event.type == p.USEREVENT:
                p.mixer.music.play()
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            print(pos)
        
        for block in blocks:
             if block.rect.collidepoint(pos):
                block.image = p.image.load('img/showeled.png')
                block.id = 15
        
    
    p.display.flip()
    CLOCK.tick()