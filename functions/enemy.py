import pygame
from functions.bullet import Bullet
from functions.enemyBullet import EnemyBullet


class Enemy():
    global enemys
    enemys = []

    global hitbox, enemy_speed, direction, enemy_color, enemy_width, enemy_height, enemy_spacing, enemy_speed_y
    hitbox = None
    direction = 1  # 1 for right, -1 for left
    enemy_speed = 1
    enemy_speed_y = 8
    enemy_color = [0, 0, 255]
    enemy_width = 30
    enemy_height = 30
    enemy_spacing = 20

    def __init__(self, x, y, line, column):
        global enemy_width, enemy_height, enemy_spacing

        self.rect = pygame.Rect(x + column * enemy_spacing + column * enemy_width, y + line * enemy_spacing + line * enemy_height, enemy_width, enemy_height)
        self.image = pygame.transform.scale(pygame.image.load("resources/enemy.png"), (enemy_width, enemy_height))

        enemys.append(self)

    def createHitbox(x, y, width, height):
        global hitbox, enemy_width, enemy_height, enemy_spacing
        hitbox = pygame.Rect(x - 10, y - 10, width * enemy_width + width * enemy_spacing + 10, height * enemy_height + height * enemy_spacing + 10)
        return hitbox

    def giveHitbox():
        global hitbox
        return hitbox

    def detectCollision():
        collision = False
        if len(enemys) == 0:
            return
        for enemy in enemys:
            for bullet in Bullet.giveBullets():
                # Check for collision between enemy and bullet
                if enemy.rect.colliderect(bullet.rect):
                    enemys.remove(enemy)
                    Bullet.removeBullet(bullet)
                    collision = True
        if collision:
            return True

    def drawSelf(screen):

        for enemy in enemys:
            screen.blit(enemy.image, enemy.rect)

    def moveSelf(HEIGHT, WIDTH):
        global direction, enemy_speed, hitbox, enemy_speed_y
        if direction == 1:
            for enemy in enemys:
                enemy.rect.x += enemy_speed
                if hitbox.x + hitbox.width > WIDTH and direction == 1:
                    direction = -1
                    for e in enemys:
                        e.rect.y += enemy_speed_y
                    hitbox.y += enemy_speed_y
            hitbox.x += enemy_speed

        elif direction == -1:
            for enemy in enemys:
                enemy.rect.x -= enemy_speed
                if hitbox.x < 0 and direction == -1:
                    direction = 1
                    for e in enemys:
                        e.rect.y += enemy_speed_y
                    hitbox.y += enemy_speed_y
            hitbox.x -= enemy_speed

    def giveEnemys():
        return enemys

    def shootBullet(enemy):
        if enemy in enemys:
            EnemyBullet(enemy.rect.x, enemy.rect.y + enemy_height)

    def clearEnemys():
        global enemys, hitbox
        enemys = []
        hitbox = None