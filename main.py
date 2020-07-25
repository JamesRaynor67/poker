# -*- coding: utf-8 -*-

import getFiveCardRankListDf as gfcrldf
import getSevenCardRankListDf as gscrldf
import getRankValueDistribution as grvd
import showRankValueDistribution as srvd
from collections import Counter
import precomputeRankValueDistributionCount as prvdc
import decodeUtils as du
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import time

def inputACard(promptStr, inputedCards):
    isValid = False
    while isValid is False:
        print("正确的牌由花色和大小组成，花色: `H(红桃), S(黑桃), 'D'(方块), 'C'(梅花)`, 大小：`2,3,4,5,6,7,8,9,10,J,Q,K,A`。例：H2, S10, DJ, CA")
        oneCard = input(promptStr + "请输入: ")

        # 确认card输入无误
        if len(oneCard) < 2:
            print('输入的牌`' + oneCard +  '`不正确！')
            continue

        if oneCard[0] not in ['H', 'S', 'D', 'C'] or oneCard[1:] not in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']:
            print('输入的牌`' + oneCard +  '`不正确！')
            continue

        if oneCard in inputedCards:
            print('你输入' + oneCard + '之前已经输入过，两张牌不应该一样。请重新输入。')
            continue
        else:
            isValid = True
            inputedCards.append(oneCard)


def printInputedCard(inputedCards):
    if len(inputedCards) == 2:
        print('你输入的底牌为:', inputedCards, '(', du.printUnicodeCards(du.readableCardsToCardsInt(inputedCards)), ')')
    elif len(inputedCards) > 2:
        print('你输入的底牌为:', inputedCards[:2], '(', du.printUnicodeCards(du.readableCardsToCardsInt(inputedCards[:2])), ')', ' 桌上的公开牌为：', inputedCards[2:], '(', du.printUnicodeCards(du.readableCardsToCardsInt(inputedCards[2:])), ')')



if __name__ == "__main__":
    bucketSize = 51
    twoCardsDf = prvdc.getTwoCardRankValueDistributionCountDf()
    fiveCardsDf = gfcrldf.getFiveCardRankListDf()
    fiveCardRankDict = fiveCardsDf.to_dict()['rankValue']


    end = False
    while end is False:
        _, axes = plt.subplots(2, 4, figsize=(21, 7), sharex=True)
        plt.ion()
        sns.set(font_scale=0.8)

        resultProbability = None
        cardsForSelection = []

        # 第一阶段
        print("\n输入两张你的底牌")
        inputACard("输入第1张底牌。", cardsForSelection)
        inputACard("输入第2张底牌。", cardsForSelection)

            # 第一阶段可能性不多但是每个可能性计算非常耗时，此时查表处理
        myRankValueDistributionDict, opponentRankValueDistributionDict = prvdc.getTwoCardRankValueDistributionCountDict(twoCardsDf, cardsForSelection)
        baselineRankValueDistributionDict = prvdc.getBaselineRankValueDistributionCountDf().to_dict()['baselineRankValueCount']
        rankValueDistributionDict = {'me':myRankValueDistributionDict, 'opponent':opponentRankValueDistributionDict, 'baseline': baselineRankValueDistributionDict}

        printInputedCard(cardsForSelection)
        resultProbability, myRankValueProbabilityDist, opponentRankValueProbabilityDist = srvd.getResultProbability(myRankValueDistributionDict, opponentRankValueDistributionDict)
        print(resultProbability)
        srvd.showRankValueDistribution(rankValueDistributionDict, axes[0,0], bucketSize, resultProbability)
        srvd.showMaxRankProbability(myRankValueProbabilityDist, opponentRankValueProbabilityDist, axes[1,0])

        # 第二阶段
        print("\n接下来输入五张公开牌中的前三张")
        inputACard("首先输入第1张公开牌。", cardsForSelection)
        inputACard("首先输入第2张公开牌。", cardsForSelection)
        inputACard("首先输入第3张公开牌。", cardsForSelection)

        myRankValueDistributionDict = Counter(grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf, fiveCardRankDict))
        opponentRankValueDistributionDict = Counter(grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection[2:]), du.readableCardsToCardsInt(cardsForSelection[0:2]), fiveCardsDf, fiveCardRankDict))
        rankValueDistributionDict = {'me':myRankValueDistributionDict, 'opponent':opponentRankValueDistributionDict}

        printInputedCard(cardsForSelection)
        resultProbability, myRankValueProbabilityDist, opponentRankValueProbabilityDist = srvd.getResultProbability(myRankValueDistributionDict, opponentRankValueDistributionDict)
        print(resultProbability)
        srvd.showRankValueDistribution(rankValueDistributionDict, axes[0,1], bucketSize, resultProbability)
        srvd.showMaxRankProbability(myRankValueProbabilityDist, opponentRankValueProbabilityDist, axes[1,1])

        # 第三阶段
        print("\n接下来输入五张公开牌中的第四张")
        inputACard("输入第4张公开牌。", cardsForSelection)
        
        myRankValueDistributionDict = Counter(grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf, fiveCardRankDict))
        opponentRankValueDistributionDict = Counter(grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection[2:]), du.readableCardsToCardsInt(cardsForSelection[0:2]), fiveCardsDf, fiveCardRankDict))
        rankValueDistributionDict = {'me':myRankValueDistributionDict, 'opponent':opponentRankValueDistributionDict}

        printInputedCard(cardsForSelection)
        resultProbability, myRankValueProbabilityDist, opponentRankValueProbabilityDist = srvd.getResultProbability(myRankValueDistributionDict, opponentRankValueDistributionDict)
        print(resultProbability)
        srvd.showRankValueDistribution(rankValueDistributionDict, axes[0,2], bucketSize, resultProbability)
        srvd.showMaxRankProbability(myRankValueProbabilityDist, opponentRankValueProbabilityDist, axes[1,2])


        # 第四阶段
        print("\n最后输入五张公开牌中的第五张")
        inputACard("输入第5张公开牌。", cardsForSelection)

        myRankValueDistributionDict = Counter(grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf, fiveCardRankDict))
        opponentRankValueDistributionDict = Counter(grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection[2:]), du.readableCardsToCardsInt(cardsForSelection[0:2]), fiveCardsDf, fiveCardRankDict))
        rankValueDistributionDict = {'me':myRankValueDistributionDict, 'opponent':opponentRankValueDistributionDict}

        printInputedCard(cardsForSelection)
        resultProbability, myRankValueProbabilityDist, opponentRankValueProbabilityDist = srvd.getResultProbability(myRankValueDistributionDict, opponentRankValueDistributionDict)
        print(resultProbability)
        srvd.showRankValueDistribution(rankValueDistributionDict, axes[0,3], bucketSize, resultProbability)
        srvd.showMaxRankProbability(myRankValueProbabilityDist, opponentRankValueProbabilityDist, axes[1,3])


        validInput = False
        while validInput is False:
            cmd = input("输入小写字母e后回车结束程序, 输入n后回车开始下一局, 请输入: ")
            if cmd == 'e':
                end = True
                validInput = True
            elif cmd == 'n':
                validInput = True
                plt.close()
            else:
                print('你输入的为`' + cmd + '`, 不是小写字母e或n, 请重新输入!')
