import numpy as np
import pygame
import sys
import time
# Il faut l'installer sur nos machines.
import gymnasium as gym


# https://gymnasium.farama.org/introduction/create_custom_env/
# C'est la doc de gym si il faut. 

# Image de : https://fr.freepik.com/auteur/macrovector.
# Lien des images : https://fr.freepik.com/vecteurs-libre/poker-cartes-icones-collection_1045019.htm#fromView=search&page=1&position=28&uuid=8c1bb531-6063-4e6d-8b00-0f058a80e24f&query=jeu+de+carte+pixel

class BlackJackEnv(gym.Env):

    def __init__(self):
        # To Do
        # Init de l'environnement, création des main pour les joueurs.
        # On passe en param la taille du deck, je ne sais pas si c'est pertinent mais bon je trouve ca cool.
        pass

    def reset(self, seed: int):
        # To DO
        # A chaque fin de partie recréer une partie avec la seed pour gerer l'aleatoire.

        # Important: permet de set la seed pour tout le random.
        super().reset(seed=seed)
        
        # On reset la variable qui finit un épisode.
        self.done = False

        # On utilise la fonction reset de l'objet deck pour recommencer un épisode.
        self.deck.reset()

        # On réinitialise le score du joueur mais pas le compteur de victoire et de défaite.
        self.player.score = 0

        # On tire deux cartes pour reset la main du joueur
        self.player.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        self.player.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        
        # On calcule le score du joueur.
        self.player.score_calcul()

        # On réinitialise le score du dealer 
        self.dealer.score = 0

        # On tire deux cartes pour la main initial du dealer 
        self.dealer.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        self.dealer.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))

        # On calcule le score du dealer
        self.dealer.score_calcul()

        # On récupère ine observation de l'épisode en cours
        obs = self._get_obs()
        
        # Si on a besoin de faire un affichage on appelle la fonction render.
        if self.render_mode == "human":
            self.render()

        # On retourne l'observation, si on veut on peut ajouter une fonction info et donc retourner cette valeur aussi. 
        return obs
        
    def step(self, action):
        # To Do
        # Une boucle de jeu, c'est a dire une action qui donne une reward et un nouveau state.
        pass

    def render(self):
        # Affichage simple pour debug.
        if(self.render_mode == "debug"):
            print("--------------------------------------")
            print(f"Dealer: {self.dealer.hand} -> {self.dealer.score}")
            print(f"Player: {self.player.hand} -> {self.player.score}")

            if(self.done):
                print("ROUND FINISHED")
            else:
                print("CONTINUE")
            print("--------------------------------------")
        elif(self.render_mode == "human"):
            # Pas complet pour faire jouer l'agent dessus. A améliorer.
            # Pour ne pas redéfinir la fenetre pour chaque tour.
            if self.window is None:
                # Création de la fenetre.
                pygame.init()
                self.window = pygame.display.set_mode((1240, 720))
                pygame.display.set_caption("Blackjack")
                
                # Création de l'horloge pour gérer le temps et les FPS 
                self.clock = pygame.time.Clock()

                # Définision du texte et de sa taille
                self.font = pygame.font.SysFont("Arial", 30)
                
                # Dict qui contient les images 
                self.cardsImages = {}
                
                # Taille des images que je veux afficher
                card_size = (150, 200)
                ranks = ["AS","2","3","4","5","6","7","8","9","10","J","Q","K"]
                suits = ["C","D","H","S"]
                for rank in ranks:
                    for suit in suits:
                        path = f"./image_card/{rank}_{suit}.png"

                        # On charge l'image
                        img = pygame.image.load(path)

                        # On resize l'image
                        img = pygame.transform.scale(img, card_size)

                        self.cardsImages[(rank, suit)] = img

                # Position de la main du player
                self.start_x_player = 50
                self.start_y_player = 350

                # Position de la main du dealer
                self.start_x_dealer = 50
                self.start_y_dealer = 50

                # Espacement entre les cartes
                self.card_spacing = 200

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Couleur du fond set a vert.
            self.window.fill((0, 100, 0))

            # Affichage main du dealer
            for i, card in enumerate(self.dealer.hand):
                self.window.blit(self.cardsImages[card],
                                (self.start_x_dealer + i*self.card_spacing, self.start_y_dealer))

            # Affichage du score du dealer au dessus de sa main
            dealer_text = self.font.render(f"Dealer Score: {self.dealer.score}", True, (255,255,255))
            self.window.blit(dealer_text, (50, self.start_y_dealer - 50))

            # Affichage de la main du player
            for i, card in enumerate(self.player.hand):
                self.window.blit(self.cardsImages[card],
                                (self.start_x_player + i*self.card_spacing, self.start_y_player))

            # Affichage du score du player en dessous de sa main
            player_text = self.font.render(f"Player Score: {self.player.score}", True, (255,255,255))
            self.window.blit(player_text, (50, self.start_y_player + 200))

            # Status de la partie, je pense le changer 
            if self.done :
                status = "ROUND FINISHED"
            else :
                status = "CONTINUE"

            status_render = self.font.render(status, True, (255, 255, 0))
            self.window.blit(status_render, (50, 300))

            # Mise a jour de l'écran
            pygame.display.flip()
            self.clock.tick(30)
    
    def close(self):
        if(self.window is not None):
            pygame.display.quit()
            pygame.quit()

    def _get_obs(self):
        # To Do
        # Un peu comme un toString, on définit comment on veut ecrire dans le terminal notre environnement.
        
        # Retourne la main et le score du player et du dealer
        return {"player" : (self.player.hand, self.player.score),
                "dealer" : (self.dealer.hand, self.dealer.score)}