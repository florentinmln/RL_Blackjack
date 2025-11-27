import random

class Deck():

    def __init__(self, nb_card_game):
        self.deck = []
        self.card = ["AS", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for _ in range(nb_card_game):
            for i in range(len(self.card)):
                self.deck.append((self.card[i] , "H"))
                self.deck.append((self.card[i] , "C"))
                self.deck.append((self.card[i] , "S"))
                self.deck.append((self.card[i] , "D"))

    def draw_card(self):
        random_index = random.randint(0, len(self.deck))
        card = self.deck[random_index]
        self.deck.remove(random_index)
        return card
    
    def reset(self, nb_card_game):
        self.deck = []
        for _ in range(nb_card_game):
            for i in range(len(self.card)):
                self.deck.append((self.card[i] , "H"))
                self.deck.append((self.card[i] , "C"))
                self.deck.append((self.card[i] , "S"))
                self.deck.append((self.card[i] , "D"))