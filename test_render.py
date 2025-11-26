import pygame
import sys


# Image de : https://fr.freepik.com/auteur/macrovector.
# Lien des images : https://fr.freepik.com/vecteurs-libre/poker-cartes-icones-collection_1045019.htm#fromView=search&page=1&position=28&uuid=8c1bb531-6063-4e6d-8b00-0f058a80e24f&query=jeu+de+carte+pixel

cardsImages = {
    ("AS", "C"): pygame.image.load("./image_card/AS_C.png"),
    ("AS", "H"): pygame.image.load("./image_card/AS_H.png"),
    ("AS", "S"): pygame.image.load("./image_card/AS_S.png"),
    ("AS", "D"): pygame.image.load("./image_card/AS_D.png"),

    ("2", "C"): pygame.image.load("./image_card/2_C.png"),
    ("2", "H"): pygame.image.load("./image_card/2_H.png"),
    ("2", "S"): pygame.image.load("./image_card/2_S.png"),
    ("2", "D"): pygame.image.load("./image_card/2_D.png"),

    ("3", "C"): pygame.image.load("./image_card/3_C.png"),
    ("3", "H"): pygame.image.load("./image_card/3_H.png"),
    ("3", "S"): pygame.image.load("./image_card/3_S.png"),
    ("3", "D"): pygame.image.load("./image_card/3_D.png"),

    ("4", "C"): pygame.image.load("./image_card/4_C.png"),
    ("4", "H"): pygame.image.load("./image_card/4_H.png"),
    ("4", "S"): pygame.image.load("./image_card/4_S.png"),
    ("4", "D"): pygame.image.load("./image_card/4_D.png"),

    ("5", "C"): pygame.image.load("./image_card/5_C.png"),
    ("5", "H"): pygame.image.load("./image_card/5_H.png"),
    ("5", "S"): pygame.image.load("./image_card/5_S.png"),
    ("5", "D"): pygame.image.load("./image_card/5_D.png"),

    ("6", "C"): pygame.image.load("./image_card/6_C.png"),
    ("6", "H"): pygame.image.load("./image_card/6_H.png"),
    ("6", "S"): pygame.image.load("./image_card/6_S.png"),
    ("6", "D"): pygame.image.load("./image_card/6_D.png"),

    ("7", "C"): pygame.image.load("./image_card/7_C.png"),
    ("7", "H"): pygame.image.load("./image_card/7_H.png"),
    ("7", "S"): pygame.image.load("./image_card/7_S.png"),
    ("7", "D"): pygame.image.load("./image_card/7_D.png"),

    ("8", "C"): pygame.image.load("./image_card/8_C.png"),
    ("8", "H"): pygame.image.load("./image_card/8_H.png"),
    ("8", "S"): pygame.image.load("./image_card/8_S.png"),
    ("8", "D"): pygame.image.load("./image_card/8_D.png"),

    ("9", "C"): pygame.image.load("./image_card/9_C.png"),
    ("9", "H"): pygame.image.load("./image_card/9_H.png"),
    ("9", "S"): pygame.image.load("./image_card/9_S.png"),
    ("9", "D"): pygame.image.load("./image_card/9_D.png"),

    ("10", "C"): pygame.image.load("./image_card/10_C.png"),
    ("10", "H"): pygame.image.load("./image_card/10_H.png"),
    ("10", "S"): pygame.image.load("./image_card/10_S.png"),
    ("10", "D"): pygame.image.load("./image_card/10_D.png"),

    ("J", "C"): pygame.image.load("./image_card/J_C.png"),
    ("J", "H"): pygame.image.load("./image_card/J_H.png"),
    ("J", "S"): pygame.image.load("./image_card/J_S.png"),
    ("J", "D"): pygame.image.load("./image_card/J_D.png"),

    ("Q", "C"): pygame.image.load("./image_card/Q_C.png"),
    ("Q", "H"): pygame.image.load("./image_card/Q_H.png"),
    ("Q", "S"): pygame.image.load("./image_card/Q_S.png"),
    ("Q", "D"): pygame.image.load("./image_card/Q_D.png"),

    ("K", "C"): pygame.image.load("./image_card/K_C.png"),
    ("K", "H"): pygame.image.load("./image_card/K_H.png"),
    ("K", "S"): pygame.image.load("./image_card/K_S.png"),
    ("K", "D"): pygame.image.load("./image_card/K_D.png")
}

def main():
    pygame.init()

    # Taille de la fenêtre
    window = pygame.display.set_mode((1240, 720))
    pygame.display.set_caption("Test Render Blackjack")

    # Horloge pour limiter FPS
    clock = pygame.time.Clock()

    # Police d'écriture
    font = pygame.font.SysFont("Arial", 50)

    # Exemple de données (comme si c'était ton env)
    dealer_hand = [("K", "C"), ("AS", "H"), ("2", "C"), ("4", "S")]
    player_hand = [("2", "S"), ("10", "D")]
    dealer_score = 18
    player_score = 20
    done = False

    # Variables pour positionner les cartes
    start_x_player = 50
    start_y_player = 350
    start_x_dealer = 50
    start_y_dealer = 50 
    card_spacing = 200 
    desired_size = (150, 200)
    for rank in ["AS","2","3","4","5","6","7","8","9","10","J","Q","K"]:
        for suit in ["C","D","H","S"]:
            path = f"./image_card/{rank}_{suit}.png"
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, desired_size)
            cardsImages[(rank, suit)] = img
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fond vert (table de blackjack)
        window.fill((0, 100, 0))
        # # Texte Dealer
        dealer_text = f"{dealer_score}"
        render_dealer = font.render(dealer_text, True, (255, 255, 255))
        window.blit(render_dealer, (900, 100))

        # # Texte Player
        player_text = f"{player_score}"
        render_player = font.render(player_text, True, (255, 255, 255))
        window.blit(render_player, (900, 400))
        for i, card in enumerate(dealer_hand):
            window.blit(cardsImages[card], (start_x_dealer + i*card_spacing, start_y_dealer))

        # Affichage player
        for i, card in enumerate(player_hand):
            window.blit(cardsImages[card], (start_x_player + i*card_spacing, start_y_player))

        # Mettre à jour l'écran
        pygame.display.flip()

        # Limiter FPS
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()