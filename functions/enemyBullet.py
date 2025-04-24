import pygame


class EnemyBullet():
    global enemyBullets
    enemyBullets = []

    global bullet_speed
    bullet_speed = 3

    def __init__(self, x, y):

        bullet_width = 10
        bullet_height = 20

        self.rect = pygame.Rect(x - bullet_width // 2, y, bullet_width, bullet_height)
        self.image = pygame.transform.scale(pygame.image.load("resources/bullet.png"), (bullet_width, bullet_height))
        self.image = pygame.transform.rotate(self.image, 180)

        enemyBullets.append(self)

    def drawSelf(screen):

        for bullet in enemyBullets:
            screen.blit(bullet.image, bullet.rect)

    def moveSelf(HEIGHT):
        for bullet in enemyBullets:
            bullet.rect.y += bullet_speed

            if bullet.rect.y > HEIGHT:
                enemyBullets.remove(bullet)

    def giveBullets():
        return enemyBullets

    def removeBullet(bullet):
        if bullet in enemyBullets:
            enemyBullets.remove(bullet)

    def clearBullets():
        global enemyBullets
        enemyBullets = []