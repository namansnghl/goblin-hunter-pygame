import pygame
pygame.init()

screen_width = 852
screen_height = 480
# setting window size.
win = pygame.display.set_mode((screen_width, screen_height))
# game window title
pygame.display.set_caption("Goblin Hunter")

# loading character movements
bg = pygame.image.load('img/bg.jpg')
idle = pygame.image.load('img/standing.png')


class player:
    '''
    Creates the main character of game

    Object params:
    x ---> initial x coordinate of player
    y ---> initial y coordinate of player
    width ---> width of player
    height ---> height of player
    jump_height ---> jumping height of player. Default 10
    vel ---> Velocity of player. Default 8

    Methods:
    draw() ---> draws the character movement at location
    '''

    walkRight = list(map(pygame.image.load,
                         '{folder}R1.png {folder}R2.png {folder}R3.png {folder}R4.png {folder}R5.png {folder}R6.png {folder}R7.png {folder}R8.png {folder}R9.png'.format(folder='img/').split()))
    walkLeft = list(map(pygame.image.load,
                        '{folder}L1.png {folder}L2.png {folder}L3.png {folder}L4.png {folder}L5.png {folder}L6.png {folder}L7.png {folder}L8.png {folder}L9.png'.format(folder='img/').split()))

    def __init__(self, x, y, width, height, jump_height=10, vel=8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpcount = jump_height
        self.jump = False
        self.standing = True

    def draw(self, win):
        # since we have only 9 sprites/movement we set 3 frame = 1 image and walkCount <= 27
        if (self.walkCount+1) >= 27:
            self.walkCount = 0

        if not(self.standing):
            # logic to choose character image as per movements
            if self.left:
                win.blit(self.walkLeft[self.walkCount//3], (int(self.x), int(self.y)))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount//3], (int(self.x), int(self.y)))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (int(self.x), int(self.y)))
            else:
                win.blit(self.walkLeft[0], (int(self.x), int(self.y)))


class fire_bullet:
    '''
    Creates the bullets fired

    Object params:
    x ---> initial x coordinate
    y ---> initial y coordinate
    radius ---> bullet size
    color ---> bullet color
    facing ---> direction player is facing while shooting. -1 = left, +1 = right
    vel ---> Velocity of bullet. Default 10

    Methods:
    draw() ---> makes bullet animation
    '''

    def __init__(self, x, y, radius, color, facing, vel=10):
        self.x, self.y, self.facing = x, y, facing
        self.color = color
        self.radius = radius
        self.vel = vel*facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy:
    '''
    Creates the main character of game

    Object params:
    x ---> initial x coordinate of enemy
    y ---> initial y coordinate of enemy
    width ---> width of enemy
    height ---> height of enemy
    end ---> right end position of enemy. Default 10
    vel ---> Velocity of enemy. Default 4

    Methods:
    draw() ---> draws the character movement at location
    moce() ---> enemy movement direction logic
    '''
    walkRight = list(map(pygame.image.load,
                         '{folder}R1E.png {folder}R2E.png {folder}R3E.png {folder}R4E.png {folder}R5E.png {folder}R6E.png {folder}R7E.png {folder}R8E.png {folder}R9E.png {folder}R10E.png {folder}R11E.png'.format(folder='img/').split()))
    walkLeft = list(map(pygame.image.load,
                        '{folder}L1E.png {folder}L2E.png {folder}L3E.png {folder}L4E.png {folder}L5E.png {folder}L6E.png {folder}L7E.png {folder}L8E.png {folder}L9E.png {folder}L10E.png {folder}L11E.png'.format(folder='img/').split()))

    def __init__(self, x, y, width, height, end, vel=4):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = vel
        self.walkCount = 0
        self.path = [self.x, self.end]

    def draw(self, win):
        self.move()
        if (self.walkCount+1) >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (int(self.x), int(self.y)))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (int(self.x), int(self.y)))
            self.walkCount += 1

    def move(self):
        if self.x+self.vel in range(self.path[0], self.path[1]):
            self.x += self.vel
        else:
            self.vel = self.vel * -1
            self.walkCount = 0


def redrawGameWindow():  # function to draw objects on window
    win.blit(bg, (0, 0))
    hero.draw(win)  # hero
    goblin.draw(win)
    for bullet in bullets:  # bullets
        bullet.draw(win)
    pygame.display.update()


clock = pygame.time.Clock()
jump_height = 8
hero = player(20, 416, 64, 64, jump_height, vel=6)
goblin = enemy(0, 420, 64, 64, screen_width-50)
run = True
bullets = []

# game begins
while run:
    clock.tick(27)  # 27fps. 9 images per movement. 1 move = 3 frames

    for event in pygame.event.get():  # Exiting game
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    for bullet in bullets:  # fire bullets
        if bullet.x in range(0, screen_width):
            bullet.x += bullet.vel
        else:  # delete when beyond screen
            bullets.pop(bullets.index(bullet))

    if keys[pygame.K_SPACE] and len(bullets) < 6:  # bullet creation
        if hero.left:
            facing = -1
        else:
            facing = 1
        bullets.append(fire_bullet(
            round(hero.x+hero.width//2),
            round(hero.y+hero.height//2),
            4, (0, 0, 0), facing))

    if keys[pygame.K_LEFT] and hero.x > 0:  # movement control
        hero.x -= hero.vel
        hero.left, hero.right = True, False
        hero.standing = False
    elif keys[pygame.K_RIGHT] and hero.x < (screen_width-hero.width-hero.vel):
        hero.x += hero.vel
        hero.left, hero.right = False, True
        hero.standing = False
    else:
        hero.walkCount = 0
        hero.standing = True

    if not(hero.jump):  # Logic to make a jump and fall back
        if keys[pygame.K_UP]:
            hero.jump = True
            hero.left, hero.right = False, False
            hero.walkCount = 0
    else:
        if hero.jumpcount >= -(jump_height):
            neg = 1
            if hero.jumpcount < 0:
                neg = -1
            hero.y -= (hero.jumpcount**2)*0.5*neg
            hero.jumpcount -= 1
        else:
            hero.jump = False
            hero.jumpcount = jump_height

    redrawGameWindow()

pygame.quit()
