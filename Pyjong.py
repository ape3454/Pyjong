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

    Melds:
    P = Pung
    S = Seon(straight)
    G = Gong
    N = Eye
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
p1HandVisuals = []
p2Hand = []
p3Hand = []
p4Hand = []
global hands
hands = [p1Hand, p2Hand, p3Hand, p4Hand]
playOrder = []
revealedMelds = [[], [], [], []]

def removeFromWall(number, hand, index=0):
        global hands

        for i in range(number):
            hands[hand] += [dealOrder.pop(index)]

def initialisation():
    print("\x1b[?25l", end='')
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
        global playOrder

        print("------[ Dealing Phase ]------")
        time.sleep(0.2)
        """print("Roll (press any key):")
        msvcrt.getch()

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
            time.sleep(0.2)
            print("There was a tie!")
            time.sleep(0.2)
            diceTotal[0] = []
            for player in diceTotal[1][:]:
                diceTotal[0].append(random.randint(1, 6))
                if player == 0:
                    print("Roll:")
                    msvcrt.getch()
                    time.sleep(3)
                    print("You rolled a", diceTotal[0][-1])
                else:
                    time.sleep(3)
                    print("Player %s rolled a %s" % (player + 1, diceTotal[0][-1]))
                if len(set(diceTotal[0])) >= 2:
                    diceTotal[1].remove(diceTotal[1][diceTotal[0].index(min(diceTotal[0]))])
                    diceTotal[0].remove(min(diceTotal[0]))"""

        diceTotal = [6, [0]]

        hands = hands[diceTotal[1][0]:] + hands[:diceTotal[1][0]]
        time.sleep(0.3)
        print("Player %s is East. Player %s is South. Player %s is West. Player %s is North." % (diceTotal[1][0] % 4 + 1, (diceTotal[1][0] + 1) % 4 + 1, (diceTotal[1][0] + 2) % 4 + 1, (diceTotal[1][0] + 3) % 4 + 1))
        playOrder = [diceTotal[1][0] % 4, (diceTotal[1][0] + 1) % 4, (diceTotal[1][0] + 2) % 4, (diceTotal[1][0] + 3) % 4]
        time.sleep(1)

        diceTotal = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)

        dealOrder = walls[diceTotal % 4] + walls[(diceTotal + 1) % 4] + walls[(diceTotal + 2) % 4] + walls[(diceTotal + 3) % 4]
        dealOrder = dealOrder[(diceTotal - 1) * 2 + 1:] + dealOrder[:(diceTotal - 1) * 2 + 1]

        """print()
        for i in range(random.choices([1, 2, 3, 4, 7], weights=[2, 10, 10, 3, 1])[0]):
            time.sleep(2)
            print("Shuffling", end='', flush=True)
            time.sleep(0.9)
            for i in range(3):
                print(".", end='', flush=True)
                time.sleep(0.9)
            print()
        time.sleep(2)"""
        
        # diceTotal represents wall shift of dealOrder
        dels = len(walls[diceTotal % 4][diceTotal:])
        walls[diceTotal % 4][diceTotal:] = []
        if 53 - dels <= 36:
            walls[(diceTotal + 1) % 4][:53 - dels] = []
        else:
            walls[(diceTotal + 1) % 4] = []
            walls[(diceTotal + 2) % 4][:17 - dels] = []
        """print()
        for i in range(3):
            time.sleep(2)
            print("Dealing", end='', flush=True)
            time.sleep(0.9)
            for i in range(3):
                print(".", end='', flush=True)
                time.sleep(0.9)
            print()
        time.sleep(2)"""

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

    options = ["Draw", "Discard", "Swap", "Meld"]
    melds = [] # list of lists in form [[discarded tile, [tiles in hand]], type of meld]
    winning = False

    def bonus():
        while bool(set([*p1Hand, *p2Hand, *p3Hand, *p4Hand]) & set(tileBonusTemplate)):
            for index, hand in enumerate(playOrder):
                if bool(set(hands[index]) & set(tileBonusTemplate)):
                    if hand == 0:
                        print("Player 1:") 
                        print("Choose a bonus tile (Use A,D)")
                        print("  ".join([f"\x1b[38;5;247m{v}\x1b[0m" if v in tileBonusTemplate else v for v in p1Hand]))
                        select = 0
                        selected = False
                        bonusTiles = [i for i in p1Hand if i in tileBonusTemplate]
                        while selected is False:
                            if msvcrt.kbhit():
                                try:
                                    key = msvcrt.getch().decode()
                                except:
                                    key = None
                                match key:
                                    case 'a':
                                        select -= 1
                                    case 'd':
                                        select += 1
                                    case '\r':
                                        selected = True
                                    case 'A':
                                        select = 0
                                    case 'D':
                                        select = len(bonusTiles) - 1
                                    case _:
                                        continue
                                if select < 0:
                                    select = 0
                                if select >= len(bonusTiles):
                                    select = len(bonusTiles) - 1
                            print("\x1b[1F" + "  ".join([f"\x1b[1;4m{i}\x1b[0m" if i == bonusTiles[select] else (i if i in bonusTiles else f"\x1b[38;5;247m{i}\x1b[0m") for i in p1Hand]))

                        p1Hand.remove(bonusTiles[select])
                        removeFromWall(1, hand, -1)

                    else:
                        hands[index].remove(list(set(hands[index]) & set(tileBonusTemplate))[0])
                        removeFromWall(1, hand, -1)

    def checkMeld():
        global melds

        discarded = discardPile[-1]
        if p1Hand.count(discarded) >= 2 or p1Hand.count(discarded) == 1 and winning == True: # identical melds
            if p1Hand.count(discarded) == 1:
                melds.append([[discarded, [i for i, v in enumerate(p1Hand) if v == discarded]], 'E'])
            elif p1Hand.count(discarded) == 3:
                melds.append([[discarded, [i for i, v in enumerate(p1Hand) if v == discarded]], 'G'])
            else:
                melds.append([[discarded, [i for i, v in enumerate(p1Hand) if v == discarded]], 'P'])

        if len(discarded) == 2: # Seons
            if discarded[1] in tileSuitedTemplate:
                for i, v in enumerate(p1Hand):
                    if v[0] == discarded[0]:
                        current_v = [discarded]
                        current_i = [discarded]
                        if abs(int(v[1]) - int(discarded[1])) == 1:
                            current_v.append(v)
                            current_i.append(i)
                            current_v.sort()
                            for i1, v1 in enumerate(p1Hand):
                                if int(v1[1]) - int(current_v[0][1]) == 1:
                                    current_i.append(i1)
                                    melds.append([current_i, 'S'])
                                elif int(current_v[1][1]) - int(v1[1]) == 1:
                                    current_i.append(i1)
                                    melds.append([current_i, 'S'])
        
        if bool(melds):
            return True

    def tileVisuals():
        for i, v in enumerate(p1Hand):
            match v:
                case v if len(v) == 1:
                    pass
                case v if v[0] == 'K':
                    p1HandVisuals[i] = f"\x1b[38;5;160m{v}\x1b[0m"
                case v if v[0] == 'S':
                    p1HandVisuals[i] = f"\x1b[38;5;34m{v}\x1b[0m"
                case v if v[0] == 'D':
                    pass
                case v if v[0] == 'H':
                    p1HandVisuals[i] = f"\x1b[38;5;160m{v}\x1b[0m"
                case v if v[0] == 'F':
                    p1HandVisuals[i] = f"\x1b[38;5;34m{v}\x1b[0m"
                case _:
                    pass

    def discardTurn():
        if playOrder[0] == 0:
            print("Player 1:") 
            print("Your Tiles:")
            print("  ".join(p1Hand))
            print("Options:")
            print("Choose an option.")
            print()
            canDraw = False
            canDiscard = True
            canSwap = True
            canMeld = False
            canOption = [canDraw, canDiscard, canSwap, canMeld]
        
            endTurn = False
            listSelect = 0 # options = 0, cards = 1
            selectable = [1, 2]
            while endTurn == False:
                select = 0
                selected = False
                while selected is False:
                    if listSelect == 0:
                        print("\x1b[2F\x1b[KChoose an option.")
                        print("\x1b[K--> " + " <--> ".join([(f"\x1b[1;4m{v}\x1b[0m" if selectable[select] == i else v) if canOption[i] else f"\x1b[38;5;247m{v}\x1b[0m" for i, v in enumerate(options)]) + " <--")
                    elif listSelect == 1:
                        print("\x1b[F" + "  ".join([f"\x1b[1;4m{v}\x1b[0m" if select == i else v for i, v in enumerate(p1HandVisuals)]))
                    if msvcrt.kbhit():
                        try:
                            key = msvcrt.getch().decode()
                        except:
                            key = msvcrt.getch()
                        match key:
                            case 'a':
                                select -= 1
                            case 'd':
                                select += 1
                            case '\r':
                                selected = True
                            case 'A':
                                select = 0
                            case 'D':
                                if listSelect == 0:
                                    select = len(options) - 1
                                elif listSelect == 1:
                                    select = len(p1Hand) - 1
                            case '\x1b':
                                if listSelect == 1:
                                    listSelect = 0
                            case _:
                                continue
                        if select < 0:
                            select = 0
                        if listSelect == 0:
                            if select >= len(selectable):
                                select = len(selectable) - 1
                        elif listSelect == 1:
                            if select >= len(p1Hand):
                                select = len(p1Hand) - 1
                if listSelect == 0:
                    listSelect = 1
                    if select == 0:
                        print("\x1b[2F\x1b[KDiscard one card.")
                        print()
                    elif select == 1:
                        print("\x1b[2F\x1b[KChoose two cards to swap.")
                        print()
                

    def newTurn():
        print("---[ Next Round ]---")
        print("Player 2: %s Tiles, Exposed Melds: %s" % (len(p2Hand), ", ".join(revealedMelds[1])))
        print("Player 3: %s Tiles, Exposed Melds: %s" % (len(p3Hand), ", ".join(revealedMelds[2])))
        print("Player 4: %s Tiles, Exposed Melds: %s" % (len(p4Hand), ", ".join(revealedMelds[3])))
        print("Player 1:") 
        print("Your Exposed Melds:")
        print(", ".join(revealedMelds[0]))
        print("Your Tiles:")
        print("  ".join(p1Hand))
        
        print("Options:")
        canDraw = True
        canDiscard = False
        canSwap = True
        if checkMeld():
            canMeld = True

        print("--> " + " <--> ".join(options) + " <--")


    print("------[ Playing Phase ]------")
    
    print("---[ First Round: Bonus Tiles ]---")
    time.sleep(0.5)
    print("Bonus Tiles?")

    p1HandVisuals = p1Hand
    tileVisuals()
    bonus()
    p1HandVisuals = p1Hand
    tileVisuals()
    discardTurn()

    while True:
        newTurn()
        break



    pass



initialisation()


play()



def test():
    while True:
        this = [msvcrt.getch().decode]
        print(this[0] == b'\x1b')
        break

test()