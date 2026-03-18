from copy import deepcopy
import itertools
import math
import random
import time
import msvcrt
from turtle import screensize

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

replay = True

tileSuitedTemplate = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
tileDragonTemplate = ["HZ", "BB", "FC"]
tileWindTemplate = ['E', 'S', 'W', 'N']
tileBonusTemplate = ["Plum", "Orchid", "Chrysanthemum", "Bamboo", "Spring", "Summer", "Autumn", "Winter"]
discardPile = []
discardPileVisuals = []
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
        while msvcrt.kbhit():
            msvcrt.getch()
        match input("Read Instructions? (Y/N)").upper().strip():
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
                #print("There also exists several unique ways of winning, for you to unlock.")
                time.sleep(0.5)
                print()
                print()
            case 'N':
                print("Suit yourself.")
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
        print("Roll (press any key):")
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
            while msvcrt.kbhit():
                msvcrt.getch()
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
                    diceTotal[0].remove(min(diceTotal[0]))

        hands = hands[diceTotal[1][0]:] + hands[:diceTotal[1][0]]
        time.sleep(0.3)
        print("Player %s is East. Player %s is South. Player %s is West. Player %s is North." % (diceTotal[1][0] % 4 + 1, (diceTotal[1][0] + 1) % 4 + 1, (diceTotal[1][0] + 2) % 4 + 1, (diceTotal[1][0] + 3) % 4 + 1))
        playOrder = [diceTotal[1][0] % 4, (diceTotal[1][0] + 1) % 4, (diceTotal[1][0] + 2) % 4, (diceTotal[1][0] + 3) % 4]
        time.sleep(1)

        diceTotal = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)

        dealOrder = walls[diceTotal % 4] + walls[(diceTotal + 1) % 4] + walls[(diceTotal + 2) % 4] + walls[(diceTotal + 3) % 4]
        dealOrder = dealOrder[(diceTotal - 1) * 2 + 1:] + dealOrder[:(diceTotal - 1) * 2 + 1]

        print()
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
        print()
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

    explanation()
    wall()
    dealing()

def play():

    options = ["Draw", "Discard", "Discard Pile", "Swap", "Meld"]
    meldAbbreviations = {'E': "Eye", 'P': "Pung", 'G': "Gong", 'S': "Seon"}
    winning = [False, False, False, False]
    global won
    won = [False, None, []] # 1: if won, 2: who won, 3: hand that won/did not
    global p1HandVisuals

    def discard(hand, tileIndex):
        discardPile.append(hands[hand].pop(tileIndex))

    def bonus():
        while bool(set([*p1Hand, *p2Hand, *p3Hand, *p4Hand]) & set(tileBonusTemplate)):
            for index, hand in enumerate(playOrder):
                if bool(set(hands[index]) & set(tileBonusTemplate)):
                    time.sleep(0.5)
                    if hand == 0:
                        print("Player 1:") 
                        print("Choose a bonus tile (Use A,D)\n")
                        select = 0
                        selected = False
                        bonusTiles = [i for i in p1Hand if i in tileBonusTemplate]
                        reprint = True
                        while selected is False:
                            if reprint:
                                print("\x1b[F\x1b[K" + "  ".join([f"\x1b[1;4m{i}\x1b[0m" if i == bonusTiles[select] else (i if i in bonusTiles else f"\x1b[38;5;247m{i}\x1b[0m") for i in p1Hand]))
                                reprint = False
                            if msvcrt.kbhit():
                                reprint = True
                                try:
                                    key = msvcrt.getch().decode()
                                except:
                                    key = None
                                match key:
                                    case 'a':
                                        select -= 1
                                    case 'd':
                                        select += 1
                                    case '\r' | ' ':
                                        selected = True
                                    case 'A':
                                        select = 0
                                    case 'D':
                                        select = len(bonusTiles) - 1
                                    case _:
                                        reprint = False
                                        continue
                                if select < 0:
                                    select = 0
                                if select >= len(bonusTiles):
                                    select = len(bonusTiles) - 1

                        p1Hand.remove(bonusTiles[select])
                        removeFromWall(1, index, -1)
                        print("You discarded %s and drew %s from the back." % (bonusTiles[select], tileVisuals([p1Hand[-1]])[0]))

                    else:
                        hands[index].remove(list(set(hands[index]) & set(tileBonusTemplate))[0])
                        removeFromWall(1, index, -1)
                        print("Player %s discarded a bonus tile and drew from the back." % (hand + 1))

    def checkMeld(handIndex):
        hand = hands[playOrder.index(handIndex)]
        melds = []

        if not bool(discardPile):
            return False, None
        discarded = discardPile[-1]
        if hand.count(discarded) >= 2 or hand.count(discarded) >= 2 and winning[0]: # identical melds
            #melds.append([[discarded] + [i for i, v in enumerate(hand) if v == discarded], ('E' if hand.count(discarded) == 1 and winning else ('G' if hand.count(discarded == 3) else ('P')))])
            if hand.count(discarded) == 1 and winning[0]:
                melds.append([[discarded] + [i for i, v in enumerate(hand) if v == discarded], 'E'])
            elif hand.count(discarded) == 3:
                melds.append([[discarded] + [i for i, v in enumerate(hand) if v == discarded], 'G'])
            elif hand.count(discarded) == 2:
                melds.append([[discarded] + [i for i, v in enumerate(hand) if v == discarded], 'P'])

        if discarded[-1] in [str(i) for i in range(1, 10)]: # Seons
            for i, v in enumerate(hand):
                if v[0] == discarded[0] and len(v) == 2:
                    current_v = [discarded]
                    current_i = [discarded]
                    if abs(int(v[1]) - int(discarded[1])) == 1:
                        current_v.append(v)
                        current_i.append(i)
                        current_v.sort()
                        for i1, v1 in enumerate(hand):
                            if v1[-1] not in [str(i) for i in range(1, 10)] or v1[0] != discarded[0]:
                                continue
                            if int(v1[1]) - int(current_v[1][1]) == 1:
                                breakFor = False
                                for i in melds:
                                    if set(i[0]) == set(current_i + [i1]):
                                        breakFor = True
                                        break
                                if not breakFor:
                                    melds.append([current_i + [i1], 'S'])
                            elif int(current_v[0][1]) - int(v1[1]) == 1:
                                breakFor = False
                                for i in melds:
                                    if set(i[0]) == set(current_i + [i1]):
                                        breakFor = True
                                        break
                                if not breakFor:
                                    melds.append([current_i + [i1], 'S'])
        
        if bool(melds):
            return True, melds
        else:
            return False, None

    def callMeld(handIndex, melds): # for ai only?
        pass

    def checkWin(handIndex):
        hand = deepcopy(hands[handIndex])
        melds = [i.replace('>', '-').replace('\x1b[38;5;34m', '-').replace('\x1b[38;5;160m', '-').replace('\x1b[0m', '-').split('-') for i in revealedMelds[handIndex]]
        possibleMelds = []
        for i, v in enumerate(hand): # for each tile in your hand
            if hand.count(v) >= 2: # identical melds
                #print("mults", i, v)
                copies = [i1 for i1, v1 in enumerate(hand) if v1 == v]
                perms = []
                for i1 in range(2, len(copies) + 1):
                    perms += tuple(set([tuple(sorted(i2)) for i2 in itertools.permutations(copies, i1)]))
                for perm in perms:
                    listMeld = [perm, (list(meldAbbreviations.keys())[len(perm) - 2])]
                    possibleMelds += [tuple(listMeld)]
                possibleMelds = list(set(possibleMelds))
            
            if v[-1] in [str(i1) for i1 in range(1, 10)]: # Seons
                for i1, v1 in enumerate(hand):
                    if v1[0] == v[0] and len(v1) == 2: # if matching suits
                        current_v = [v]
                        current_i = [i]
                        if abs(int(v1[1]) - int(v[1])) == 1: # if consecutive to original number
                            current_v.append(v1)
                            current_i.append(i1)
                            current_v.sort()
                            #print("strings", current_v, current_i)
                            for i2, v2 in enumerate(hand):
                                if len(v2) != 2 or v2[0] != v[0]:
                                    continue
                                if int(v2[1]) - int(current_v[1][1]) == 1: # if third tile is consecutive to end
                                    breakFor = False
                                    #print(i2, v2)
                                    for i3 in possibleMelds:
                                        if set(i3[0]) == set(current_i + [i2]):
                                            breakFor = True
                                            break
                                    if not breakFor:
                                        possibleMelds.append(tuple([tuple(current_i + [i2]), 'S']))
                                elif int(current_v[0][1]) - int(v2[1]) == 1: # if third tile is consecutive to start
                                    breakFor = False
                                    #print(i2, v2)
                                    for i3 in possibleMelds:
                                        if set(i3[0]) == set(current_i + [i2]):
                                            breakFor = True
                                            break
                                    if not breakFor:
                                        possibleMelds.append(tuple([tuple(current_i + [i2]), 'S']))
        
        possibleMelds.sort(key=lambda x: len(x[0]), reverse=True)
        def meldAHand(meldedHand, breakFor):
            for i, v in enumerate(possibleMelds): # check if melds make up the hand
                if set(v[0]) <= meldedHand: # if full subset
                    meldedHand -= set(v[0])
                    meldHand.append(i)
                    match len(meldedHand):
                        case 0:
                            meldHand.sort(key=lambda x: len(possibleMelds[x][0]), reverse=True)
                            if len(possibleMelds[meldHand[-2]][0]) > 2:
                                winningHand = ("   ".join([('>' if i1[1] == 'S' else '-').join(sorted([hand[i2] for i2 in i1[0]])) for i1 in [possibleMelds[i4] for i4 in meldHand]]))
                                global won
                                won = [True, playOrder[handIndex], winningHand]
                                breakFor.append(True)
                            else:
                                breakFor.append(False)
                        case 2:
                            meldHand.sort(key=lambda x: len(possibleMelds[x][0]), reverse=True)
                            if len(possibleMelds[meldHand[-2]]) > 2:
                                winning[playOrder[handIndex]] = True
                            breakFor.append(meldAHand(meldedHand, breakFor))
                        case 3:
                            meldHand.sort(key=lambda x: len(possibleMelds[x][0]), reverse=True)
                            if len(possibleMelds[meldHand[-2]]) > 2 and len(possibleMelds[meldHand[-2]]) == 2:
                                winning[playOrder[handIndex]] = True
                            breakFor.append(meldAHand(meldedHand, breakFor))
                        case _:
                            breakFor.append(meldAHand(meldedHand, breakFor))
                    if breakFor[-1]:
                        return True
                    meldedHand |= set(v[0])
                    meldHand.pop()
                    breakFor.pop()
                

        meldedHand = set(range(14 - 2 * len(melds)))
        meldHand = []
        breakFor = [False]
        meldAHand(meldedHand, breakFor)
                        

                
        pass

    def tileVisuals(tiles):
        for i, v in enumerate(tiles):
            match v:
                case v if len(v) == 1:
                    pass
                case v if v[0] == 'K':
                    tiles[i] = f"\x1b[38;5;160m{v}\x1b[0m"
                case v if v[0] == 'S':
                    tiles[i] = f"\x1b[38;5;34m{v}\x1b[0m"
                case v if v[0] == 'D':
                    pass
                case v if v[0] == 'H':
                    tiles[i] = f"\x1b[38;5;160m{v}\x1b[0m"
                case v if v[0] == 'F':
                    tiles[i] = f"\x1b[38;5;34m{v}\x1b[0m"
                case _:
                    pass
        return tiles

    def aiTurn(ai):
        canMeld, melds = checkMeld(ai)
        """if canMeld:
            callMeld(ai, melds)
        elif turn != 0:"""
        if turn != 0:
            removeFromWall(1, playOrder.index(ai))
            print("Player %s drew a tile." % (ai + 1))
        checkWin(playOrder.index(ai))
        time.sleep(0.5)
        bonus()
        discard(playOrder.index(ai), random.randint(0, len(hands[ai]) - 1))
        print("Player %s discarded %s." % (ai + 1, hands[playOrder.index(ai)]))
        pass

    def p1Turn():
        print("---[ Next Round ]---")
        print("Player 2: %s Tiles, Exposed Melds: %s" % (len(p2Hand), ", ".join(revealedMelds[1])))
        print("Player 3: %s Tiles, Exposed Melds: %s" % (len(p3Hand), ", ".join(revealedMelds[2])))
        print("Player 4: %s Tiles, Exposed Melds: %s" % (len(p4Hand), ", ".join(revealedMelds[3])))
        print("Player 1:") 
        print("Your Exposed Melds:")
        print("   ".join(revealedMelds[0]))
        
        canDraw = turn != 0
        canDiscard = turn == 0
        canCheck = turn != 0
        canSwap = True
        canMeld, melds = checkMeld(0)
        endTurn = False

        global p1HandVisuals
        listSelect = 0 # options = 0, cards = 1
        mode = None
        chosen = []
        reprint = True
        confirmMeld = False
        meldAvailable = None

        print("\n\n")
        while endTurn == False:
            canOption = [canDraw, canDiscard, canCheck, canSwap, canMeld]
            if listSelect == 0:
                selectable = [i for i, v in enumerate(canOption) if v]
            elif listSelect == 1 and mode in (1, 3, 4):
                selectable = [i for i, v in enumerate(p1Hand) if i not in chosen]
            elif listSelect == 1 and mode == 2:
                selectable = discardPile
            select = 0
            selected = False
            while selected is False: # key detect ----------------------
                if listSelect == 0 and reprint:
                    print("\x1b[3F\x1b[JOptions:")
                    print("Choose an option.")
                    print("--> " + " <--> ".join([(f"\x1b[1;4m{v}\x1b[0m" if selectable[select] == i else v) if canOption[i] else f"\x1b[38;5;247m{v}\x1b[0m" for i, v in enumerate(options)]) + " <--")
                elif listSelect == 1 and mode in (1, 3) and reprint:
                    print("\x1b[F" + "  ".join([f"\x1b[1;4m{v}\x1b[0m" if select == i else v for i, v in enumerate(p1HandVisuals)]))
                elif listSelect == 1 and mode == 4 and reprint:
                    print("\x1b[F" + "  ".join([f"\x1b[1;4m{p1HandVisuals[i]}\x1b[0m" if selectable[select] == i else (f"\x1b[38;5;247m{v}\x1b[0m" if i in chosen else p1HandVisuals[i]) for i, v in enumerate(p1Hand)]))
                elif listSelect == 1 and mode == 2 and reprint:
                    print("\x1b[3F\x1b[JThe Discard Pile:")
                    print("Top of discard pile is the left.")
                    discardPrint = [f"\x1b[1;4m{v}\x1b[0m" if select == i else v for i, v in enumerate(discardPileVisuals[::-1])]
                    if len(discardPile) > 30:
                        discardPrint = discardPrint[:30] + ["..."]
                    print("  ".join(discardPrint))
                reprint = False
                if msvcrt.kbhit():
                    reprint = True
                    try:
                        key = msvcrt.getch().decode()
                    except:
                        key = msvcrt.getch()
                    match key:
                        case 'a':
                            select -= 1
                        case 'd':
                            select += 1
                        case '\r' | ' ':
                            if mode != 2:
                                selected = True
                            else:
                                reprint = False
                        case 'A':
                            select = 0
                        case 'D':
                            if listSelect == 0:
                                select = len(options) - 1
                            elif listSelect == 1:
                                select = len(p1Hand) - 1
                            elif listSelect == 2:
                                select = len(discardPile) - 1
                        case '\x1b':
                            if listSelect == 1 and mode in (1, 2):
                                listSelect = 0
                                mode = None
                                print("\x1b[F")
                                selectable = [i for i, v in enumerate(canOption) if v]
                            elif listSelect == 1 and mode in (3, 4):
                                if not bool(chosen):
                                    listSelect = 0
                                    mode = None
                                    print("\x1b[F")
                                    selectable = [i for i, v in enumerate(canOption) if v]
                                else:
                                    if mode == 3:
                                        chosen = []
                                        print("\x1b[3F\x1b[JChoose two cards to swap.")
                                        print("You have chosen None.")
                                        print()
                                        selectable = [i for i, v in enumerate(p1Hand)]
                                    if mode == 4:
                                        chosen = chosen[:-1]
                                        print("\x1b[2F\x1b[JYou have chosen %s. " % (" and ".join([p1Hand[i] for i in chosen]) if bool(chosen) else "None"), end='')
                                        for meld in melds:
                                            if sorted([p1Hand[i] for i in meld[0] if type(i) == int]) == sorted([p1Hand[i] for i in chosen]):
                                                print("(%s) (Press E to confirm)" % (meldAbbreviations[meld[1]]), end='')
                                                meldAvailable = meld
                                                break
                                        print("\n")
                                        selectable = [i for i, v in enumerate(p1Hand) if i not in chosen]
                        case 'e':
                            if bool(meldAvailable):
                                confirmMeld = True
                                selected = True
                            else:
                                reprint = False
                                continue
                        case _:
                            reprint = False
                            continue
                    if select < 0:
                        select = 0
                    elif select >= len(selectable):
                        select = len(selectable) - 1

            if listSelect == 0: # something was selected -----------------------------------
                listSelect = 1
                mode = selectable[select]
                match mode:
                    case 0:
                        listSelect = 0
                        removeFromWall(1, playOrder.index(0), 0)
                        canDraw = False
                        canDiscard = True
                        canMeld = False
                        reprint = False
                        canOption = [canDraw, canDiscard, canCheck, canSwap, canMeld]
                        selectable = [i for i, v in enumerate(canOption) if v]
                        p1HandVisuals = tileVisuals(deepcopy(p1Hand))
                        print("\x1b[3F\x1b[JOptions:")
                        print("You drew a %s." % (p1HandVisuals[-1]))
                        print("--> " + " <--> ".join([(f"\x1b[1;4m{v}\x1b[0m" if selectable[select] == i else v) if canOption[i] else f"\x1b[38;5;247m{v}\x1b[0m" for i, v in enumerate(options)]) + " <--")
                        if bool(set(p1Hand) & set(tileBonusTemplate)):
                            bonus()
                            print("\n\n")
                            p1HandVisuals = tileVisuals(deepcopy(p1Hand))
                            reprint = True
                        checkWin(playOrder.index(0))
                        if won[0]:
                            return
                        if winning[0]:
                            print("\x1b[4F\x1b[JYou are one tile from winning!")
                            print("\n\n\n")
                    case 1:
                        print("\x1b[3F\x1b[JDiscard one card:")
                        print("(Ends turn immediately)")
                        print()
                    case 2:
                        discardPileVisuals = tileVisuals(deepcopy(discardPile))
                        print("\x1b[3F\x1b[JThe Discard Pile:")
                        print("Top of discard pile is the left.")
                        print()
                    case 3:
                        print("\x1b[3F\x1b[JChoose two cards to swap:")
                        print("You have chosen None.")
                        print()
                    case 4:
                        chosen = []
                        print("\x1b[3F\x1b[JSelect tiles:")
                        print("You have chosen %s." % (" and ".join([p1Hand[i] for i in chosen]) if bool(chosen) else "None"))
                        print()
            elif listSelect == 1:
                match mode:
                    case 1:
                        print("You discarded %s." % (p1HandVisuals[select]))
                        discard(playOrder.index(0), select)
                        endTurn = True
                    case 3:
                        if not bool(chosen):
                            chosen.append(select)
                            print("\x1b[3F\x1b[JChoose another cards to swap:")
                            print("You have chosen %s." % (p1Hand[select]))
                            print()
                        else:
                            chosen = [[chosen[0], p1Hand[chosen[0]]], [select, p1Hand[select]]]
                            chosenVisuals = (p1HandVisuals[chosen[0][0]], p1HandVisuals[select])
                            p1Hand[chosen[0][0]] = chosen[0][1]
                            p1Hand[chosen[1][0]] = chosen[1][1]
                            p1HandVisuals[chosen[0][0]] = chosenVisuals[1]
                            p1HandVisuals[chosen[1][0]] = chosenVisuals[0]
                            print("\x1b[3F\x1b[JChoose two cards to swap.")
                            print("You swapped %s with %s." % (chosenVisuals[0], chosenVisuals[1]))
                            print()
                            chosen = []
                            chosenVisuals = (None,)
                    case 4:
                        if not confirmMeld:
                            if len(chosen) == 3:
                                continue
                            chosen.append(selectable[select])
                            print("\x1b[2F\x1b[JYou have chosen %s. " % (" and ".join([p1Hand[i] for i in chosen]) if bool(chosen) else "None"), end='')
                            meldAvailable = None
                            for meld in melds:
                                if sorted([p1Hand[i] for i in meld[0] if type(i) == int]) == sorted([p1Hand[i] for i in chosen]):
                                    print("(%s) (Press E to confirm)" % (meldAbbreviations[meld[1]]), end='')
                                    meldAvailable = meld
                                    break
                            print("\n")
                        else:
                            print("\x1b[3F\x1b[JYou created a %s with %s." % (meldAbbreviations[meld[1]], " and ".join([p1HandVisuals[int(i)] for i in meldAvailable[0] if str(i).isdigit()])))
                            print("\n\n\n")
                            revealedMelds[0].append(['>'.join([tileVisuals([i])[0] for i in sorted([(p1Hand[i1] if str(i1).isdigit() else i1) for i1 in meldAvailable[0]])]) if meldAvailable[1] == 'S' else '-'.join((2 + list(meldAbbreviations.keys()).index(meldAvailable[1])) * [meldAvailable[0][0]])][0])
                            for i in sorted(chosen, reverse=True):
                                p1Hand.pop(i)
                            discardPile.pop()
                            discardPileVisuals.pop()
                            p1HandVisuals = tileVisuals(deepcopy(p1Hand))
                            if meld[1] == 'G':
                                removeFromWall(1, playOrder.index(0), -1)
                                print("\x1b[3F\x1b[JOptions:")
                                print("You drew a %s." % (p1HandVisuals[-1]))
                                print("--> " + " <--> ".join([(f"\x1b[1;4m{v}\x1b[0m" if selectable[select] == i else v) if canOption[i] else f"\x1b[38;5;247m{v}\x1b[0m" for i, v in enumerate(options)]) + " <--")
                                if bool(set(p1Hand) & set(tileBonusTemplate)):
                                    bonus()
                                    print("\n")
                                    p1HandVisuals = tileVisuals(deepcopy(p1Hand))
                                    reprint = True
                            checkWin(playOrder.index(0))
                            if winning[0]:
                                print("\x1b[4FYou are one tile from winning!")
                                print("\n\n\n")
                            chosen = []
                            listSelect = 0
                            mode = None
                            canDraw = False
                            canDiscard = True
                            canMeld = False
                            confirmMeld = False
                            selectable = [i for i, v in enumerate(canOption) if v]

    print("------[ Playing Phase ]------")
    
    print("---[ First Round: Bonus Tiles ]---")
    time.sleep(0.5)
    print("Any Bonus Tiles?")
    while msvcrt.kbhit():
        msvcrt.getch()
    bonus()
    print()
    time.sleep(1)
    
    turn = 0
    while True: # main playing loop
        time.sleep(1)
        print("\n")
        while msvcrt.kbhit():
            msvcrt.getch()
        if playOrder[turn % 4] != 0:
            aiTurn(playOrder[turn % 4])
            canMeld, melds = checkMeld(0)
            if canMeld and bool([i for i in melds if i[1] != 'S']):
                pass
        else:
            p1HandVisuals = tileVisuals(deepcopy(p1Hand))
            p1Turn()
        bonus()
        if won[0] or len(dealOrder) == 0:
            break
        turn += 1

    global replay
    replay = False
    if won[0]:
        print("Player %s won the game with the following hand:" % (won[1] + 1))
        print(won[2])

        match input("Play again? (Y or N)\x1b[?25h").upper().strip():
            case 'Y':
                replay = True
            case 'N':
                print("Thanks for playing Pyjong,")
                print("Remember to check out LeadPipe Corporation's games!")
            case _:
                print("You went through that whole game without pressing a single wrong key,")
                print("And then you do this?")
    elif len(dealOrder) == 0:
        print("The draw pile ran out without anyone winning!")
        match input("Play again? (Y or N)\x1b[?25h").upper().strip():
            case 'Y':
                replay = True
            case 'N':
                print("Thanks for playing Pyjong,")
                print("Remember to check out LeadPipe Corporation's games!")
            case _:
                print("You went through that whole game without pressing a single wrong key,")
                print("And then you do this?")
    pass



while replay:
    initialisation()
    play()



def test():
    while False:
        this = msvcrt.getch().decode()
        print("1" + this + "1")
        break

test()