import numpy as np

# Il faut l'installer sur nos machines.
import gymnasium as gym


# https://gymnasium.farama.org/introduction/create_custom_env/
# C'est la doc de gym si il faut. 

class BlackJackEnv(gym.Env):

    def __init__(self, deck_size: int = 32):
        # To Do
        # Init de l'environnement, création des main pour les joueurs.
        # On passe en param la taille du deck, je ne sais pas si c'est pertinent mais bon je trouve ca cool.

    def reset(self, seed: int):
        # To DO
        # A chaque fin de partie recréer une partie avec la seed pour gerer l'aleatoire.

        # Important: permet de set la seed pour tout le random.
        super().reset(seed=seed)

        self.deck.reset()

        self.player.score = 0
        self.player.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        self.player.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        self.player.score_calcul()

        self.dealer.score = 0
        self.dealer.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        self.dealer.hand.append(self.deck.take_card(self.np_random.integers(0, self.deck.lenght())))
        self.dealer.score_calcul()

        obs = self._get_obs()
        info = self._get_info()

        return obs, info
        
    def step(self, action):
        # To Do
        # Une boucle de jeu, c'est a dire une action qui donne une reward et un nouveau state.

    def render(self):
        # To Do 
        # Pour faire l'affichage graphique si je ne me trompe pas.

    def _get_obs(self):
        # To Do
        # Un peu comme un toString, on définit comment on veut ecrire dans le terminal notre environnement.

    def _get_info(self):
        # To Do
        # Permet de faire du debug, ici aussi on définit comment on affiche cette valeur. 
        # Regarder la doc pour un exemple