# -*- coding: utf-8 -*-

import random
import itertools
import functools
import time
import getFiveCardRankListDf as gfcrldf
import patternCompareUtils as pcu
import decodeUtils as du
import seaborn as sns
import matplotlib.pyplot as plt

def selectBestFiveOutOfSeven_bySort(sevenCard, rankDf):
    # 进一步的优化方式是针对所有7张的组合打一张表，可以直接查出maxRankValue
    # 输入是一个长度为7的int list, 我们需要确保其排序为降序 e.g. [50,35,23,21,19,12,3]
    assert sevenCard[0] > sevenCard[1] and sevenCard[1] > sevenCard[2] and sevenCard[2] > sevenCard[3] and sevenCard[3] > sevenCard[4] and sevenCard[4] > sevenCard[5] and sevenCard[5] > sevenCard[6], "The input sevenCard list should be sorted in desending way" + str(sevenCard)

    fiveCards = []
    for fiveCard in itertools.combinations(sevenCard, 5):
        fiveCards.append(list(fiveCard))
    
    fiveCards.sort(key=functools.cmp_to_key(pcu.compareTwoSuits))
    
    maxFiveCardId = gfcrldf.fiveCardsToID(fiveCards[-1])
    return maxFiveCardId, rankDf.loc[maxFiveCardId]['rankValue']


def selectBestFiveOutOfSeven_byLookingUp(sevenCard, rankDict):
    # 输入是一个长度为7的int list, 我们需要确保其排序为降序 e.g. [50,35,23,21,19,12,3]
    # 考虑仅将这个函数用于快速生成7张的战力列表
    assert sevenCard[0] > sevenCard[1] and sevenCard[1] > sevenCard[2] and sevenCard[2] > sevenCard[3] and sevenCard[3] > sevenCard[4] and sevenCard[4] > sevenCard[5] and sevenCard[5] > sevenCard[6], "The input sevenCard list should be sorted in desending way" + str(sevenCard)

    maxRankValue = -1
    for fiveCard in itertools.combinations(sevenCard, 5):
        fiveCardId = gfcrldf.fiveCardsToID(list(fiveCard))
        rankValue = rankDict[fiveCardId]
        if maxRankValue < rankValue:
            maxRankValue = rankValue
    
    return maxRankValue



def getRankValueDistribution(cardsForSelection, bannedCards, rankDf):
    # 输入的为两个list和一个df
    allCardsSet = set(list(range(52))) # 可以考虑转为全局变量
    rankValueDistribution = []
    
    # 求restOfCardToSelect，有至少两种方法
    restOfCardToSelect = list(allCardsSet - set(cardsForSelection) - set(bannedCards))
    sevenCards = []
    for restOfCardToSelect in itertools.combinations(restOfCardToSelect, 7-len(cardsForSelection)):
        # print(cardsForSelection)
        sevenCard = list(restOfCardToSelect) + cardsForSelection
        sevenCard.sort(reverse=True)
        sevenCards.append(sevenCard)

    print(len(sevenCards))
    if len(sevenCards) > 10000:
        sampledSevenCards = random.sample(sevenCards, k=10000)
        for sevenCard in sampledSevenCards:
            _, maxCardValue = selectBestFiveOutOfSeven_bySort(sevenCard, rankDf)
            rankValueDistribution.append(maxCardValue)
    else:
        selectBestFiveOutOfSeven_bySort(sevenCard,rankDf)
        for sevenCard in sevenCards:
            _, maxCardValue = selectBestFiveOutOfSeven_bySort(sevenCard, rankDf)
            rankValueDistribution.append(maxCardValue)
    return rankValueDistribution


def printRankValueDistribution(rankValueDistribution, role, enableKde = True, ax = None, showPlot=True):

    if role == 'opponent':
        sns.distplot(rankValueDistribution, bins=200, color='r', kde=enableKde)
        plt.xlim([-1, 6170])
    elif role == 'me':
        sns.distplot(rankValueDistribution, bins=200, color='b', kde=enableKde)
        plt.xlim([-1, 6170])
    elif role == 'baseline':
        sns.distplot(rankValueDistribution, bins=200, color='g', kde=enableKde)
        plt.xlim([-1, 6170])

    if showPlot is True:
        plt.show()


if __name__ == "__main__":
    fiveCardsDf = gfcrldf.getFiveCardRankListDf()
    # print(fiveCardsDf.head())
    # print(fiveCardsDf.loc[350530283])
    # testSevenCards = []
    # for i in range(1000):
    #     testSevenCard = random.sample(range(52), k=7)
    #     testSevenCard.sort(reverse=True)
    #     testSevenCards.append(testSevenCard)

    # start = time.time()
    # test_bySort = []
    # for testSevenCard in testSevenCards:
    #     test_bySort.append(selectBestFiveOutOfSeven_bySort(testSevenCard, df))
    # end = time.time()
    # print(end-start)

    # test_byLookingUpList = []
    # for testSevenCard in testSevenCards:
    #     test_byLookingUpList.append(selectBestFiveOutOfSeven_byLookingUpList(testSevenCard, df))
    # end = time.time()
    # print(end-start)

    # for suit in test:
    #     printSuit(suit)
    # cardsForSelectionTest = ["SA", "H3", "DQ", "D2", "D9"]
    cardsForSelectionTest = ["H3", "SK", "D2", "D9", "CJ"]
    bannedCards = []
    rankValueDistribution = getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelectionTest), bannedCards, fiveCardsDf)
    printRankValueDistribution(rankValueDistribution)