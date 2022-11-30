import pygame
import random
from pygame.locals import *

pygame.init()
pygame.font.init()

#inicjalizacja czcionki
myfont = pygame.font.SysFont("MS Comic Sans", 30)
welcome_font = pygame.font.SysFont("MS Comic Sans", 90)

# inicjalizacja
window_width, window_height = 800, 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Om nom nom")

# def kolorów
RED, GREEN, BLUE, WHITE = (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)

# obiekt potwora
monster_width = 100
monster_height = 100
monster = pygame.Rect(  # top, left, bottom, right
    window_width / 2 - monster_width / 2,
    window_height - monster_height,
    monster_width,
    monster_height,
)

# obiekt ciastka
cookie_width = 50
cookie_height = 50

cookies = []

points = 0  # licznik

# muzyka w tle
pygame.mixer.music.load("blue2.mp3")
pygame.mixer.music.play(-1, 0.0)
# efekty dźwiękowe
sounds = ["cookie.mp3", "nomnom.mp3"]

# wczytane grafiki
monster_img = pygame.image.load("monster.png")
monster_img = pygame.transform.scale(monster_img, (monster_width, monster_height))
cookie_img = pygame.image.load("cookie.png")
cookie_img = pygame.transform.scale(cookie_img, (cookie_width, cookie_height))
background_img = pygame.image.load("idylla.png")
background_img = pygame.transform.scale(background_img, (window_width, window_height))

# timer odliczający czas wyzwalania ciastek
COOKIE_RELEASE = 100  # przypisanie identyfikatora w postaci inta do eventu
pygame.time.set_timer(COOKIE_RELEASE, 1000)

# pętla główna gry
velocity = 2

game_on = False

while True:
    window.blit(background_img, (0, 0))  # obraz tła

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    if not game_on:
        welcome_text = welcome_font.render('OM NOM NOM GAME', False, BLUE)
        press_key_text = myfont.render('press space to start cookie game', False, BLUE)
        window.blit(welcome_text, (window_width/2 - welcome_text.get_width() / 2, window_height /3))
        window.blit(press_key_text, (window_width/2 - press_key_text.get_width() / 2, window_height /3 + welcome_text.get_height()))

        for event in events:
            if event.type == QUIT:
                pygame.quit()

        if keys[pygame.K_SPACE]:
            game_on = True

    if game_on:
        for event in events:
            if event.type == COOKIE_RELEASE:
                new_cookie = pygame.Rect(random.randint(0, window_width), 0, cookie_width, cookie_height)
                cookies.append(new_cookie)
            if event.type == QUIT:
                pygame.quit()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if monster.left > 0:
                monster.left -= velocity
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if monster.right < window_width:
                monster.right += velocity

        window.blit(monster_img, monster)

        for cookie in cookies[:]:
            cookie.bottom += 1  # prędkość spadania ciasteczka
            if monster.colliderect(cookie):
                action_sound = pygame.mixer.Sound(random.choice(sounds))
                action_sound.play()
                points += 1
                cookies.remove(cookie)
            elif cookie.bottom >= window_height:
                points -= 1
                cookies.remove(cookie)
            else:
                # pygame.draw.rect(window, GREEN, cookie)
                window.blit(cookie_img, cookie)

        # licznik punktów
        points_text = myfont.render('POINTS: ' + str(points), False, WHITE)
        window.blit(points_text, (window_width * 0.1, window_height - 100))

    pygame.display.update()
