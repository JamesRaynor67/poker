def printCards(Cards):
    cardType = ["♠", "♥", "♦", "♣"]
    for card in Cards:
        cardValue = card//4
        if cardValue < 9:
            print(cardType[card%4] + str(cardValue+2), end=" ")
        elif cardValue == 9:
            print(cardType[card%4] + 'J', end=" ")
        elif cardValue == 10:
            print(cardType[card%4] + 'Q', end=" ")
        elif cardValue == 11:
            print(cardType[card%4] + 'K', end=" ")
        elif cardValue == 12:
            print(cardType[card%4] + 'A', end=" ")
        else:
            print("error!" + str(card))
    print(" (" + str(Cards) + ")")


def decodeSevenCardId(sevenCardId):
    cardIntList = [-1] * 7
    for i in range(7):
        cardIntList[i] = (sevenCardId % 52)
        sevenCardId = sevenCardId // 52
    return cardIntList


def readableCardsToCardsInt(readAbleCards):
    # cardType = ["♠", "♥", "♦", "♣"]
    # S(pade), H(eart), D(iamond), C(lub)
    # S2, S3, S4,...,S10, SJ, SQ, SK, SA
    cardsInt = []
    for card in readAbleCards:
        cardSuit = card[0]
        cardType = card[1:]
        cardInt = 0
        if cardType == "J":
            cardInt = 9 * 4
        elif cardType == "Q":
            cardInt = 10 * 4
        elif cardType == "K":
            cardInt = 11 * 4
        elif cardType == "A":
            cardInt = 12 * 4
        else:
            assert 2 <= int(cardType) and int(cardType) <=10, "invalid input of card: " + str(readAbleCards) + " (" + str(card) + ")"
            cardInt = (int(cardType) - 2) * 4
        
        if cardSuit == "S":
            cardInt += 0
        elif cardSuit == "H":
            cardInt += 1
        elif cardSuit == "D":
            cardInt += 2
        elif cardSuit == "C":
            cardInt += 3
        else:
            assert False, "invalid input of card: " + str(readAbleCards) + " (" + str(card) + ")"
        cardsInt.append(cardInt)
    return cardsInt

noPairTestSuit1 = [50,45,38,22,0]
noPairTestSuit2 = [51,35,30,17,8]
noPairTestSuit3 = [40,34,20,11,2]
onePairTestSuit1 = [51,50,30,12,0]
onePairTestSuit2 = [51,50,31,12,0]
onePairTestSuit3 = [51,23,22,8,0]
twoPairTestSuit1 = [51,50,15,14,0]
twoPairTestSuit2 = [51,50,14,13,0]
twoPairTestSuit3 = [33,32,23,1,0]
threeofAKindTestSuit1 = [51,32,2,1,0]
threeofAKindTestSuit2 = [22,16,10,9,8]
straightTestSuit1 = [6*4+1,5*4+3,4*4+2,3*4+0,2*4+1]
straightTestSuit2 = [12*4+3,11*4+2,10*4+1,9*4+2,8*4+0]
straightTestSuit3 = [9*4+2,8*4+1,7*4+1,6*4+2,5*4+1]
flushTestSuit1 = [48,36,24,12,0]
flushTestSuit2 = [51,39,27,15,3]
fullHouseTestSuit1 = [50,49,48,1,0]
fullHouseTestSuit2 = [51,33,2,1,0]
fourOfAKindTestSuit1 = [39,38,37,36,2]
fourOfAKindTestSuit2 = [51,39,38,37,36]
fourOfAKindTestSuit3 = [51,50,49,48,0]
straightFlushTestSuit1 = [6*4+1,5*4+1,4*4+1,3*4+1,2*4+1]
straightFlushTestSuit1 = [4*4+0,3*4+0,2*4+0,1*4+0,0*4+0]
testList = [noPairTestSuit1, straightTestSuit2, threeofAKindTestSuit1, 
            onePairTestSuit1, straightFlushTestSuit1, fullHouseTestSuit1, 
            noPairTestSuit1, flushTestSuit2,onePairTestSuit3]
