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
        bucketCountDict = dict(zip(range(6191//bucketSize+1), [0]*(6191//bucketSize+1)))
        for rankValue in rankValueDistribution:
            bucketCountDict[rankValue//52] += rankValueDistribution[rankValue]
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

    df = pd.DataFrame(zip(xList, yList, roleList), columns=['x', 'y', 'role'])
    sns.lineplot(x="x", y="y", hue="role", style='role', estimator=None, data=df, ax=ax, alpha=0.8)
    ax.set(xlim=(0, 6200))
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
    for xRankValue in range(6191):
        xRankValueList.append(xRankValue)
        if xRankValue in myRankValueProbabilityDistDict:
            accumulateProbability += myRankValueProbabilityDistDict[xRankValue]
        yProbabilityList.append(accumulateProbability)
        roleList.append('me')

    accumulateProbability = 0
    xRankValueList.append(-0.001)
    yProbabilityList.append(0)
    for xRankValue in range(6191):
        xRankValueList.append(xRankValue)
        if xRankValue in opponentRankValueProbabilityDistDict:
            accumulateProbability += opponentRankValueProbabilityDistDict[xRankValue]
        yProbabilityList.append(accumulateProbability)
        roleList.append('opponent')

    df = pd.DataFrame(zip(xRankValueList, yProbabilityList, roleList), columns=['x', 'y', 'role'])
    df.to_csv('debug.csv')
    sns.lineplot(x="x", y="y", hue="role", style='role', estimator=None, data=df, ax=ax, alpha=0.8)
    ax.set(xlim=(0, 6200))
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

# _, ax = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
# #d={'baseline':random.choices(range(3000, 3500),k=5000)}
# d={'me':rankValueDistribution, 'baseline':random.choices(range(3000, 3500),k=5000), 'opponent':random.choices(range(2000, 3500),k=5000)}

# drawRankValueDistribution(d, ax)