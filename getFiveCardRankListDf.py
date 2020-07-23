import os
import itertools
import collections
import logging
import functools
import time
import patternCompareUtils as pcu
import pandas as pd


def generateAllDeckCards():
    deckCards = []
    for deckCard in itertools.combinations(range(51,-1,-1), 5):
        deckCards.append(list(deckCard))
    print(len(deckCards))
    # TODO: Make sure the combinations algorithm makes sure 5 elements in a deckCard list is sorted descending way
    return deckCards

def fiveCardsToID(fiveCard):
    return fiveCard[0] + fiveCard[1]*52 + fiveCard[2]*(52**2) + fiveCard[3]*(52**3) + fiveCard[4]*(52**4)

def getFiveCardRankListDf():
    if os.path.exists('fiveCardRankList.csv'):
        print("Reading from fiveCardRankList.csv ...")
        df = pd.read_csv('fiveCardRankList.csv')
        df.set_index('id', inplace=True)
        return df
    else:
        print("fiveCardRankList.csv not found, generating new rank list...")
        deckCards = generateAllDeckCards()
        deckCards.sort(key=functools.cmp_to_key(pcu.compareTwoSuits))
        df = pd.DataFrame(deckCards, columns =['fiveCards_0','fiveCards_1','fiveCards_2','fiveCards_3','fiveCards_4'])

        idList = []
        for fiveCard in deckCards:
            idList.append(fiveCardsToID(fiveCard))
        df['id'] = idList
        df.set_index('id', inplace=True)

        rankValue = 0
        rankValueList = [0]
        for index in range(1, len(deckCards)):
            compareResult = pcu.compareTwoSuits(deckCards[index-1], deckCards[index])
            if compareResult < 0:
                rankValue += 1
            elif compareResult > 0:
                logging.critical('Unexpected sequence!', index, deckCards[index-1], deckCards[index])
                exit()
            rankValueList.append(rankValue)
        df['rankValue'] = rankValueList

        # 也许以下的weekerNumberList， strongerNumberList用不上
        weekerNumberList = []
        strongerNumberList = []
        totalNumber = len(deckCards)
        weekerNumberCount = 0
        weekerNumberCountIndex = 0
        strongerNumberCount = 0
        strongerNumberCountIndex = 0
        for index in range(len(rankValueList)):
            currentFiveCardRankValue = rankValueList[index]
            while strongerNumberCountIndex < totalNumber and rankValueList[strongerNumberCountIndex] < currentFiveCardRankValue:
                strongerNumberCountIndex += 1
            while weekerNumberCountIndex < totalNumber and rankValueList[weekerNumberCountIndex] <= currentFiveCardRankValue:
                weekerNumberCountIndex += 1
            weekerNumberList.append(totalNumber-weekerNumberCountIndex)
            strongerNumberList.append(strongerNumberCountIndex)
        df['weekerNumber'] = weekerNumberList
        df['strongerNumber'] = strongerNumberList
        
        idList = []
        for fiveCard in deckCards:
            idList.append(fiveCardsToID(fiveCard))
        df.set_index('id', inplace=True)

        df.to_csv('fiveCardRankList.csv')
        return df
