# -*- coding: utf-8 -*-

def printUnicodeCards(Cards):
    cardType = ["♠", "♥", "♦", "♣"]
    unicodeCards = []
    for card in Cards:
        cardValue = card//4
        if cardValue < 9:
            unicodeCards.append(cardType[card%4] + str(cardValue+2))
        elif cardValue == 9:
            unicodeCards.append(cardType[card%4] + 'J')
        elif cardValue == 10:
            unicodeCards.append(cardType[card%4] + 'Q')
        elif cardValue == 11:
            unicodeCards.append(cardType[card%4] + 'K')
        elif cardValue == 12:
            unicodeCards.append(cardType[card%4] + 'A')
        else:
            print("error!" + str(Cards))
            return []
    
    resultStr = ""
    for unicodeCard in unicodeCards:
        resultStr += (str(unicodeCard) + ' ')
    return resultStr


def decodeSevenCardId(sevenCardId):
    cardIntList = [-1] * 7
    for i in range(7):
        cardIntList[i] = (sevenCardId % 52)
        sevenCardId = sevenCardId // 52
    return cardIntList


def decodeFiveCardId(fiveCardId):
    cardIntList = [-1] * 5
    for i in range(5):
        cardIntList[i] = (fiveCardId % 52)
        fiveCardId = fiveCardId // 52
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
