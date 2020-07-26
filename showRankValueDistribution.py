import seaborn as sns
import matplotlib.pyplot as plt
import time
from collections import Counter
import functools
import random
import pandas as pd
from decimal import Decimal

def compareTwoPoints(p1, p2):
    if p1[0] != p2[0]:
        return p1[0] - p2[0]
    else:
        return p1[1] - p2[1]


def showRankValueDistribution(rankValueDistributionDict, ax, bucketSize, resultProbability):
    y_lim = -1
    yList = []
    xList = []
    roleList = []
    for role, rankValueDistribution in rankValueDistributionDict.items():
        totalCount = 0
        
        # 将rankValue粒度提升便于绘图
        bucketCountDict = dict(zip(range(7462//bucketSize+1), [0]*(7462//bucketSize+1)))
        for rankValue in rankValueDistribution:
            bucketCountDict[rankValue//bucketSize] += rankValueDistribution[rankValue]
            totalCount += rankValueDistribution[rankValue]
        
        # 计算每个非零的桶的概率，化为点后排序
        points = []
        for bucket_index, frequency in bucketCountDict.items():
            points.append([bucket_index, frequency/totalCount])
        points.sort(key=functools.cmp_to_key(compareTwoPoints))

        # 转化为两个list，注意x轴的缩放
        for point in points:
            xList.append(point[0]*bucketSize + (bucketSize-1)//2)
            yList.append(point[1])
            roleList.append(role)

        if max(yList)*1.05 > y_lim:
            y_lim = max(yList) * 1.05



    df = pd.DataFrame(zip(xList, yList, roleList), columns=['CardRank', 'Probability', 'role'])
    sns.lineplot(x="CardRank", y="Probability", hue="role", style='role', estimator=None, data=df, ax=ax, alpha=0.8)
    ax.set(xlim=(0, 7465))
    ax.set(ylim=(0, y_lim))

    if isinstance(resultProbability, dict) and 'win' in resultProbability and 'draw' in resultProbability and 'loss' in resultProbability:
        titleStr = 'Win:' + f'{resultProbability["win"]*100:.1f}' + '% ' + \
            'Draw:' + f'{resultProbability["draw"]*100:.1f}' + '% ' + \
            'Loss:' + f'{resultProbability["loss"]*100:.1f}' + '%'
        ax.set_title(titleStr)
        print(titleStr)

    plt.tight_layout()
    plt.show()
    # print(df)


def showMaxRankProbability(myRankValueProbabilityDist, opponentRankValueProbabilityDist, ax):
    # Note that these Dist has been sorted
    xRankValueList = []
    yProbabilityList = []
    roleList = []

    myRankValueProbabilityDistDict = {}
    for e in myRankValueProbabilityDist:
        myRankValueProbabilityDistDict[e[0]] = e[1]

    opponentRankValueProbabilityDistDict = {}
    for e in opponentRankValueProbabilityDist:
        opponentRankValueProbabilityDistDict[e[0]] = e[1]


    accumulateProbability = 0
    xRankValueList.append(-0.001)
    yProbabilityList.append(0)
    for xRankValue in range(7462):
        xRankValueList.append(xRankValue)
        if xRankValue in myRankValueProbabilityDistDict:
            accumulateProbability += myRankValueProbabilityDistDict[xRankValue]
        yProbabilityList.append(accumulateProbability)
        roleList.append('me')

    accumulateProbability = 0
    xRankValueList.append(-0.001)
    yProbabilityList.append(0)
    for xRankValue in range(7462):
        xRankValueList.append(xRankValue)
        if xRankValue in opponentRankValueProbabilityDistDict:
            accumulateProbability += opponentRankValueProbabilityDistDict[xRankValue]
        yProbabilityList.append(accumulateProbability)
        roleList.append('opponent')

    df = pd.DataFrame(zip(xRankValueList, yProbabilityList, roleList), columns=['CardRank', 'Probability', 'role'])
    sns.lineplot(x="CardRank", y="Probability", hue="role", style='role', estimator=None, data=df, ax=ax, alpha=0.8)

    # 加若干竖线将不同牌型区分开:
        # StraightFlush = 8
        # FourofAKind = 7
        # FullHouse = 6
        # Flush = 5
        # Straight = 4
        # ThreeofAKind = 3
        # TwoPair = 2
        # OnePair = 1
        # NoPair = 0
        # 15064571,1278 ♣5 ♣4 ♣3 ♣2 ♦2  ([15, 11, 7, 3, 2])
        # 15061655,4138 ♣4 ♣3 ♦3 ♣2 ♦2  ([11, 7, 6, 3, 2])
        # 7601319,4996 ♣4 ♣3 ♣2 ♦2 ♥2  ([11, 7, 3, 2, 1])
        # 15638031,5854 ♣6 ♣5 ♣4 ♣3 ♦2  ([19, 15, 11, 7, 2])
        # 22949651,5863 ♣7 ♣5 ♣4 ♣3 ♣2  ([23, 15, 11, 7, 3])
        # 7601263,7141 ♣3 ♦3 ♣2 ♦2 ♥2  ([7, 6, 3, 2, 1])
        # 146179,7297 ♣3 ♣2 ♦2 ♥2 ♠2  ([7, 3, 2, 1, 0])
        # 22949647,7453 ♣6 ♣5 ♣4 ♣3 ♣2  ([19, 15, 11, 7, 3])
    xRankValueList, yProbabilityList, roleList = [], [], []
    xRankValueList.append(1278), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(1278), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(1278.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(4138), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(4138), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(4138.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(4996), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(4996), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(4996.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(5854), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(5854), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(5854.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(5863), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(5863), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(5863.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(7141), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(7141), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(7141.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(7297), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(7297), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(7297.0001), yProbabilityList.append(0), roleList.append('boundary')

    xRankValueList.append(7453), yProbabilityList.append(0), roleList.append('boundary')
    xRankValueList.append(7453), yProbabilityList.append(1), roleList.append('boundary')
    xRankValueList.append(7453.0001), yProbabilityList.append(0), roleList.append('boundary')

    df = pd.DataFrame(zip(xRankValueList, yProbabilityList, roleList), columns=['CardRank', 'Probability', 'role'])
    g = sns.lineplot(x="CardRank", y="Probability", hue="role", style='role', estimator=None, data=df, ax=ax, alpha=0.6, palette="ch:2.5,.25")
    g.legend_.remove()
    
    ax.set(xlim=(0, 7465))
    ax.set(ylim=(0, 1.0))


def getResultProbability(myCountDict, targetCountDict):

    # print('Calculate each rankValue probability')
    myRankValueProbability = []
    targetRankValueProbability = []
    myRankValueSampleSpaceSize = sum(myCountDict.values())
    targetRankValueSampleSpaceSize = sum(targetCountDict.values())
    for rankValue, frequency in myCountDict.items():
        myRankValueProbability.append([rankValue, Decimal(frequency)/Decimal(myRankValueSampleSpaceSize)])
    for rankValue, frequency in targetCountDict.items():
        targetRankValueProbability.append([rankValue, Decimal(frequency)/Decimal(targetRankValueSampleSpaceSize)])
    # print('Calculate each rankValue probability')

    myRankValueProbability.sort(key=lambda x:x[0])
    targetRankValueProbability.sort(key=lambda x:x[0])

    # print(len(myRankValueProbability))
    # print('Calcuate win/draw probability')
    
    # 通过计算累进概率可以进一步优化下面的概率计算，但是数组长度最多6192，就不过度优化了
    winRate = 0
    drawRate = 0
    for myRank in myRankValueProbability:
        for targetRank in targetRankValueProbability:
            if targetRank[0] > myRank[0]:
                break
            elif targetRank[0] == myRank[0]:
                drawRate += targetRank[1]*myRank[1]
            else:
                winRate += targetRank[1]*myRank[1]

    return {'win':float(winRate), 'draw':float(drawRate), 'loss': 1-float(winRate+drawRate)}, myRankValueProbability, targetRankValueProbability
