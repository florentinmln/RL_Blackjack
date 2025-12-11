import gymnasium as gym
from Blackjack import BlackJackEnv

blackjack = BlackJackEnv()

for i in range(5):
    while(not blackjack.done) :
        print("Choose your action. (Stand : s, Pick : p)")
        action = input()
        if action == "s" :
            blackjack.step("STAND")
        elif action == "p" :
            blackjack.step("PICK")
        else :
            print("tu n'a pas fait le bon choix")
    
    if i < 5 - 1 :
        blackjack.reset()
        blackjack.render()