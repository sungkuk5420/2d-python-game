import pygame 

pygame.init()

screen_width = 480
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("KIM Game")

clock = pygame.time.Clock()

background = pygame.image.load('images\\full-bg.png')
background = pygame.transform.scale(background, (1360, 680))

character = pygame.image.load('images\\chracter_top_2x.jpg')
character_left = [
    'images\\chracter_left_1_2x.jpg',
    'images\\chracter_left_2_2x.jpg',
    'images\\chracter_left_3_2x.jpg',
    'images\\chracter_left_4_2x.jpg',
]
character_right = [
    'images\\chracter_right_1_2x.jpg',
    'images\\chracter_right_2_2x.jpg',
    'images\\chracter_right_3_2x.jpg',
    'images\\chracter_right_4_2x.jpg',
]
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width /2 - character_width/2
character_y_pos = screen_height - character_height -90

to_x = 0
to_y = 0

counter = 0

character_speed = 0.4

running = True
keydownEventType = "stop"
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keydownEventType = "left"
                to_x -= character_speed 
                
            elif event.key == pygame.K_RIGHT:
                keydownEventType = "right"
                to_x += character_speed
                
            # elif event.key == pygame.K_UP:
            #     to_y -= 5
            # elif event.key == pygame.K_DOWN:
            #     to_y += 5
        if keydownEventType =="left":
            to_x = -character_speed
        elif keydownEventType =="right":
            to_x = character_speed
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and keydownEventType=="left") or (event.key == pygame.K_RIGHT and keydownEventType=="right"):
                keydownEventType = "stop"
                counter = 0
                character = pygame.image.load('images\\chracter_top_2x.jpg')
                to_x = 0
            # elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #     to_y = 0

    character_x_pos += to_x * dt
    character_y_pos += to_y * dt
    if(keydownEventType == "left"):
        counter = (counter + 1) % len(character_left)
        character = pygame.image.load(character_left[counter])
    elif (keydownEventType == "right"):
        counter = (counter + 1) % len(character_right)
        character = pygame.image.load(character_right[counter])
    

    if character_x_pos <0:
        character_x_pos = 0
    elif character_x_pos >(screen_width-character_width):
        character_x_pos = (screen_width-character_width)

    screen.blit(background,(0,0))

    screen.blit(character,(character_x_pos,character_y_pos))
    pygame.display.update()
    

pygame.quit()