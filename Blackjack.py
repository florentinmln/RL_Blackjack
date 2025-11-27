from typing import Optional
import numpy as np
from Deck import Deck
from Player import Player
import gymnasium as gym


class GridWorldEnv(gym.Env):

    def __init__(self, number_card: int = 5):
        # The number of cards in deck
        self.deck = Deck(number_card)

        # Initialize score - will be set randomly in reset()
        # Using -1,-1 as "uninitialized" state
        self.player = Player(role="player")
        self.dealer = Player(role="dealer")

        # Define what the agent can observe
        # Dict space gives us structured, human-readable observations
        self.observation_space = gym.spaces.Dict(
            {
                "agent": gym.spaces.Box(0, shape=1, dtype=int),   # [x, y] coordinates
                "target": gym.spaces.Box(0, shape=1, dtype=int),  # [x, y] coordinates
            }
        )

        # Define what actions are available (2 tirer les cartes ou se coucher)
        self.action_space = gym.spaces.Discrete(2)

        # Map action numbers to actual movements on the grid
        # This makes the code more readable than using raw numbers
        self._action_to_direction = {
            0: np.array([1, 0]),   # Move right (positive x)
            1: np.array([0, 1]),   # Move up (positive y)
        }

    def start_hand(self):
        hand = []
        for _ in range(2):
            hand.append(self.deck.draw_card())
        return hand