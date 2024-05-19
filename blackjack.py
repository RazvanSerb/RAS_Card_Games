import menu as menu
import pygame
from pygame.locals import *
import random
import copy

def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)
def load_cards():
    characters = ['C', 'R', 'S', 'V']
    values = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '13', '14']
    card_pack = []
    for value in values:
        for char in characters:
            card_pack.append(load_image(f'resources/CARDS/{value}{char}.png', (223, 312)))
    return card_pack
# Load images
icon = load_image('resources/ICON.png', (223, 312))
cardBack = load_image('resources/CARDS/CARDBACK.png', (223, 312))
cardsPack = load_cards()
# Cards categorization
card2 = cardsPack[1:5]
card3 = cardsPack[5:9]
card4 = cardsPack[9:13]
card5 = cardsPack[13:17]
card6 = cardsPack[17:21]
card7 = cardsPack[21:25]
card8 = cardsPack[25:29]
card9 = cardsPack[29:33]
card10 = cardsPack[33:37]
cardJ = cardsPack[37:41]
cardQ = cardsPack[41:45]
cardK = cardsPack[45:49]
cardA = cardsPack[0:1] + cardsPack[12:13] + cardsPack[24:25] + cardsPack[36:37]
# generateCard: generate a random card from pack
def generateCard(cardsPack):
    card = random.choice(cardsPack)
    cardsPack.remove(card)
    return card
# getCardValue: return the value of the card
def getCardValue(card):
    if card in card2:
        return 2
    elif card in card3:
        return 3
    elif card in card4:
        return 4
    elif card in card5:
        return 5
    elif card in card6:
        return 6
    elif card in card7:
        return 7
    elif card in card8:
        return 8
    elif card in card9:
        return 9
    elif card in card10:
        return 10
    elif card in cardJ:
        return 10
    elif card in cardQ:
        return 10
    elif card in cardK:
        return 10
    elif card in cardA:
        return 11
    return 0
# startGame: return a list of lists of 2 cardsPack generates each for Player and Dealer
def startGame(cardsPack):
    cardsPlayer = []
    numCardAPlayer = 0
    cardsDealer = []
    numCardADealer = 0
    for _ in range(0, 2):
        cardPlayer = generateCard(cardsPack)
        if cardPlayer in cardA:
            numCardAPlayer += 1
        cardsPlayer.append(cardPlayer)
        cardDealer = generateCard(cardsPack)
        if cardDealer in cardA:
            numCardADealer += 1
        cardsDealer.append(cardDealer)
    return [[cardsPlayer, numCardAPlayer], [cardsDealer, numCardADealer]]
# finishGame: return the result of the game
def finishGame(sumCardsPlayer, sumCardsDealer):
    if sumCardsPlayer > 21:
        return 0
    if sumCardsDealer > 21:
        return 1
    if sumCardsPlayer >= sumCardsDealer:
        return 1
    return 0
# blackjack: the game API
black = (0, 0, 0)
white = (255, 255, 255)
green = (19, 85, 52)
def blackjack():
    pygame.init()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Blackjack')
    screen = pygame.display.set_mode((1024, 768))
    background = pygame.image.load("resources/BG.png")
    font = pygame.font.Font("resources/Arial.ttf", 42)
    MenuButton = pygame.draw.rect(background, green, (700, 670, 300, 50))
    MenuText = font.render('Main Menu', 1, black)
    HitButton = pygame.draw.rect(background, green, (20, 330, 150, 60))
    HitText = font.render('Hit', 1, white)
    StandButton = pygame.draw.rect(background, green, (190, 330, 150, 60))
    StandText = font.render('Stand', 1, white)
    pygame.draw.rect(background, green, (700, 10, 300, 200))
    BGCopy = copy.copy(background)
    numWins = 0
    numLosses = 0
    if True:
        cardsPackCopy = copy.copy(cardsPack)
        [[cardsPlayer, numCardAPlayer], [cardsDealer, numCardADealer]] = startGame(cardsPackCopy)
        sumCardsPlayer = getCardValue(cardsPlayer[0]) + getCardValue(cardsPlayer[1])
        sumCardsDealer = getCardValue(cardsDealer[0]) + getCardValue(cardsDealer[1])
        Stand = False
        GameOver = False
        screen.blit(background, (0, 0))
        screen.blit(HitText, (70, 330))
        screen.blit(StandText, (210, 330))
        if len(cardsPlayer) == 2 and sumCardsPlayer == 21:
            while sumCardsDealer < 17:
                card = generateCard(cardsPackCopy)
                cardsDealer.append(card)
                numCardADealer += card in cardA
                sumCardsDealer += getCardValue(card)
                while sumCardsDealer > 21 and numCardADealer > 0:
                    numCardADealer -= 1
                    sumCardsDealer -= 10
            if finishGame(sumCardsPlayer, sumCardsDealer) == 1:
                numWins = numWins + 1
            else:
                numLosses = numLosses + 1
            GameOver = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and MenuButton.collidepoint(pygame.mouse.get_pos()):
                menu.menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand) and HitButton.collidepoint(pygame.mouse.get_pos()):
                card = generateCard(cardsPackCopy)
                cardsPlayer.append(card)
                numCardAPlayer += card in cardA
                sumCardsPlayer += getCardValue(card)
                while sumCardsPlayer > 21 and numCardAPlayer > 0:
                    numCardAPlayer -= 1
                    sumCardsPlayer -= 10
                if len(cardsPlayer) >= 5 or (sumCardsPlayer >= 21 and numCardAPlayer == 0):
                    while sumCardsDealer < 17:
                        card = generateCard(cardsPackCopy)
                        cardsDealer.append(card)
                        numCardADealer += card in cardA
                        sumCardsDealer += getCardValue(card)
                        while sumCardsDealer > 21 and numCardADealer > 0:
                            numCardADealer -= 1
                            sumCardsDealer -= 10
                    if finishGame(sumCardsPlayer, sumCardsDealer) == 1:
                        numWins = numWins + 1
                    else:
                        numLosses = numLosses + 1
                    GameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not GameOver and StandButton.collidepoint(pygame.mouse.get_pos()):
                Stand = True
                while len(cardsDealer) <= 5 and sumCardsDealer < 17:
                    card = generateCard(cardsPackCopy)
                    cardsDealer.append(card)
                    numCardADealer += card in cardA
                    sumCardsDealer += getCardValue(card)
                    while sumCardsDealer > 21 and numCardADealer > 0:
                        numCardADealer -= 1
                        sumCardsDealer -= 10
                if finishGame(sumCardsPlayer, sumCardsDealer) == 1:
                    numWins = numWins + 1
                else:
                    numLosses = numLosses + 1
                GameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN and GameOver and RestartButton.collidepoint(pygame.mouse.get_pos()):
                cardsPackCopy = copy.copy(cardsPack)
                [[cardsPlayer, numCardAPlayer], [cardsDealer, numCardADealer]] = startGame(cardsPackCopy)
                sumCardsPlayer = getCardValue(cardsPlayer[0]) + getCardValue(cardsPlayer[1])
                sumCardsDealer = getCardValue(cardsDealer[0]) + getCardValue(cardsDealer[1])
                Stand = False
                GameOver = False
                if len(cardsPlayer) == 2 and sumCardsPlayer == 21:
                    while sumCardsDealer < 17:
                        card = generateCard(cardsPackCopy)
                        cardsDealer.append(card)
                        numCardADealer += card in cardA
                        sumCardsDealer += getCardValue(card)
                        while sumCardsDealer > 21 and numCardADealer > 0:
                            numCardADealer -= 1
                            sumCardsDealer -= 10
                    if finishGame(sumCardsPlayer, sumCardsDealer) == 1:
                        numWins = numWins + 1
                    else:
                        numLosses = numLosses + 1
                    GameOver = True
        screen.blit(background, (0, 0))
        screen.blit(MenuText, (750, 665))
        screen.blit(HitText, (70, 330))
        screen.blit(StandText, (210, 330))
        WinsText = font.render('Wins: %i' % numWins, 1, black)
        screen.blit(WinsText, (790, 35))
        LossesText = font.render('Losses: %i' % numLosses, 1, black)
        screen.blit(LossesText, (770, 105))
        for card in cardsDealer:
            x = 10 + cardsDealer.index(card) * 110
            screen.blit(card, (x, 10))
        screen.blit(cardBack, (120, 10))
        for card in cardsPlayer:
            x = 10 + cardsPlayer.index(card) * 110
            screen.blit(card, (x, 400))
        if GameOver:
            for card in cardsDealer:
                x = 10 + cardsDealer.index(card) * 110
                screen.blit(card, (x, 10))
            GameOverText = font.render('GAME OVER', 1, black)
            screen.blit(GameOverText, (400, 330))
            RestartButton = pygame.draw.rect(background, green, (700, 600, 300, 50))
            RestartText = font.render('Restart', 1, black)
            screen.blit(RestartText, (785, 595))
            background = copy.copy(BGCopy)
        pygame.display.update()

if __name__ == '__main__':
    blackjack()
