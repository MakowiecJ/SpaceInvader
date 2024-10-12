import pygame
import random
import math

pygame.init()

# Tworzenie okna
screen = pygame.display.set_mode((800, 600))

# Tytul i ikona
pygame.display.set_caption("Space Invadors")
ikona = pygame.image.load("spaceship.png")
pygame.display.set_icon(ikona)

# Tlo
tlo = pygame.image.load("tlo2.png")

# Gracz
gracz_img = pygame.image.load("gracz.png")
gracz_x = 370
gracz_x_zmiana = 0
gracz_y = 480

# Wrog
wrog_img = []
wrog_x = []
wrog_x_zmiana = []
wrog_y = []
wrog_y_zmiana = []
liczba_wrogow = 6

for i in range(liczba_wrogow):
    wrog_img.append(pygame.image.load("wrog.png"))
    wrog_x.append(random.randint(0, 736))
    wrog_x_zmiana.append(3)
    wrog_y.append(random.randint(64, 128))
    wrog_y_zmiana.append(75)

# rakieta
rakieta_img = pygame.image.load("rakieta.png")
rakieta_x = 0
rakieta_x_zmiana = 0
rakieta_y = gracz_y
rakieta_y_zmiana = 8
rakieta_stan = "gotowa"

# Wynik
punkty = 0
font = pygame.font.Font("freesansbold.ttf", 32)
tekst_x = 10
tekst_y = 10

# Game over tekst
over_font = pygame.font.Font("freesansbold.ttf", 64)


def pokaz_wynik(x, y):
    wynik = font.render("Wynik: " + str(punkty), True, (255, 255, 255))
    screen.blit(wynik, (x, y))


def pokaz_game_over():
    over_tekst = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_tekst, (200, 250))


def gracz(x, y):
    screen.blit(gracz_img, (x, y))


def wrog(x, y, i):
    screen.blit(wrog_img[i], (x, y))


def rakieta_strzal(x, y):
    global rakieta_stan
    rakieta_stan = "strzal"
    screen.blit(rakieta_img, (x + 16, y - 10))


def if_kolizja(wrog_x, wrog_y, rakieta_x, rakieta_y):
    dystans = math.sqrt(math.pow((wrog_x - rakieta_x), 2) + math.pow((wrog_y - rakieta_y), 2))
    if dystans <= 27:
        return True
    else:
        return False


running = True
while running:
    screen.blit(tlo, (0, 0))

    # Wyjscie z programu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                print("ESCAPE")
                running = False
            # Sterowanie
            if event.key == pygame.K_LEFT:
                gracz_x_zmiana = -4
            if event.key == pygame.K_RIGHT:
                gracz_x_zmiana = 4
            if event.key == pygame.K_SPACE:
                if rakieta_stan is "gotowa":
                    rakieta_x = gracz_x
                    rakieta_strzal(rakieta_x, rakieta_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                gracz_x_zmiana = 0

    gracz_x += gracz_x_zmiana
    # Ograniczenie ruchu
    if gracz_x <= 0:
        gracz_x = 0
    elif gracz_x >= 736:
        gracz_x = 736

    # Ruch wroga
    for i in range(liczba_wrogow):

        # Game over
        if wrog_y[i] > 440:
            for k in range(liczba_wrogow):
                wrog_y[k] = 1000
            pokaz_game_over()
            break

        wrog_x[i] += wrog_x_zmiana[i]
        if wrog_x[i] <= 0:
            wrog_x_zmiana[i] *= -1
            wrog_y[i] += wrog_y_zmiana[i]
        elif wrog_x[i] >= 736:
            wrog_x_zmiana[i] *= -1
            wrog_y[i] += wrog_y_zmiana[i]
        # Kolizja
        kolizja = if_kolizja(wrog_x[i], wrog_y[i], rakieta_x, rakieta_y)
        if kolizja:
            rakieta_y = gracz_y
            rakieta_stan = "gotowa"
            punkty += 1
            wrog_x[i] = random.randint(0, 736)
            wrog_y[i] = random.randint(32, 100)
        wrog(wrog_x[i], wrog_y[i], i)

    # Ruch rakiety
    if rakieta_y <= -32:
        rakieta_y = gracz_y
        rakieta_stan = "gotowa"
    if rakieta_stan is "strzal":
        rakieta_strzal(rakieta_x, rakieta_y)
        rakieta_y -= rakieta_y_zmiana

    gracz(gracz_x, gracz_y)
    pokaz_wynik(tekst_x, tekst_y)
    pygame.display.update()
