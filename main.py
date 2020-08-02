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


class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpcount = 10
        self.jump = False

    def draw(self, win):
        # since we have only 9 sprites/movement we set 3 frame = 1 image and walkCount <= 27
        if (self.walkCount+1) >= 27:
            self.walkCount = 0
        # logic to choose character image as per movements
        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(idle, (self.x, self.y))


clock = pygame.time.Clock()


def redrawGameWindow():
    win.blit(bg, (0, 0))
    hero.draw(win)
    pygame.display.update()


hero = player(20, 416, 64, 64)
run = True
# game begins
while run:
    clock.tick(27)  # 27fps. 9 images per movement. 1 move = 3 frames

    for event in pygame.event.get():  # Exiting game
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and hero.x > 0:  # movement control
        hero.x -= hero.vel
        hero.left, hero.right = True, False
        print("L")
    elif keys[pygame.K_RIGHT] and hero.x < (screen_width-hero.width-hero.vel):
        hero.x += hero.vel
        hero.left, hero.right = False, True
        print("R")
    else:
        hero.left, hero.right = False, False
        hero.walkCount = 0

    if not(hero.jump):  # Logic to make a jump and fall back
        if keys[pygame.K_SPACE]:
            hero.jump = True
            hero.left, hero.right = False, False
            hero.walkCount = 0
            print("JUMP")
    else:
        if hero.jumpcount >= -10:
            neg = 1
            if hero.jumpcount < 0:
                neg = -1
            hero.y -= (hero.jumpcount**2)*0.5*neg
            hero.jumpcount -= 1
        else:
            hero.jump = False
            hero.jumpcount = 10

    redrawGameWindow()

pygame.quit()
