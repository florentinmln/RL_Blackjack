class Player():

    def __init__(self, role):
        self.score = 0
        self.win = 0
        self.lose = 0
        self.draw
        self.hand =[]
        self.role = role

    def reset(self):
        self.score = 0
        self.hand =[]