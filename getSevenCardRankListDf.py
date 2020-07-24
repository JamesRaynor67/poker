# -*- coding: utf-8 -*-

import os
import itertools
import collections
import logging
import functools
import time
import patternCompareUtils as pcu
import getRankValueDistribution as grvd
import getFiveCardRankListDf as gfcrldf
import pandas as pd
from collections import Counter


def sevenCardsToID(sevenCard):
    return sevenCard[0] + sevenCard[1]*52 + sevenCard[2]*(52**2) + sevenCard[3]*(52**3) + sevenCard[4]*(52**4) + sevenCard[5]*(52**5) + sevenCard[6]*(52**6)


def getSevenCardRankListDf(fiveCardRankListDf):
    if os.path.exists('sevenCardRankList.zip'):
        print("Reading from sevenCardRankList.zip ...")
        df = pd.read_csv('sevenCardRankList.zip', compression='zip', sep=',')
        df.set_index('id', inplace=True)
        return df
    else:
        print("File sevenCardRankList.csv not found, generating new rank list...This may take a LONG time")
        fiveCardRankDict = fiveCardRankListDf.to_dict()['rankValue']
        sevenCardIdList = []
        sevenCardRankList = []
        count = 0
        start = time.time()
        for sevenCard in itertools.combinations(range(51,-1,-1), 7):
            count += 1
            if count % 100000 == 0:
                print("progress: " + str(count/133784560))
            sevenCardIdList.append(sevenCardsToID(sevenCard))
            rankValue = grvd.selectBestFiveOutOfSeven_byLookingUp(sevenCard, fiveCardRankDict)
            # _, rankValue = grvd.selectBestFiveOutOfSeven_bySort(sevenCard, fiveCardRankListDf)
            sevenCardRankList.append(rankValue)
        end = time.time()
        print(end-start)

        df = pd.DataFrame()
        df['id'] = sevenCardIdList
        sevenCardIdList = None # High memory is required ahead, make it availble to free memory
        df['rankValue'] = sevenCardRankList
        sevenCardRankList = None # High memory is required ahead, make it availble to free memory
        df.set_index('id', inplace=True)

        print('Saving file as zip, it may take sometime')
        df.to_csv('sevenCardRankList.zip', compression="zip")
        return df


def getBaselineBucketCountDict(sevenCardRankListDf, bucketSize):
    sevenCardRankValueDistribution = sevenCardRankListDf['rankValue'].tolist()
    print('正在处理随机抽牌背景概率...')
    bucket = [rankValue//bucketSize for rankValue in sevenCardRankValueDistribution]
    bucketCountDict = dict(Counter(bucket))
    print('随机抽牌背景概率处理完成')
    return bucketCountDict
    

if __name__ == '__main__':
    fiveCardRankListDf = gfcrldf.getFiveCardRankListDf()
    sevenCardRankListDf = getSevenCardRankListDf(fiveCardRankListDf)
    sevenCardRankListDf.head()
