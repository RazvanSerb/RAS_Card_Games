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
    card_pack = {}
    for char in characters:
        card_pack[char] = []
        for value in values:
            card_pack[char].append(load_image(f'resources/CARDS/{value}{char}.png', (223, 312)))
    return card_pack
# Load images
icon = load_image('resources/ICON.png', (223, 312))
cardBack = load_image('resources/CARDS/CARDBACK.png', (223, 312))
cardsPackDictionary = load_cards()
cardsPack = [card for sublist in cardsPackDictionary.values() for card in sublist]
# generateCard: generate a random card from pack
def generateCard(cardsPack):
    card = random.choice(cardsPack)
    cardsPack.remove(card)
    return card
# getCardCharacter: return the character on the card
cardC = cardsPackDictionary['C']
cardR = cardsPackDictionary['R']
cardS = cardsPackDictionary['S']
cardV = cardsPackDictionary['V']
def getCardCharacter(card):
    if card in cardC:
        return "C"
    elif card in cardR:
        return "R"
    elif card in cardS:
        return "S"
    elif card in cardV:
        return "V"
    return "#"
# getCardNumber: return the number on the card
card2 = cardC[1:2] + cardR[1:2] + cardS[1:2] + cardV[1:2]
card3 = cardC[2:3] + cardR[2:3] + cardS[2:3] + cardV[2:3]
card4 = cardC[3:4] + cardR[3:4] + cardS[3:4] + cardV[3:4]
card5 = cardC[4:5] + cardR[4:5] + cardS[4:5] + cardV[4:5]
card6 = cardC[5:6] + cardR[5:6] + cardS[5:6] + cardV[5:6]
card7 = cardC[6:7] + cardR[6:7] + cardS[6:7] + cardV[6:7]
card8 = cardC[7:8] + cardR[7:8] + cardS[7:8] + cardV[7:8]
card9 = cardC[8:9] + cardR[8:9] + cardS[8:9] + cardV[8:9]
card10 = cardC[9:10] + cardR[9:10] + cardS[9:10] + cardV[9:10]
cardJ = cardC[10:11] + cardR[10:11] + cardS[10:11] + cardV[10:11]
cardQ = cardC[11:12] + cardR[11:12] + cardS[11:12] + cardV[11:12]
cardK = cardC[12:13] + cardR[12:13] + cardS[12:13] + cardV[12:13]
cardA = cardC[0:1] + cardR[0:1] + cardS[0:1] + cardV[0:1]
def getCardNumber(card):
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
        return 12
    elif card in cardQ:
        return 13
    elif card in cardK:
        return 14
    elif card in cardA:
        return 15
    return 0
# getCardValue: return the value of the card
def getCardValue(card):
    return [getCardCharacter(card), getCardNumber(card)]
# startGame: return a list of lists of 5 cards generates each for Player and Dealer
def startGame(cardsPack):
    cardsPlayer = []
    cardsDealer = []
    for _ in range(0, 5):
        cardsPlayer.append(generateCard(cardsPack))
        cardsDealer.append(generateCard(cardsPack))
    return [cardsPlayer, cardsDealer]
# finishGame: return the result of the game
def finishGame(cardsPlayer, cardsDealer):
    cardsValuesPlayer = []
    for card in cardsPlayer:
        cardsValuesPlayer.append(getCardValue(card))
    flushPlayer = []
    for character in ["C", "R", "S", "V"]:
        counter = sum(character in cardValue[0] for cardValue in cardsValuesPlayer)
        if counter == 5:
            flushPlayer.append(character)
    highCardValuePlayer = max(cardValue[1] for cardValue in cardsValuesPlayer)
    fourOfAKindPlayer = []
    threeOfAKindPlayer = []
    pairPlayer = []
    for cardNumber in range(2, 16):
        counter = sum(cardNumber == cardValue[1] for cardValue in cardsValuesPlayer)
        if counter == 4:
            fourOfAKindPlayer.append(cardNumber)
        if counter == 3:
            threeOfAKindPlayer.append(cardNumber)
        if counter == 2:
            pairPlayer.append(cardNumber)
    straightPlayer = []
    cardsValuesPlayer = sorted(cardsValuesPlayer, key=lambda x: x[1])
    if (cardsValuesPlayer[0][1] == cardsValuesPlayer[1][1] - 1) or (cardsValuesPlayer[0][1] == 10 and cardsValuesPlayer[1][1] == 12):
        if (cardsValuesPlayer[1][1] == cardsValuesPlayer[2][1] - 1) or (cardsValuesPlayer[1][1] == 10 and cardsValuesPlayer[2][1] == 12):
            if (cardsValuesPlayer[2][1] == cardsValuesPlayer[3][1] - 1) or (cardsValuesPlayer[2][1] == 10 and cardsValuesPlayer[3][1] == 12):
                if (cardsValuesPlayer[3][1] == cardsValuesPlayer[4][1] - 1) or (cardsValuesPlayer[3][1] == 10 and cardsValuesPlayer[4][1] == 12):
                    straightPlayer.append(cardsValuesPlayer[4][1])
    cardsValuesDealer = []
    for card in cardsDealer:
        cardsValuesDealer.append(getCardValue(card))
    flushDealer = []
    for character in ["C", "R", "S", "V"]:
        counter = sum(character in cardValue[0] for cardValue in cardsValuesDealer)
        if counter == 5:
            flushDealer.append(character)
    highCardValueDealer = max(cardValue[1] for cardValue in cardsValuesDealer)
    fourOfAKindDealer = []
    threeOfAKindDealer = []
    pairDealer = []
    for cardNumber in range(2, 16):
        counter = sum(cardNumber == cardValue[1] for cardValue in cardsValuesDealer)
        if counter == 4:
            fourOfAKindDealer.append(cardNumber)
        if counter == 3:
            threeOfAKindDealer.append(cardNumber)
        if counter == 2:
            pairDealer.append(cardNumber)
    straightDealer = []
    cardsValuesDealer = sorted(cardsValuesDealer, key=lambda x: x[1])
    if (cardsValuesDealer[0][1] == cardsValuesDealer[1][1] - 1) or (cardsValuesDealer[0][1] == 10 and cardsValuesDealer[1][1] == 12):
        if (cardsValuesDealer[1][1] == cardsValuesDealer[2][1] - 1) or (cardsValuesDealer[1][1] == 10 and cardsValuesDealer[2][1] == 12):
            if (cardsValuesDealer[2][1] == cardsValuesDealer[3][1] - 1) or (cardsValuesDealer[2][1] == 10 and cardsValuesDealer[3][1] == 12):
                if (cardsValuesDealer[3][1] == cardsValuesDealer[4][1] - 1) or (cardsValuesDealer[3][1] == 10 and cardsValuesDealer[4][1] == 12):
                    straightDealer.append(cardsValuesDealer[4][1])
    handRankPlayer = 10
    handRankDealer = 10
    # Royal Flush
    if len(flushPlayer) == 1 and len(straightPlayer) == 1 and highCardValuePlayer == 15:
        handRankPlayer = 1
    if len(flushPlayer) == 1 and len(straightDealer) == 1 and highCardValueDealer == 15:
        handRankDealer = 1
    if handRankPlayer == handRankDealer == 1:
        return 1
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Straight Flush
    if len(flushPlayer) == 1 and len(straightPlayer) == 1:
        handRankPlayer = 2
    if len(flushPlayer) == 1 and len(straightDealer) == 1:
        handRankDealer = 2
    if handRankPlayer == handRankDealer == 2:
        if straightPlayer[0] >= straightDealer[0]:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Four of a Kind
    if len(fourOfAKindPlayer) == 1:
        handRankPlayer = 3
    if len(fourOfAKindDealer) == 1:
        handRankDealer = 3
    if handRankPlayer == handRankDealer == 3:
        if fourOfAKindPlayer[0] > fourOfAKindDealer[0]:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Full House
    if len(threeOfAKindPlayer) == 1 and len(pairPlayer) == 1:
        handRankPlayer = 4
    if len(threeOfAKindDealer) == 1 and len(pairDealer) == 1:
        handRankDealer = 4
    if handRankPlayer == handRankDealer == 4:
        if threeOfAKindPlayer[0] > threeOfAKindDealer[0]:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Flush
    if len(flushPlayer) == 1:
        handRankPlayer = 5
    if len(flushDealer) == 1:
        handRankDealer = 5
    if handRankPlayer == handRankDealer == 5:
        if highCardValuePlayer >= highCardValueDealer:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Straight
    if len(straightPlayer) == 1:
        handRankPlayer = 6
    if len(straightDealer) == 1:
        handRankDealer = 6
    if handRankPlayer == handRankDealer == 6:
        if straightPlayer[0] >= straightDealer[0]:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Three of a Kind
    if len(threeOfAKindPlayer) == 1:
        handRankPlayer = 7
    if len(threeOfAKindDealer) == 1:
        handRankDealer = 7
    if handRankPlayer == handRankDealer == 7:
        if threeOfAKindPlayer[0] > threeOfAKindDealer[0]:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Two pair
    if len(pairPlayer) == 2:
        handRankPlayer = 8
    if len(pairDealer) == 2:
        handRankDealer = 8
    if handRankPlayer == handRankDealer == 8:
        if max(pairPlayer) > max(pairDealer):
            return 1
        elif max(pairPlayer) < max(pairDealer):
            return 0
        elif sum(pairPlayer) > sum(pairDealer):
            return 1
        elif sum(pairPlayer) < sum(pairDealer):
            return 0
        elif highCardValuePlayer >= highCardValueDealer:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # Pair
    if len(pairPlayer) == 1:
        handRankPlayer = 9
    if len(pairDealer) == 1:
        handRankDealer = 9
    if handRankPlayer == handRankDealer == 9:
        if pairPlayer[0] > pairDealer[0]:
            return 1
        elif pairPlayer[0] < pairDealer[0]:
            return 0
        elif highCardValuePlayer >= highCardValueDealer:
            return 1
        return 0
    elif handRankPlayer < handRankDealer:
        return 1
    elif handRankDealer < handRankPlayer:
        return 0
    # High card
    if highCardValuePlayer >= highCardValueDealer:
        return 1
    return 0
# poker: the game API
black = (0, 0, 0)
white = (255, 255, 255)
green = (19, 85, 52)
def poker():
    pygame.init()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Poker')
    screen = pygame.display.set_mode((1024, 768))
    background = pygame.image.load("resources/BG.png")
    font = pygame.font.Font("resources/Arial.ttf", 42)
    MenuButton = pygame.draw.rect(background, green, (700, 670, 300, 50))
    MenuText = font.render('Main Menu', 1, black)
    ChangeButton = pygame.draw.rect(background, green, (20, 330, 150, 60))
    ChangeText = font.render('Change', 1, white)
    StandButton = pygame.draw.rect(background, green, (190, 330, 150, 60))
    StandText = font.render('Stand', 1, white)
    pygame.draw.rect(background, green, (700, 10, 300, 200))
    card1Button = pygame.draw.rect(background, green, (10, 400, 110, 312))
    card2Button = pygame.draw.rect(background, green, (120, 400, 110, 312))
    card3Button = pygame.draw.rect(background, green, (230, 400, 110, 312))
    card4Button = pygame.draw.rect(background, green, (340, 400, 110, 312))
    card5Button = pygame.draw.rect(background, green, (450, 400, 223, 312))
    BGCopy = copy.copy(background)
    numWins = 0
    numLosses = 0
    if True:
        cardsPackCopy = copy.copy(cardsPack)
        [cardsPlayer, cardsDealer] = startGame(cardsPackCopy)
        card1Changed = False
        card2Changed = False
        card3Changed = False
        card4Changed = False
        card5Changed = False
        Stand = False
        GameOver = False
        screen.blit(background, (0, 0))
        screen.blit(ChangeText, (20, 330))
        screen.blit(StandText, (210, 330))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and MenuButton.collidepoint(pygame.mouse.get_pos()):
                menu.menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand or card1Changed) and card1Button.collidepoint(pygame.mouse.get_pos()):
                for card in cardsPlayer:
                    if (cardsPlayer.index(card) != 0):
                        x = 10 + cardsPlayer.index(card) * 110
                        screen.blit(card, (x, 400))
                    else:
                        screen.blit(cardBack, (10, 400))
                pygame.display.update()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and ChangeButton.collidepoint(pygame.mouse.get_pos()):
                            cardsPlayer[0] = generateCard(cardsPackCopy)
                            card1Changed = True
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and card1Button.collidepoint(pygame.mouse.get_pos()):
                            running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand or card2Changed) and card2Button.collidepoint(pygame.mouse.get_pos()):
                for card in cardsPlayer:
                    if (cardsPlayer.index(card) != 1):
                        x = 10 + cardsPlayer.index(card) * 110
                        screen.blit(card, (x, 400))
                    else:
                        screen.blit(cardBack, (120, 400))
                pygame.display.update()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and ChangeButton.collidepoint(pygame.mouse.get_pos()):
                            cardsPlayer[1] = generateCard(cardsPackCopy)
                            card2Changed = True
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and card2Button.collidepoint(pygame.mouse.get_pos()):
                            running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand or card3Changed) and card3Button.collidepoint(pygame.mouse.get_pos()):
                for card in cardsPlayer:
                    if (cardsPlayer.index(card) != 2):
                        x = 10 + cardsPlayer.index(card) * 110
                        screen.blit(card, (x, 400))
                    else:
                        screen.blit(cardBack, (230, 400))
                pygame.display.update()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and ChangeButton.collidepoint(pygame.mouse.get_pos()):
                            cardsPlayer[2] = generateCard(cardsPackCopy)
                            card3Changed = True
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and card3Button.collidepoint(pygame.mouse.get_pos()):
                            running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand or card4Changed) and card4Button.collidepoint(pygame.mouse.get_pos()):
                for card in cardsPlayer:
                    if (cardsPlayer.index(card) != 3):
                        x = 10 + cardsPlayer.index(card) * 110
                        screen.blit(card, (x, 400))
                    else:
                        screen.blit(cardBack, (340, 400))
                pygame.display.update()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and ChangeButton.collidepoint(pygame.mouse.get_pos()):
                            cardsPlayer[3] = generateCard(cardsPackCopy)
                            card4Changed = True
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and card4Button.collidepoint(pygame.mouse.get_pos()):
                            running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand or card5Changed) and card5Button.collidepoint(pygame.mouse.get_pos()):
                for card in cardsPlayer:
                    if (cardsPlayer.index(card) != 4):
                        x = 10 + cardsPlayer.index(card) * 110
                        screen.blit(card, (x, 400))
                    else:
                        screen.blit(cardBack, (450, 400))
                pygame.display.update()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and ChangeButton.collidepoint(pygame.mouse.get_pos()):
                            cardsPlayer[4] = generateCard(cardsPackCopy)
                            card5Changed = True
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and card5Button.collidepoint(pygame.mouse.get_pos()):
                            running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not (GameOver or Stand or card1Changed or card2Changed or card3Changed or card4Changed or card5Changed) and ChangeButton.collidepoint(pygame.mouse.get_pos()):
                cardsPlayer[0] = generateCard(cardsPackCopy)
                cardsPlayer[1] = generateCard(cardsPackCopy)
                cardsPlayer[2] = generateCard(cardsPackCopy)
                cardsPlayer[3] = generateCard(cardsPackCopy)
                cardsPlayer[4] = generateCard(cardsPackCopy)
                Stand = True
                if finishGame(cardsPlayer, cardsDealer) == 1:
                    numWins = numWins + 1
                else:
                    numLosses = numLosses + 1
                GameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not GameOver and StandButton.collidepoint(pygame.mouse.get_pos()):
                Stand = True
                if finishGame(cardsPlayer, cardsDealer) == 1:
                    numWins = numWins + 1
                else:
                    numLosses = numLosses + 1
                GameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN and GameOver and RestartButton.collidepoint(pygame.mouse.get_pos()):
                cardsPackCopy = copy.copy(cardsPack)
                [cardsPlayer, cardsDealer] = startGame(cardsPackCopy)
                card1Changed = False
                card2Changed = False
                card3Changed = False
                card4Changed = False
                card5Changed = False
                Stand = False
                GameOver = False
        screen.blit(background, (0, 0))
        screen.blit(MenuText, (750, 665))
        screen.blit(ChangeText, (20, 330))
        screen.blit(StandText, (210, 330))
        WinsText = font.render('Wins: %i' % numWins, 1, black)
        screen.blit(WinsText, (790, 35))
        LossesText = font.render('Losses: %i' % numLosses, 1, black)
        screen.blit(LossesText, (770, 105))
        for card in cardsDealer:
            x = 10 + cardsDealer.index(card) * 110
            screen.blit(cardBack, (x, 10))
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
    poker()
