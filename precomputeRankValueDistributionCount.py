# -*- coding: utf-8 -*-

import getFiveCardRankListDf as gfcrldf
import getSevenCardRankListDf as gscrldf
import getRankValueDistribution as grvd
import showRankValueDistribution as srvd
import decodeUtils as du
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import time
import itertools
from collections import Counter
import pandas as pd
import gc
import os

def getTwoCardRankValueDistributionCountDf():
    # 因为仅仅两张牌，且德州扑克不考虑花色，为减少重复计算故仅仅
    # 在这个函数及生成的csv文件中考虑牌的值为 0,1...12,对应
    # cardInt为0,1..51
    if os.path.exists('twoCardRankValueDistribution.zip'):
        print("Reading from twoCardRankValueDistribution.zip ...")
        df = pd.read_csv('twoCardRankValueDistribution.zip', compression='zip', sep=',')
        df.set_index('rankValue', inplace=True)
    else:
        print('twoCardRankValueDistribution.zip not found, start generating and it may take a long time and a lot of memory')
        fiveCardsDf = gfcrldf.getFiveCardRankListDf()
        sevenCardsDf = gscrldf.getSevenCardRankListDf(fiveCardsDf)
        sevenCardsRankDict = sevenCardsDf.to_dict()['rankValue']
        
        # Seems doesn't work, don't know why
        fiveCardsDf, sevenCardsDf = None, None
        del fiveCardsDf
        del sevenCardsDf
        gc.collect()

        twoCards = []
        for twoCard in itertools.combinations_with_replacement(range(12,-1,-1), 2):
            twoCards.append(list(twoCard))
        print(len(twoCards))

        rankValueList = list(range(6192))
        df = pd.DataFrame(rankValueList, columns=['rankValue'])

        for twoCard in twoCards:
            includeTwoCardRankValueDistribution = []
            excludeTwoCardRankValueDistribution = []
            includeTwoCardId = 'include_' + str(twoCard[0] + twoCard[1]*13)
            excludeTwoCardId = 'exclude_' + str(twoCard[0] + twoCard[1]*13)

            includeRankValueCountDict = dict(zip(range(6192),[0]*6192))
            excludeRankValueCountDict = dict(zip(range(6192),[0]*6192))

            print(twoCard)
            for sevenCardId in sevenCardsRankDict:
                rankValue = sevenCardsRankDict[sevenCardId]
                sevenCardValueList = []
                for i in range(7):
                    sevenCardValueList.append(sevenCardId % 52)
                    sevenCardId = sevenCardId // 52
                if twoCard[0] in sevenCardValueList and twoCard[1] in sevenCardValueList:
                    includeRankValueCountDict[rankValue] += 1 # rankValue 必然已经在此Dict中，故不检查
                else:
                    excludeRankValueCountDict[rankValue] += 1
        
            for rankValue in rankValueList:
                includeTwoCardRankValueDistribution.append(includeRankValueCountDict[rankValue])
                excludeTwoCardRankValueDistribution.append(excludeRankValueCountDict[rankValue])

            df[includeTwoCardId] = includeTwoCardRankValueDistribution
            df[excludeTwoCardId] = excludeTwoCardRankValueDistribution

        df.set_index('rankValue', inplace=True)
        df.to_csv('twoCardRankValueDistribution.zip', compression="zip")
    return df


def getBaselineRankValueDistributionCountDf():
    if os.path.exists('baselineRankValueDistribution.csv'):
        # print("Reading from baselineRankValueDistribution.csv ...")
        df = pd.read_csv('baselineRankValueDistribution.csv')
        df.set_index('rankValue', inplace=True)
    else:
        print('baselineRankValueDistribution.csv not found, start generating and it may take a long time and a lot of memory')
        fiveCardsDf = gfcrldf.getFiveCardRankListDf()
        sevenCardsDf = gscrldf.getSevenCardRankListDf(fiveCardsDf)
        sevenCardsRankList = sevenCardsDf['rankValue'].tolist()
        sevenCardsRankCount = Counter(sevenCardsRankList)

        rankValueList = list(range(6192))
        df = pd.DataFrame(rankValueList, columns=['rankValue'])

        sevenCardRankValueDistribution = []
        for rankValue in rankValueList:
            if rankValue in sevenCardsRankCount:
                sevenCardRankValueDistribution.append(sevenCardsRankCount[rankValue])
            else:
                sevenCardRankValueDistribution.append(0)
        
        df['baselineRankValueCount'] = sevenCardRankValueDistribution
        df.set_index('rankValue', inplace=True)
        df.to_csv('baselineRankValueDistribution.csv')
    return df


def getTwoCardRankValueDistributionCountDict(twoCardDf, twoCard):
    twoCardInt = du.readableCardsToCardsInt(twoCard)
    twoCardInt.sort(reverse=True)
    cardId = (twoCardInt[0]//13) + (twoCardInt[1]//13)*13
    return twoCardDf.to_dict()['include_' + str(cardId)], twoCardDf.to_dict()['exclude_' + str(cardId)]


if __name__ == '__main__':
    print('start')
    print(getTwoCardRankValueDistributionCountDf())
    print(getBaselineRankValueDistributionCountDf())