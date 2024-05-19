import blackjack as blackjack
import poker as poker
import slapjack as slapjack
import pygame
from pygame.locals import *

icon = pygame.transform.scale(pygame.image.load('resources/ICON.png'), (223, 312))
poker_preview = pygame.transform.scale(pygame.image.load("resources/PREVIEW/POKER.png"), (400, 250))
blackjack_preview = pygame.transform.scale(pygame.image.load("resources/PREVIEW/BLACKJACK.png"), (400, 250))
slapjack_preview = pygame.transform.scale(pygame.image.load("resources/PREVIEW/SLAPJACK.png"), (400, 250))
# menu: the API
black = (0, 0, 0)
white = (255, 255, 255)
green = (19, 85, 52)
def menu():
    pygame.init()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Main Menu')
    screen = pygame.display.set_mode((1024, 768))
    background = pygame.image.load("resources/BG.png")
    screen.blit(background, (0, 0))
    screen.blit(blackjack_preview, (50, 100))
    button_blackjack_x = 50
    button_blackjack_y = 100
    button_blackjack_width = blackjack_preview.get_width()
    button_blackjack_height = blackjack_preview.get_height()
    screen.blit(poker_preview, (550, 100))
    button_poker_x = 550
    button_poker_y = 100
    button_poker_width = poker_preview.get_width()
    button_poker_height = poker_preview.get_height()
    screen.blit(slapjack_preview, (300, 450))
    button_slapjack_x = 300
    button_slapjack_y = 450
    button_slapjack_width = slapjack_preview.get_width()
    button_slapjack_height = slapjack_preview.get_height()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            mouse_x, mouse_y = pygame.mouse.get_pos()
            click, _, _ = pygame.mouse.get_pressed()
            if button_blackjack_x < mouse_x < button_blackjack_x + button_blackjack_width and button_blackjack_y < mouse_y < button_blackjack_y + button_blackjack_height:
                if click:
                    blackjack.blackjack()
            if button_poker_x < mouse_x < button_poker_x + button_poker_width and button_poker_y < mouse_y < button_poker_y + button_poker_height:
                if click:
                    poker.poker()
            if button_slapjack_x < mouse_x < button_slapjack_x + button_slapjack_width and button_slapjack_y < mouse_y < button_slapjack_y + button_slapjack_height:
                if click:
                    slapjack.slapjack()
        pygame.display.update()
    pygame.quit()
    quit()

if __name__ == "__main__":
    menu()
