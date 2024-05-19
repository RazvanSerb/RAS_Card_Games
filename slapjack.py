import pygame
import random
import menu as menu
from enum import Enum

Symbol = Enum('Symbol', 'C R S V')
GameState = Enum('GameState', 'GAME SNAP FINAL')

pygame.init()
pygame.mixer.init()

bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("SlapJack")

card_back = pygame.image.load("resources/CARDS/CARDBACK.png")
card_back = pygame.transform.scale(card_back, (223, 312))
background = pygame.image.load("resources/BG.png")
background = pygame.transform.scale(background, bounds)

def load_card_image(symbol, value):
    number = f"{value:02}"
    image = pygame.image.load(f"resources/CARDS/{number}{symbol.name}.png")
    return pygame.transform.scale(image, (223, 312))

def create_deck():
    return [(symbol, value, load_card_image(symbol, value)) 
            for symbol in Symbol for value in range(1, 15) if value != 11]

def shuffle_deck(deck):
    random.shuffle(deck)

def draw_card(deck):
    return deck.pop()

def deck_length(deck):
    return len(deck)

def create_pile():
    return []

def add_to_pile(pile, card):
    pile.append(card)

def top_of_pile(pile):
    return pile[-1] if pile else None

def clear_pile(pile):
    pile.clear()

def is_snap(pile):
    return len(pile) > 1 and pile[-1][1] == pile[-2][1]

def create_player(name, flip_key, snap_key):
    return {'hand': [], 'name': name, 'flip_key': flip_key, 'snap_key': snap_key}

def draw_for_player(player, deck):
    player['hand'].append(draw_card(deck))

def play_card_from_player(player):
    return player['hand'].pop(0)

def deal_cards(deck, player1, player2):
    half_deck = deck_length(deck) // 2
    for _ in range(half_deck):
        draw_for_player(player1, deck)
        draw_for_player(player2, deck)

def switch_player(current_player, player1, player2):
    return player2 if current_player == player1 else player1

def win_round(player, pile):
    player['hand'].extend(pile)
    clear_pile(pile)

def initialize_game_state():
    deck = create_deck()
    shuffle_deck(deck)
    player1 = create_player("Player 1", pygame.K_a, pygame.K_d)
    player2 = create_player("Player 2", pygame.K_LEFT, pygame.K_RIGHT)
    pile = create_pile()
    deal_cards(deck, player1, player2)
    return {
        'deck': deck,
        'player1': player1,
        'player2': player2,
        'pile': pile,
        'current_player': player1,
        'state': GameState.GAME,
        'score_player1': 0,
        'score_player2': 0,
        'result': {}
    }

def play_game(state, key):
    if key is None or state['state'] == GameState.FINAL:
        return

    current_player = state['current_player']
    if key == current_player['flip_key']:
        add_to_pile(state['pile'], play_card_from_player(current_player))
        state['current_player'] = switch_player(current_player, state['player1'], state['player2'])

    snap_caller = None
    non_snap_caller = None
    is_snap_game = is_snap(state['pile'])

    if key == state['player1']['snap_key']:
        snap_caller = state['player1']
        non_snap_caller = state['player2']
    elif key == state['player2']['snap_key']:
        snap_caller = state['player2']
        non_snap_caller = state['player1']

    if is_snap_game and snap_caller:
        state['result'] = {
            "winner": snap_caller,
            "is_snap": True,
            "snap_caller": snap_caller
        }
        win_round(snap_caller, state['pile'])
        state['state'] = GameState.SNAP
    elif not is_snap_game and snap_caller:
        state['result'] = {
            "winner": non_snap_caller,
            "is_snap": False,
            "snap_caller": snap_caller
        }
        win_round(non_snap_caller, state['pile'])
        state['state'] = GameState.SNAP

    if len(state['player1']['hand']) == 0:
        state['result'] = {"winner": state['player2']}
        state['state'] = GameState.FINAL
    elif len(state['player2']['hand']) == 0:
        state['result'] = {"winner": state['player1']}
        state['state'] = GameState.FINAL

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] or keys[pygame.K_m]:
        if state['result']["winner"]['name'] == "Player 1":
            state['score_player1'] += 1
        else:
            state['score_player2'] += 1
        state.update(initialize_game_state())
        if keys[pygame.K_m]:
            state['score_player1'] = 0
            state['score_player2'] = 0
            menu.menu()
        else:
            start_game(window, state)

def show_shuffle_screen():
    window.fill((0, 0, 0))
    font = pygame.font.Font("resources/Arial.ttf", 30)
    text = font.render("Shuffling the cards...", True, (255, 255, 255))
    window.blit(text, (325, 320))
    pygame.display.update()

def render_game(window, state):
    window.fill((15, 0, 169))
    window.blit(background, (0, 0))
    font = pygame.font.Font("resources/Arial.ttf", 30)

    window.blit(card_back, (100, 200))
    window.blit(card_back, (700, 200))

    text = font.render(f"{len(state['player1']['hand'])} cards", True, (255, 255, 255))
    window.blit(text, (110, 520))

    text = font.render(f"{len(state['player2']['hand'])} cards", True, (255, 255, 255))
    window.blit(text, (710, 520))

    text = font.render(f"{state['score_player1']} | {state['score_player2']}", True, (255, 255, 255))
    window.blit(text, (470, 700))

    top_card = top_of_pile(state['pile'])
    if top_card:
        window.blit(top_card[2], (400, 200))

    if state['state'] == GameState.GAME:
        text = font.render(f"It's {state['current_player']['name']}'s turn", True, (255, 255, 255))
        window.blit(text, (20, 50))

    if state['state'] == GameState.SNAP:
        result = state['result']
        if result["is_snap"]:
            message1 = f"Correct Snap! Called by {result['snap_caller']['name']}"
        else:
            message1 = f"Incorrect Snap! Called by {result['snap_caller']['name']}."
        window.fill((0, 0, 0))
        text = font.render(message1, True, (255, 255, 255))
        window.blit(text, (270, 250))

        if not result["is_snap"]:
            message2 = f"{result['winner']['name']} gets the cards!"
            text2 = font.render(message2, True, (255, 255, 255))
            window.blit(text2, (300, 300))

    if state['state'] == GameState.FINAL:
        result = state['result']
        window.fill((0, 0, 0))
        message = f"Game Over! {result['winner']['name']} wins!"
        restart_game = "Press R to start a new game!"
        back_to_menu = "Press M to go back to the menu!"
        text_back_to_menu = font.render(back_to_menu, True, (255, 255, 255))
        text_restart = font.render(restart_game, True, (255, 255, 255))
        text = font.render(message, True, (255, 255, 255))
        window.blit(text, (190, 250))
        window.blit(text_restart, (225, 300))
        window.blit(text_back_to_menu, (210, 350))
        key = pygame.key.get_pressed()
        if key[pygame.K_r] or key[pygame.K_m]:
            if result['winner']['name'] == "Player 1":
                state['score_player1'] += 1
            else:
                state['score_player2'] += 1
            state.update(initialize_game_state())
            if key[pygame.K_m]:
                state['score_player1'] = 0
                state['score_player2'] = 0
                menu.menu()
            else:
                start_game(window, state)

def start_game(window, state):
    pygame.display.set_caption("SlapJack")
    show_shuffle_screen()
    pygame.time.delay(1000)
    run = True
    while run:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                key = event.key

        play_game(state, key)
        render_game(window, state)
        pygame.display.update()

        if state['state'] == GameState.SNAP:
            pygame.time.delay(3000)
            state['state'] = GameState.GAME

    pygame.quit()
    quit()

def slapjack():
    game_state = initialize_game_state()
    start_game(window, game_state)
