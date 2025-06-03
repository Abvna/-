import random
import math
import pygame
from random import randint

pygame.init()

MOVE_SPEED = [1, 3, 2, 4, 3, 5, 4, 6]
SHOT_DELAY = [60, 50, 55, 45, 40, 35, 30, 25]
BULLET_SPEED = [5, 7, 6, 8, 7, 9, 8, 10]
BULLET_DAMAGE = [1, 2, 3, 2, 4, 3, 5, 4]

WIDTH, HEIGHT = 960, 720
FPS = 60
TILE = 32
MAP_WIDTH, MAP_HEIGHT = 2600, 1400

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

play = True

def draw_background():
    start_color = (int(10 * 0.4), int(50 * 0.4), int(10 * 0.4))
    end_color = (int(34 * 0.4), int(177 * 0.4), int(76 * 0.4))

    steps = HEIGHT

    for y in range(steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * y // steps
        g = start_color[1] + (end_color[1] - start_color[1]) * y // steps
        b = start_color[2] + (end_color[2] - start_color[2]) * y // steps
        pygame.draw.line(window, (r, g, b), (0, y), (WIDTH, y))



fontUI = pygame.font.Font(None, 30)


imgBrick = pygame.image.load('res/images/block_brick.png')
imgTanks = [
    pygame.image.load('res/images/tank1.png'),
    pygame.image.load('res/images/tank2.png'),
    pygame.image.load('res/images/tank3.png'),
    pygame.image.load('res/images/tank4.png'),
    pygame.image.load('res/images/tank5.png'),
    pygame.image.load('res/images/tank6.png'),
    pygame.image.load('res/images/tank7.png'),
    pygame.image.load('res/images/tank8.png'),
]
imgBangs = [
    pygame.image.load('res/images/bang1.png'),
    pygame.image.load('res/images/bang2.png'),
    pygame.image.load('res/images/bang3.png'),
]
imgBonuses = [
    pygame.image.load('res/images/bonus_star.png'),
    pygame.image.load('res/images/bonus_tank.png'),
    pygame.image.load('res/images/ammo_box.png')
]


sound_shot = pygame.mixer.Sound('res/sounds/shot.wav')
sound_move = pygame.mixer.Sound('res/sounds/move.wav')
sound_destroy = pygame.mixer.Sound('res/sounds/destroy.wav')
sound_dead = pygame.mixer.Sound('res/sounds/dead.wav')
sound_bonus = pygame.mixer.Sound('res/sounds/star.wav')

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]




class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self, player_tank):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)

                if obj == player_tank:
                    text = fontUI.render(f'Ammo: {obj.ammo}', 1, 'white')
                    window.blit(text, (5, 40))

                i += 1


class Tank:
    def __init__(self, color, px, py, direct, keyList=None, is_ai=False):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = 5
        self.shotTimer = 0

        self.moveSpeed = MOVE_SPEED[0]
        self.shotDelay = SHOT_DELAY[0]
        self.bulletSpeed = BULLET_SPEED[0]
        self.bulletDamage = BULLET_DAMAGE[0]
        self.ammo = 35


        if not is_ai:
            self.keyLEFT = pygame.K_a
            self.keyRIGHT = pygame.K_d
            self.keyUP = pygame.K_w
            self.keyDOWN = pygame.K_s
            self.keySHOT = pygame.K_SPACE

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.is_ai = is_ai
        self.ai_move_timer = 0

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]

        oldX, oldY = self.rect.topleft
        moving = False

        if self.is_ai:
            player_tank = None
            for obj in objects:
                if obj.type == 'tank' and obj != self:
                    player_tank = obj
                    break

            if player_tank:
                dx = player_tank.rect.centerx - self.rect.centerx
                dy = player_tank.rect.centery - self.rect.centery
                distance_to_player = math.sqrt(dx ** 2 + dy ** 2)

                if distance_to_player < 200:
                    if abs(dx) > abs(dy):
                        self.rect.x += self.moveSpeed if dx > 0 else -self.moveSpeed
                        self.direct = 1 if dx > 0 else 3
                    else:
                        self.rect.y += self.moveSpeed if dy > 0 else -self.moveSpeed
                        self.direct = 2 if dy > 0 else 0

                    if distance_to_player < 100 and self.shotTimer == 0:
                        Bullet(self, self.rect.centerx, self.rect.centery,
                               DIRECTS[self.direct][0] * self.bulletSpeed,
                               DIRECTS[self.direct][1] * self.bulletSpeed,
                               self.bulletDamage)
                        sound_shot.play()
                        self.shotTimer = self.shotDelay

                else:
                    if self.ai_move_timer <= 0:
                        self.direct = random.choice([0, 1, 2, 3])
                        self.ai_move_timer = random.randint(30, 60)
                    else:
                        self.ai_move_timer -= 1

                    if self.direct == 0:
                        self.rect.y -= self.moveSpeed
                    elif self.direct == 1:
                        self.rect.x += self.moveSpeed
                    elif self.direct == 2:
                        self.rect.y += self.moveSpeed
                    elif self.direct == 3:
                        self.rect.x -= self.moveSpeed

            if self.shotTimer > 0:
                self.shotTimer -= 1

        else:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            if keys[self.keyLEFT]:
                dx = -self.moveSpeed
                self.direct = 3
                moving = True
            if keys[self.keyRIGHT]:
                dx = self.moveSpeed
                self.direct = 1
                moving = True
            if keys[self.keyUP]:
                dy = -self.moveSpeed
                self.direct = 0
                moving = True
            if keys[self.keyDOWN]:
                dy = self.moveSpeed
                self.direct = 2
                moving = True

            self.rect.x += dx
            self.rect.y += dy

            if keys[self.keySHOT] and self.shotTimer == 0 and self.ammo > 0:
                bullet_dx = DIRECTS[self.direct][0] * self.bulletSpeed
                bullet_dy = DIRECTS[self.direct][1] * self.bulletSpeed

                if dx != 0 and dy != 0:
                    bullet_dx = math.copysign(self.bulletSpeed * 0.7071, dx)
                    bullet_dy = math.copysign(self.bulletSpeed * 0.7071, dy)

                Bullet(self, self.rect.centerx, self.rect.centery, bullet_dx, bullet_dy, self.bulletDamage)
                sound_shot.play()
                self.shotTimer = self.shotDelay
                self.ammo -= 1

        if self.shotTimer > 0:
            self.shotTimer -= 1

        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

    def draw(self):
        window.blit(self.image, camera.apply(self))

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            sound_dead.play()
            print(self.color, 'dead')

class APC:
    pass

class BMP:
    pass

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        self.rect = pygame.Rect(px, py, 4, 4)

    def update(self):
        self.px += self.dx
        self.py += self.dy

        self.rect.center = (self.px, self.py)

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        sound_destroy.play()
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (int(self.px), int(self.py)), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0
        self.rect = pygame.Rect(px, py, 32, 32)

    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=camera.apply(self).center)
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.hp = randint(1, 3)

        self.rect = pygame.Rect(px, py, size, size)

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, camera.apply(self))

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'

        self.bonusNum = bonusNum
        self.image = imgBonuses[bonusNum]

        if self.bonusNum == 2:
            self.image = pygame.transform.scale(self.image, (36, 36))

        self.rect = self.image.get_rect(center=(px, py))
        self.timer = 400

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and obj.rect.colliderect(self.rect):
                sound_bonus.play()
                if self.bonusNum == 0:
                    obj.rank += 1
                    if obj.rank == len(imgTanks):
                        obj.rank = len(imgTanks) - 1
                elif self.bonusNum == 1:
                    obj.hp += 1
                elif self.bonusNum == 2:
                    ammo_count = random.randint(8, 40)
                    obj.ammo += ammo_count
                    print(f'{obj.color} received {ammo_count} ammo!')

                objects.remove(self)

    def draw(self):
        window.blit(self.image, camera.apply(self))


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)


camera = Camera(MAP_WIDTH, MAP_HEIGHT)


bullets = []
objects = []

player_tank = Tank(color='blue', px=100, py=100, direct=0, keyList=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE], is_ai=False)
Tank('red', 650, 275, 0, is_ai=True)
ui = UI()

for _ in range(200):
    while True:
        x = randint(0, MAP_WIDTH // TILE - 1) * TILE
        y = randint(0, MAP_HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True

        if not fined:
            break

    Block(x, y, TILE)


bonusTimer = 180

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()

    if bonusTimer > 0:
        bonusTimer -= 1
    else:
        Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1))
        bonusTimer = randint(120, 240)

    for bullet in bullets:
        bullet.update()

    for obj in objects:
        obj.update()

    ui.update()

    camera.update(player_tank)

    window.fill('black')
    draw_background()

    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()

    ui.draw(player_tank)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()