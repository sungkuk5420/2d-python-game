import pygame 

pygame.init()

#화면 크기
screen_width = 480
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
stage_height = 100
# 게임 제목
pygame.display.set_caption("KIM Game")

# FPS
clock = pygame.time.Clock()

# 배경이미지
background = pygame.image.load('images\\full-bg.png')
background = pygame.transform.scale(background, (1360, 680))

# 게임 캐릭터
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

character_to_x = 0
character_to_y = 0

counter = 0

character_speed = 0.4

# 적 enemy 
enemy_images = [
    pygame.image.load('images\\monster-1.png'),
    pygame.image.load('images\\monster-2.png'),
    pygame.image.load('images\\monster-3.png'),
    pygame.image.load('images\\monster-4.png')
]

enemy_spped_y = [-18,-15,-12,-9] 

enemys =[]

enemys.append({
    "pos_x":50, #공의 x좌표
    "pos_y":50, #공의 y좌표
    "image_index":0,
    "to_x":3, # x축 이동방향 -3면 왼쪽으로 +3면 오른쪽으로
    "to_y":-6, # y축 이동방향
    "init_speed_y" : enemy_spped_y[0]
})

# 무기 weapon 
weapon = pygame.image.load('images\\arrow.png')
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러 발 발사 가능
weapons = []

#무기 속도
weapon_speed = 10

# 폰트 정의
game_font = pygame.font.Font(None,40) #폰트 객체 생성 ( 폰트, 크기 )

#총 시간
total_time = 30

#시간 계산
start_ticks = pygame.time.get_ticks() #시작 tick을 받아옴

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
enemy_to_remove = -1

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
                character_to_x -= character_speed 
            elif event.key == pygame.K_RIGHT:
                keydownEventType = "right"
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                print(character_x_pos)
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
                
            # elif event.key == pygame.K_UP:
            #     character_to_y -= 5
            # elif event.key == pygame.K_DOWN:
            #     character_to_y += 5
        if keydownEventType =="left":
            character_to_x = -character_speed
        elif keydownEventType =="right":
            character_to_x = character_speed
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and keydownEventType=="left") or (event.key == pygame.K_RIGHT and keydownEventType=="right"):
                keydownEventType = "stop"
                counter = 0
                character = pygame.image.load('images\\chracter_top_2x.jpg')
                character_to_x = 0
            # elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #     character_to_y = 0

    #게임 캐릭터 위치 정의
    character_x_pos += character_to_x * dt
    character_y_pos += character_to_y * dt
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
    
    # 무기 위치 조정
    # 100, 200  미사일 발사하게 되면 100은 그대로 y값은 180 160 140 으로 줄어든다..
    # 그래서 w[0]는 x값이므로 그대로 두고 [1]인 y값은 계속 줄여준다
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    #몬스터 위치 정의
    for enemy_index, enemy_value in enumerate(enemys):
        enemy_pos_x = enemy_value["pos_x"]
        enemy_pos_y = enemy_value["pos_y"]
        enemy_image_index = enemy_value["image_index"]

        enemy_size = enemy_images[enemy_index].get_rect().size
        enemy_width = enemy_size[0] - (enemy_size[0]/10)
        enemy_height = enemy_size[1] - (enemy_size[1]/10)

        #가로 벽에 닿았을때 공 이동 방향 변경
        if enemy_pos_x < 0 or enemy_pos_x >  screen_width - enemy_width:
            enemy_value["to_x"] = enemy_value["to_x"] * -1

        # 세로 위치
        print(enemy_value["init_speed_y"])
        if enemy_pos_y >= screen_height - stage_height - enemy_height:
            enemy_value["to_y"] = enemy_value["init_speed_y"]
        else:
            enemy_value["to_y"] += 0.5

        enemy_value["pos_x"] += enemy_value["to_x"]
        enemy_value["pos_y"] += enemy_value["to_y"]


    #충돌 처리를 위한 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos + 10

    
    for enemy_index, enemy_value in enumerate(enemys):
        enemy_pos_x = enemy_value["pos_x"]
        enemy_pos_y = enemy_value["pos_y"]
        enemy_image_index = enemy_value["image_index"]

        enemy_rect = enemy_images[enemy_index].get_rect()
        print(enemy_value["to_x"])
        # 캐릭터 공백때문에 20px씩 여유두고 게임오버
        # if enemy_value["to_x"] >= 0:
        #     enemy_rect.left = enemy_pos_x + 20
        # else:
        #     enemy_rect.left = enemy_pos_x - 20
        enemy_rect.left = enemy_pos_x
        enemy_rect.top = enemy_pos_y
        
        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(enemy_rect):
            running = False

            
        for weapon_index, weapon_value in enumerate(weapons):
            weapon_pos_x = weapon_value[0]
            weapon_pos_y = weapon_value[1]

            # 무기 rect 정보 업데이트

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = enemy_pos_y

            # 무기 충돌 처리
            if weapon_rect.colliderect(enemy_rect):
                weapon_to_remove = weapon_index # 해당 무기 없애기 위한 값 저장
                enemy_to_remove = enemy_index # 해당 무기 없애기 위한 값 저장

        # enemy_width = enemy_size[0]
        # enemy_height = enemy_size[1]

    # 충돌 체크 적 and 무기
    if enemy_to_remove > -1:
        del enemys[enemy_to_remove]
        enemy_to_remove = -1

    if  weapon_to_remove > -1:
        del  weapons[ weapon_to_remove]
        weapon_to_remove = -1
    #     print("충돌함!")
    #     running = False

    # 화면에 그리기

    screen.blit(background,(0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    for index, value in enumerate(enemys):
        enemy_pos_x = value["pos_x"]
        enemy_pos_y = value["pos_y"]
        enemy_image_index = value["image_index"]
        screen.blit(enemy_images[enemy_image_index], (enemy_pos_x,enemy_pos_y))

    screen.blit(character,(character_x_pos,character_y_pos)) #캐릭터 그리기
    # screen.blit(enemy,(enemy_x_pos,enemy_y_pos)) #적 그리기

    # 타이머 집어 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #초로 환산위해서 1000으로 나눔

    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255))  #파라미터는 출력 문자열, ?(무조껀 트루), 글자 색상순으로 입력

    screen.blit(timer, (10, 10))
    
    # 시간종료시 게임종료
    if total_time - elapsed_time <= 0:
        print("게임 종료")
        running = False

    pygame.display.update()
    
# 잠시 대기
pygame.time.delay(2000)

pygame.quit()