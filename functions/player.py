import pygame

from functions.bullet import Bullet
from functions.enemy import Enemy
from functions.enemyBullet import EnemyBullet


class Player():
    def __init__(self, HEIGHT, WIDTH):

        global Self
        player_width = 40
        player_height = 40

        self.rect = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - player_height, player_width, player_height)
        self.image = pygame.transform.scale(pygame.image.load("resources/player.png"), (player_width, player_height))
        Self = self

    def drawSelf(screen):
        screen.blit(Self.image, Self.rect)

    def moveSelf(keys, WIDTH):
        player_speed = 5

        if keys[pygame.K_LEFT] and Self.rect.x > 0:
            Self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and Self.rect.x < WIDTH - Self.rect.width:
            Self.rect.x += player_speed
        if keys[pygame.K_UP] and Self.rect.y > 0:
            Self.rect.y -= player_speed

        Self.rect.x = max(0, min(WIDTH - Self.rect.width, Self.rect.x))

    def shootBullet():
        Bullet(Self.rect.x + Self.rect.width // 2, Self.rect.y - 20)

    def detectCollision():
        for enemy in Enemy.giveEnemys():
            if Self.rect.colliderect(enemy.rect):
                return True
        for bullet in EnemyBullet.giveBullets():
            if Self.rect.colliderect(bullet.rect):
                EnemyBullet.removeBullet(bullet)
                return True
        return False

    def clearPlayer():
        global Self
        Self = None