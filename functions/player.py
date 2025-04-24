import pygame

from functions.bullet import Bullet
from functions.enemy import Enemy
from functions.enemyBullet import EnemyBullet


class Player():
    def __init__(self, position, sprite_type):

        player_width = 40
        player_height = 40

        self.rect = pygame.Rect(position[0], position[1], player_width, player_height)
        if sprite_type == 0:
            self.image = pygame.transform.scale(pygame.image.load("resources/player1.png"), (player_width, player_height))
        elif sprite_type == 1:
            self.image = pygame.transform.scale(pygame.image.load("resources/player2.png"), (player_width, player_height))

    def drawSelf(self, screen):
        screen.blit(self.image, self.rect)

    def moveSelf(self, keys, WIDTH):
        player_speed = 5

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += player_speed

        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def shootBullet(self):
        Bullet(self.rect.x + self.rect.width // 2, self.rect.y - 20)

    def detectCollision(self):
        for enemy in Enemy.giveEnemys():
            if self.rect.colliderect(enemy.rect):
                return True
        for bullet in EnemyBullet.giveBullets():
            if self.rect.colliderect(bullet.rect):
                EnemyBullet.removeBullet(bullet)
                return True
        return False

    def clearPlayer(self):
        self = None
        return self