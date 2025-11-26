import pygame
import sys
import random
import time

# --- INIT PYGAME ---
pygame.init()
window = pygame.display.set_mode((1240, 720))
pygame.display.set_caption("Simulation Blackjack Visuelle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# --- TAILLE DES CARTES ---
card_size = (150, 200)

# --- CHARGER LES CARTES ---
ranks = ["AS","2","3","4","5","6","7","8","9","10","J","Q","K"]
suits = ["C","D","H","S"]
cardsImages = {}
for rank in ranks:
    for suit in suits:
        path = f"./image_card/{rank}_{suit}.png"
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, card_size)
        cardsImages[(rank, suit)] = img

# --- FONCTIONS UTILES ---
def draw_card():
    return random.choice(ranks), random.choice(suits)

def get_card_value(card):
    rank, suit = card
    if rank in ["J","Q","K"]:
        return 10
    elif rank == "AS":
        return 11  # simplification pour la simulation
    else:
        return int(rank)

def calculate_score(hand):
    score = sum(get_card_value(card) for card in hand)
    # ajustement As si > 21
    aces = sum(1 for card in hand if card[0] == "A")
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

# --- INITIALISATION DES MAINS ---
player_hand = [draw_card(), draw_card()]
dealer_hand = [draw_card()]
done = False
player_done = False
dealer_done = False

# --- POSITIONS ---
start_x_player = 50
start_y_player = 350
start_x_dealer = 50
start_y_dealer = 50
card_spacing = 200

# --- SIMULATION ---
player_next_draw_time = time.time() + 1
dealer_next_draw_time = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()

    # --- TOUR DU JOUEUR ---
    if not player_done and current_time >= player_next_draw_time:
        score = calculate_score(player_hand)
        if score < 17:  # tirage automatique si score < 17
            player_hand.append(draw_card())
            player_next_draw_time = current_time + 1  # prochaine carte dans 1s
        else:
            player_done = True
            dealer_next_draw_time = current_time + 1  # dealer commence dans 1s

    # --- TOUR DU DEALER ---
    if player_done and not dealer_done and current_time >= dealer_next_draw_time:
        dealer_score = calculate_score(dealer_hand)
        if dealer_score < 17:
            dealer_hand.append(draw_card())
            dealer_next_draw_time = current_time + 1
        else:
            dealer_done = True
            done = True

    # --- AFFICHAGE ---
    window.fill((0, 100, 0))

    # Dealer
    for i, card in enumerate(dealer_hand):
        window.blit(cardsImages[card], (start_x_dealer + i*card_spacing, start_y_dealer))
    dealer_score = calculate_score(dealer_hand)
    dealer_text = font.render(f"Dealer Score: {dealer_score}", True, (255,255,255))
    window.blit(dealer_text, (50, start_y_dealer - 50))

    # Player
    for i, card in enumerate(player_hand):
        window.blit(cardsImages[card], (start_x_player + i*card_spacing, start_y_player))
    player_score = calculate_score(player_hand)
    player_text = font.render(f"Player Score: {player_score}", True, (255,255,255))
    window.blit(player_text, (50, start_y_player + 200))

    # Status
    status = "ROUND FINISHED" if done else "CONTINUE"
    status_render = font.render(status, True, (255, 255, 0))
    window.blit(status_render, (50, 300))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
