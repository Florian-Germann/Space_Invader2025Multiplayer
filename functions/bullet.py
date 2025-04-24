import pygame


class Bullet():
    global bullets
    bullets = []

    global bullet_speed
    bullet_speed = 5

    def __init__(self, x, y):

        bullet_width = 20
        bullet_height = 40

        self.rect = pygame.Rect(x - bullet_width // 2, y, bullet_width, bullet_height)
        self.image = pygame.transform.scale(pygame.image.load("resources/bullet.png"), (bullet_width, bullet_height))

        bullets.append(self)

    def drawSelf(screen):

        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect)

    def moveSelf(HEIGHT):
        for bullet in bullets:
            bullet.rect.y -= bullet_speed

            if bullet.rect.y < 0:
                bullets.remove(bullet)

    def giveBullets():
        return bullets

    def removeBullet(bullet):
        if bullet in bullets:
            bullets.remove(bullet)

    def clearBullets():
        global bullets
        bullets = []