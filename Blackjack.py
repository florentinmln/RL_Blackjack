from typing import Optional
import numpy as np
from Deck import Deck
from Player import Player
import gymnasium as gym


class GridWorldEnv(gym.Env):

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
                "agent": gym.spaces.Box(0, dtype=int),   # [x, y] coordinates
                "target": gym.spaces.Box(0, dtype=int),  # [x, y] coordinates
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
        for i in range(len(self.player.hand)):
            key = self.player.hand[i][0]
            if key == "AS":
                print("tu veut que ton As soit egale a 11? (yes :y, no : n)")
                x = input()
                if x == "n":
                    self.player.score += 1
                else :
                    self.player.score += 11
            else :
                self.player.score += self.card_value[key]

    def score_dealer(self):
        for i in range(len(self.dealer.hand)):
            key = self.dealer.hand[i][0]
            if key == "AS":
                if self.dealer.score < 11:
                    self.dealer.score += 11
                else:
                    self.dealer.score += 1
            else:
                self.player.score += self.card_value[key]