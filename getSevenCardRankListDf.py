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


def sevenCardsToID(sevenCard):
    return sevenCard[0] + sevenCard[1]*52 + sevenCard[2]*(52**2) + sevenCard[3]*(52**3) + sevenCard[4]*(52**4) + sevenCard[5]*(52**5) + sevenCard[6]*(52**6)

def getSevenCardRankListDf(fiveCardRankListDf):
    if os.path.exists('sevenCardRankList.csv'):
        print("Reading from sevenCardRankList.csv ...")
        df = pd.read_csv('sevenCardRankList.csv')
        df = df.set_index('id')
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
        df = pd.DataFrame(zip(sevenCardIdList, sevenCardRankList), columns =['id','rankValue'])
        df = df.set_index('id')
        df.to_csv('sevenCardRankList.csv')
        return df

if __name__ == '__main__':
    fiveCardRankListDf = gfcrldf.getFiveCardRankListDf()
    sevenCardRankListDf = getSevenCardRankListDf(fiveCardRankListDf)
    sevenCardRankListDf.head()
