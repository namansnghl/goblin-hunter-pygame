import pygame
pygame.init()

screen_width = 852
screen_height = 480
# setting window size.
win = pygame.display.set_mode((screen_width, screen_height))
# game window title
pygame.display.set_caption("Goblin Hunter - 1st game")

# loading character movements
walkRight = list(map(pygame.image.load,
                     '{folder}R1.png {folder}R2.png {folder}R3.png {folder}R4.png {folder}R5.png {folder}R6.png {folder}R7.png {folder}R8.png {folder}R9.png'.format(folder='img/').split()))
walkLeft = list(map(pygame.image.load,
                    '{folder}L1.png {folder}L2.png {folder}L3.png {folder}L4.png {folder}L5.png {folder}L6.png {folder}L7.png {folder}L8.png {folder}L9.png'.format(folder='img/').split()))
bg = pygame.image.load('img/bg.jpg')
idle = pygame.image.load('img/standing.png')


x, y, width, height, vel = 20, 416, 64, 64, 8
left, right = False, False
walkCount = 0
run = True
jumpcount = 10
jump = False

clock = pygame.time.Clock()


def redrawGameWindow():
    global walkCount
    win.blit(bg, (0, 0))

    # since we have only 9 sprites/movement we set 3 frame = 1 image and walkCount <= 27
    if (walkCount+1) >= 27:
        walkCount = 0

    # logic to choose character image as per movements
    if left:
        win.blit(walkLeft[walkCount//3], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x, y))
        walkCount += 1
    else:
        win.blit(idle, (x, y))

    pygame.display.update()


# game begins
while run:
    clock.tick(27)  # 27fps. 9 images per movement. 1 move = 3 frames

    for event in pygame.event.get():  # Exiting game
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:  # movement control
        x -= vel
        left, right = True, False
        print("LEFT")
    elif keys[pygame.K_RIGHT] and x < (screen_width-width-vel):
        x += vel
        left, right = False, True
        print("RIGHT")
    else:
        left, right = False, False
        walkCount = 0

    if not(jump):  # Logic to make a jump and fall back
        if keys[pygame.K_SPACE]:
            jump = True
            left, right = False, False
            walkCount = 0
            print("JUMP")
    else:
        if jumpcount >= -10:
            neg = 1
            if jumpcount < 0:
                neg = -1
            y -= (jumpcount**2)*0.5*neg
            jumpcount -= 1
        else:
            jump = False
            jumpcount = 10

    redrawGameWindow()

pygame.quit()
