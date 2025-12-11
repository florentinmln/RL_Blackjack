import numpy as np
import pygame
import sys

from typing import Optional
from Deck import Deck
from Player import Player
import gymnasium as gym

class BlackJackEnv(gym.Env):

    def __init__(self, render_mode="debug", number_card: int = 5):
        # The number of cards in deck
        self.deck = Deck(number_card)

        self.card_value = {"AS" : 1,
                      "2": 2,
                      "3": 3,
                      "4": 4,
                      "5": 5,
                      "6": 6,
                      "7": 7,
                      "8": 8,
                      "9": 9,
                      "10": 10,
                      "J": 10,
                      "Q": 10,
                      "K": 10
                      }

        # Initialize score - will be set randomly in reset()
        # Using -1,-1 as "uninitialized" state
        self.player = Player(role="player")
        self.dealer = Player(role="dealer")

        self.player.hand = self.start_hand()
        self.dealer.hand = self.start_hand()

        self.score_dealer()
        self.score_player()

        # Define what the agent can observe
        # Dict space gives us structured, human-readable observations
        self.observation_space = gym.spaces.Dict(
            {
                "agent": gym.spaces.Box(0, 30, dtype=int),   # [x, y] coordinates
                "target": gym.spaces.Box(0, 30, dtype=int),  # [x, y] coordinates
            }
        )

        # Define what actions are available (2 tirer les cartes ou se coucher)
        self.action_space = gym.spaces.Discrete(2)

        # Map action numbers to actual movements on the grid
        # This makes the code more readable than using raw numbers
        self._action_to_direction = ["STAND", "PICK"]

        self.render_mode = render_mode
        
        self.window = None
        self.clock = None
        self.done = False
        self.render()

    def step(self, action):
        if self.player.score == 21 :
            self.dealer.lose += 1
            self.player.win += 1
            self.done = True

        elif self.dealer.score == 21:
            self.dealer.win += 1
            self.player.lose += 1
            self.done = True

        else:
            if action == "STAND":
                while self.dealer.score < 17:
                    self.dealer.hand.append(self.deck.draw_card())
                    self.score_dealer()

                if self.player.score <= self.dealer.score:
                    self.dealer.win += 1
                    self.player.lose += 1
                    self.done = True

                else :
                    self.dealer.lose += 1
                    self.player.win += 1
                    self.done = True

            elif action == "PICK":
                self.player.hand.append(self.deck.draw_card())
                self.score_player()

                if self.player.score > 21:
                    self.dealer.win += 1
                    self.player.lose += 1
                    self.done = True
                    
            else :
                print("voue voue")
        
        self.render()
        
    def start_hand(self):
        hand = []
        for _ in range(2):
            hand.append(self.deck.draw_card())
        return hand
    
    def score_player(self):
        score = 0
        if self.player.score == 0 :
            for i in range(len(self.player.hand)):
                key = self.player.hand[i][0]
                if key == "AS" and i == 0:
                    score += 11
                else :
                    score += self.card_value[key]
            self.player.score = score
        else :
            key = self.player.hand[-1][0]
            if key == "AS":
                print("Tu veut que ton As soit égale à 11? (yes :y, no : n)")
                x = input()
                if x == "n":
                    self.player.score += 1
                else :
                    self.player.score += 11
            else :
                self.player.score += self.card_value[key]

    def score_dealer(self):
        score = 0
        if self.dealer.score == 0 :
            for i in range(len(self.dealer.hand)):
                key = self.dealer.hand[i][0]
                if key == "AS":
                    if score < 11:
                        score += 11
                    else:
                        score += 1
                else:
                    score += self.card_value[key]
            self.dealer.score = score
        else :
            key = self.dealer.hand[-1][0]
            if key == "AS":
                if self.dealer.score < 11:
                    self.dealer.score += 11
                else:
                    self.dealer.score += 1
            else:
                self.dealer.score += self.card_value[key]

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
        self.player.hand.append(self.deck.draw_card())
        self.player.hand.append(self.deck.draw_card())
        
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
        return {"player" : (self.player.score),
                "dealer" : (self.dealer.score)}