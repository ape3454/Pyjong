from copy import deepcopy
import math
import random
import time
import msvcrt

"""
Abbreviations:
    S = Stick (索)
    D = Dot (筒)
    K (or 10K) = 10 Thousand (萬)
    HZ = Red Middle (红中)
    BB = White Board (白板)
    FC = Jackpot(?) (发财)
    E = East (東)
    S = South (南)
    W = West (西)
    N = North (北)
"""

tileSuitedTemplate = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
tileDragonTemplate = ["HZ", "BB", "FC"]
tileWindTemplate = ['E', 'S', 'W', 'N']
tileBonusTemplate = ["Plum", "Orchid", "Chrysanthemum", "Bamboo", "Spring", "Summer", "Autumn", "Winter"]
discardPile = []
p1Wall = []
p2Wall = []
p3Wall = []
p4Wall = []
walls = [p1Wall, p2Wall, p3Wall, p4Wall]
p1Hand = []
p2Hand = []
p3Hand = []
p4Hand = []
global hands
hands = [p1Hand, p2Hand, p3Hand, p4Hand]

def initialisation():
    def removeFromWall(number, hand):
        global hands

        for i in range(number):
            hands[hand] += [dealOrder.pop(0)]
            
    def explanation():
        print("Welcome to Mahjong")
        time.sleep(0.7)
        print("Graciously hosted by LeadPipe Corp., enjoy this rendition of the classic Chinese game of Mahjong!")
        time.sleep(2)
        print()
        match input("Read Instructions? (Y/N)").upper():
            case 'Y':
                print()
                print("You are one of four players, playing to win with valid hands.")
                time.sleep(1.5)
                print("You start the game with 14 tiles, each part of different sets and suits.")
                time.sleep(1.5)
                print("There are 3 suits:")
                time.sleep(0.5)
                print("The Sticks, represented by 'S'.")
                time.sleep(1)
                print("The Dots, represented by 'D'.")
                time.sleep(1)
                print("The Ten Thousands, represented by 'K'.")
                time.sleep(1.5)
                print("There are also 3 other sets:")
                time.sleep(1)
                print("The Directional Winds, represented by the cardinal directions (E, S, W, N).")
                time.sleep(1)
                print("The Dragons: Red Middle (HZ), Blank Board (BB), and Jackpot (FC).")
                time.sleep(1)
                print("And the Bonus tiles: tiles with names of flowers and the four seasons.")
                time.sleep(2)
                print()
                print("The order of play is determined by whoever rolls the highest number using one dice. That player becomes the 'Dealer'.")
                time.sleep(2)
                print("The Dealer rolls three dice to determine how the tiles are drawn.")
                time.sleep(1.5)
                print("Each player draws 13 tiles, with the exception that the Dealer draws 14.")
                time.sleep(1.5)
                print("The gameplay starts when the Dealer discards his first tile.")
                time.sleep(1.5)
                print("On each player's turn, they must first either draw a tile or call a special move, and then discard a tile.")
                time.sleep(2)
                print("A special move is determined by the previously discarded tile and the tiles in your hand.")
                time.sleep(2)
                print("They are only callable when their conditions are met.")
                time.sleep(1.5)
                print("A 'Straight' is when the discarded tile and two other tiles in your hand creates a set of three consecutive numbers.")
                time.sleep(2)
                print("A 'Match' is when the discarded tile and TWO other tiles in your hand creates a set of THREE identical tiles.")
                time.sleep(2)
                print("A '4-Match' is when the discard tile and THREE other tiles in your hand creates a set of FOUR identical tiles.")
                time.sleep(2)
                print("And an 'Eye' is when the discarded tile and another tile in your hand creates a pair of identical tiles. This is only callable when you would win from the tile.")
                time.sleep(2)
                print()
                print("A player wins when their hand is valid. These are the valid hands:")
                time.sleep(1.5)
                print("A 'Pure' hand is when every tile in your hand belongs to a single suit (i.e. All sticks).")
                time.sleep(1.5)
                print("A 'Semi-Pure' hand is when four sets of tiles in your hand belongs to a single suit, and an unmatching eye.")
                time.sleep(1.5)
                print("A 'Matched' hand is when every tile in your hand belongs to a set of Matches or 4-Matches, and an eye.")
                time.sleep(1.5)
                print("A 'Straight' hand is when every tile in your hand belongs to a set of Straights, and an eye.")
                time.sleep(1.5)
                print()
                print("There also exists several unique ways of winning, for you to unlock.")
                time.sleep(0.5)
                print()
                print()
            case 'N':
                print("Suits you.")
            case _:
                print("??? ...")

    def wall():
        tiles = []
        suits = ['S', 'D', 'K']

        for i in range(3):
            for tile in tileSuitedTemplate:
                for j in range(4):
                    tiles.append(suits[i] + tile)

        for tile in tileDragonTemplate:
            for i in range(4):
                tiles.append(tile)
        
        for tile in tileWindTemplate:
            for i in range(4):
                tiles.append(tile)
        
        tiles += tileBonusTemplate

        random.shuffle(tiles)
        for i in range(4):
            walls[i] = tiles[:36]
            tiles = tiles[36:]

    def dealing():
        global hands
        global walls
        global diceTotal
        global dealOrder

        print("------[ Dealing Phase ]------")
        time.sleep(0.2)
        print("Roll (press any key):")
        while not msvcrt.kbhit():
            pass

        diceTotal = [0, []]
        for i in range(4): # first roll is player's
            time.sleep(3)
            roll = random.randint(1, 6)
            if roll > diceTotal[0]:
                diceTotal = [roll, [i]]
            elif roll == diceTotal[0]:
                diceTotal[1].append(i)
            if i == 0:
                print("You rolled a", roll)
            else:
                print("Player", (i + 1), "rolled a", roll)

        while len(diceTotal[1]) >= 2:
            msvcrt.getch()
            time.sleep(0.2)
            print("There was a tie!")
            time.sleep(0.2)
            diceTotal[0] = []
            for player in diceTotal[1][:]:
                diceTotal[0].append(random.randint(1, 6))
                if player == 0:
                    print("Roll:")
                    while not msvcrt.kbhit():
                        pass
                    time.sleep(3)
                    print("You rolled a", diceTotal[0][-1])
                else:
                    time.sleep(3)
                    print("Player %s rolled a %s" % (diceTotal[1][1], diceTotal[0][-1]))
                if len(set(diceTotal[0])) >= 2:
                    diceTotal[1].remove(player)
                    diceTotal[0].remove(min(diceTotal[0]))
                print(diceTotal)

        hands = hands[diceTotal[1][0]:] + hands[:diceTotal[1][0]]
        time.sleep(0.3)
        print("Player %s is East. Player %s is South. Player %s is West. Player %s is North." % (diceTotal[1][0] % 4 + 1, (diceTotal[1][0] + 1) % 4 + 1, (diceTotal[1][0] + 2) % 4 + 1, (diceTotal[1][0] + 3) % 4 + 1))
        time.sleep(1)

        diceTotal = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)

        dealOrder = walls[diceTotal % 4] + walls[(diceTotal + 1) % 4] + walls[(diceTotal + 2) % 4] + walls[(diceTotal + 3) % 4]
        dealOrder = dealOrder[(diceTotal - 1) * 2 + 1:] + dealOrder[:(diceTotal - 1) * 2 + 1]

        for i in range(random.choices([1, 2, 3, 4, 7], weights=[2, 10, 10, 3, 1])[0]):
            time.sleep(2)
            print("Shuffling", end='', flush=True)
            time.sleep(0.9)
            for i in range(3):
                print(".", end='', flush=True)
                time.sleep(0.9)
            print()
        time.sleep(2)
        
        # diceTotal represents wall shift of dealOrder
        dels = len(walls[diceTotal % 4][diceTotal:])
        walls[diceTotal % 4][diceTotal:] = []
        if 53 - dels <= 36:
            walls[(diceTotal + 1) % 4][:53 - dels] = []
        else:
            walls[(diceTotal + 1) % 4] = []
            walls[(diceTotal + 2) % 4][:17 - dels] = []

        for i in range(3):
            time.sleep(2)
            print("Dealing", end='', flush=True)
            time.sleep(0.9)
            for i in range(3):
                print(".", end='', flush=True)
                time.sleep(0.9)
            print()
        time.sleep(2)

        for i in range(3):
            for j in range(4):
                removeFromWall(4, j)
        for i in range(4):
            removeFromWall(1, i)
        removeFromWall(1, 0)

        

    # functions are done

    #explanation()
    wall()
    dealing()

def play():
    pass



initialisation()
print(diceTotal)
for i in hands:
    print(i)
    print(len(i))
print(p1Hand) # user always player 1
print(p2Hand)
print(p3Hand)
print(p4Hand)


play()



def test():
    this = [1, 2, 3, 4]
    this[2:] = []

test()