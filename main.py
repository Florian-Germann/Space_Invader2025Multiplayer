import pygame
import pygame_menu
import sys
from random import choice

from functions.enemy import Enemy
from functions.player import Player
from functions.bullet import Bullet
from functions.enemyBullet import EnemyBullet


# initialize pygame
pygame.init()

# Define Screen Size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load background image
image = pygame.image.load("resources/space.jpg")
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

# Load lives image
lives_image = pygame.image.load("resources/heart.png")
lives_image = pygame.transform.scale(lives_image, (20, 20))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Main Game Loop
clock = pygame.time.Clock()

gameState = "menu"
running = True
shot_bullet = False
shotCountdown = 0
enemyFieldWidth = 8
enemyFieldHeight = 4
score = 0
scoreboard = []
lives = 3
playerName = "Player"
enemyShotCountdown = 60  # Reset shot countdown to 60 frames
menu_theme = pygame_menu.themes.THEME_DARK


def gameRunning():
    global shot_bullet, shotCountdown, gameState, running, score, lives, enemyShotCountdown
    # Game logic goes here
    if len(Enemy.giveEnemys()) == 0:
        for line in range(enemyFieldHeight):
            for column in range(enemyFieldWidth):
                hitbox = Enemy.giveHitbox()
                Enemy(hitbox.x + 10, hitbox.y + 10, line, column)

    clock.tick(60)
    screen.fill(BLACK)
    screen.blit(image, (0, 0))  # Draw background image
    # check events (e.g. quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameState = "pause"  # Change the game state to "pause"
    # check for Keystrokes
    keys = pygame.key.get_pressed()
    Player.moveSelf(keys, WIDTH)
    # Bullet shooting mechanism
    if keys[pygame.K_SPACE]:
        if not shot_bullet:
            Player.shootBullet()
            shot_bullet = True
            shotCountdown = 0
    else:
        if shotCountdown > 15:
            shot_bullet = False
            shotCountdown = 0
    shotCountdown += 1

    # Enemy shooting mechanism
    if enemyShotCountdown <= 0:
        Enemy.shootBullet(choice(Enemy.giveEnemys()))
        enemyShotCountdown = 60  # Reset shot countdown to 60 frames
    enemyShotCountdown -= 1

    # move bullets enemys and check for collisions
    Bullet.moveSelf(HEIGHT)
    EnemyBullet.moveSelf(HEIGHT)
    Enemy.moveSelf(HEIGHT, WIDTH)
    if Enemy.detectCollision():
        score += 100

    if Player.detectCollision():
        if lives > 1:
            lives -= 1
        else:
            print("Game Over")
            gameState = "gameover"
    # Draw Player
    Player.drawSelf(screen)
    # move and draw enemies
    Enemy.drawSelf(screen)
    Bullet.drawSelf(screen)
    EnemyBullet.drawSelf(screen)
    # Draw score
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))  # Draw score on the screen
    # Draw lives
    lives_text = font.render("lives:", True, WHITE)
    screen.blit(lives_text, (WIDTH - 100, 10))  # Draw lives text on the screen
    for i in range(lives):
        screen.blit(lives_image, (WIDTH - 100 + i * 25, 40))
    # Draw enemy hitbox
    # hitbox = Enemy.giveHitbox()
    # pygame.draw.rect(screen, RED, hitbox, 2)  # Draw enemy hitbox


def startGame():
    global gameState, shot_bullet, shotCountdown, score, lives, enemyShotCountdown, enemyFieldHeight, enemyFieldWidth
    shot_bullet = False
    shotCountdown = 0
    score = 0
    lives = 3
    enemyShotCountdown = 60  # Reset shot countdown to 60 frames

    Player.clearPlayer()  # Clear the player
    Player(HEIGHT, WIDTH)  # Create a new player
    Enemy.clearEnemys()  # Clear the enemies
    Bullet.clearBullets()  # Clear the bullets
    EnemyBullet.clearBullets()  # Clear the enemy bullets

    for line in range(enemyFieldHeight):
        for column in range(enemyFieldWidth):
            Enemy(10, 20, line, column)
    Enemy.createHitbox(10, 20, enemyFieldWidth, enemyFieldHeight)

    gameState = "game"  # Change the game state to "game"
    menuScreen.disable()  # Disable the menu
    pauseScreen.disable()  # Disable the pause


def continueGame():
    global gameState
    gameState = "game"  # Change the game state to "game"
    pauseScreen.disable()  # Disable the pause menu


def stopGame():
    global running
    running = False  # Stop the game loop
    menuScreen.disable()  # Disable the menu
    pauseScreen.disable()  # Disable the pause menu
    gameoverScreen.disable()  # Disable the game over menu


def openScoreboard():
    menuScreen.disable()  # Disable the menu
    scoreboardScreen.enable()  # Enable the scoreboard
    scoreboardScreen.clear()  # Clear the scoreboard
    scoreboardScreen.add.label('Scoreboard', font_size=40)  # Add a label to the menu7
    scoreboard.sort(key=lambda n: n[1], reverse=True)
    for i in range(len(scoreboard)):
        scoreboardScreen.add.label(f'{i + 1}. {scoreboard[i][0]}: {scoreboard[i][1]}', font_size=20)
    scoreboardScreen.add.button('Back to Menu', gotoMenu)  # Button to go back to the menu
    scoreboardScreen.mainloop(screen)  # Run the scoreboard menu


def gotoMenu():
    global gameState
    gameState = "menu"  # Change the game state to "menu"
    scoreboardScreen.disable()  # Disable the scoreboard
    pauseScreen.disable()  # Disable the pause menu
    gameoverScreen.disable()  # Disable the game over menu


def getName(value):
    global playerName
    playerName = value  # Get the player name from the input field


menuScreen = pygame_menu.Menu('Space Invaders', WIDTH, HEIGHT, theme=menu_theme)
menuScreen.add.label('Welcome to Space Invaders', font_size=40)  # Add a label to the menu
menuScreen.add.button('Play', startGame)  # Button to start the game
menuScreen.add.button('Scoreboard', openScoreboard)  # Button to open the scoreboard
menuScreen.add.button('Quit', stopGame)  # Button to quit the game

scoreboardScreen = pygame_menu.Menu('Scoreboard', WIDTH, HEIGHT, theme=menu_theme)
scoreboardScreen.add.label('Scoreboard', font_size=40)  # Add a label to the menu
scoreboardScreen.add.button('Back to Menu', gotoMenu)  # Button to go back to the menu

pauseScreen = pygame_menu.Menu('Pause', WIDTH, HEIGHT, theme=menu_theme)
pauseScreen.add.label('Game Paused', font_size=40)  # Add a label to the menu
pauseScreen.add.button('Resume', continueGame)  # Button to resume the game
pauseScreen.add.button('Quit', gotoMenu)  # Button to quit the game

gameoverScreen = pygame_menu.Menu('Game Over', WIDTH, HEIGHT, theme=menu_theme)
gameoverScreen.add.label('Game Over', font_size=40)  # Add a label to the menu
gameoverScreen.add.label('Your Score: ' + str(score), font_size=20)  # Add a label to the menu
gameoverScreen.add.image('resources/Explosion.png', scale=(0.1, 0.1))  # Add a game over image
gameoverScreen.add.text_input('Name: ', default='Player', maxchar=10, onchange=getName)  # Input field for player name
gameoverScreen.add.button('Back to Menu', gotoMenu)  # Button to play again

Player(HEIGHT, WIDTH)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    match gameState:
        case "menu":
            pauseScreen.disable()  # Disable the pause menu
            menuScreen.enable()  # Enable the menu
            menuScreen.mainloop(screen)  # Run the menu

        case "game":
            menuScreen.disable()  # Disable the menu
            pauseScreen.disable()  # Disable the pause menu
            gameRunning()

        case "pause":
            menuScreen.disable()  # Disable the menu
            pauseScreen.enable()  # Enable the pause menu
            pauseScreen.mainloop(screen)  # Run the pause menu

        case "gameover":
            menuScreen.disable()  # Disable the menu
            pauseScreen.disable()  # Disable the pause menu
            gameoverScreen.enable()  # Enable the game over menu
            gameoverScreen.mainloop(screen)  # Run the game over menu
            scoreboard.append([playerName, score])  # Add the score to the scoreboard

    pygame.display.update()             # Update the display

pygame.quit()               # Close pygame
sys.exit()                  # Stop the program