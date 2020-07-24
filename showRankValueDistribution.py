import seaborn as sns
import matplotlib.pyplot as plt
import time
from collections import Counter
import functools
import random
import pandas as pd

def compareTwoPoints(p1, p2):
    if p1[0] != p2[0]:
        return p1[0] - p2[0]
    else:
        return p1[1] - p2[1]


def showRankValueDistribution(rankValueDistributionDict, ax, bucketSize, baselineBucketCountDict):
    # bucketSize = 51 # Should be a factor of 6191+1
    colorDict = {'opponent':'r', 'me':'b', 'baseline':'g'}
    eps = 0.005
    y_lim = -1
    yList = []
    xList = []
    roleList = []
    for role, rankValueDistribution in rankValueDistributionDict.items():
        color = colorDict[role]
        if role != 'baseline':
            bucket = [rankValue//bucketSize for rankValue in rankValueDistribution]
            bucketCountDict = dict(Counter(bucket))
        else:
            bucket = None
            bucketCountDict = baselineBucketCountDict
        points = []
        
        # 计算每个非零的桶的概率，化为点后排序
        totalCount = len(rankValueDistribution)
        for bucket_index, frequency in bucketCountDict.items():
            points.append([bucket_index, frequency/totalCount])
        points.sort(key=functools.cmp_to_key(compareTwoPoints))

        
        extraPointsForPlot = []
        for point in points:
            # 遇到非零点，若左/右两边的bucket的值不存在(即为0)，则左/右插入一个0
            if point[1] != 0:
                leftPointX = point[0]-1
                if leftPointX not in bucketCountDict:
                    extraPointsForPlot.append([point[0]-eps, 0])
                rightPointX = point[0]+1
                if rightPointX not in bucketCountDict:
                    extraPointsForPlot.append([point[0]+eps, 0])

        # print(points)
        # print(bucketCountDict)
        points = points + extraPointsForPlot
        points.sort(key=functools.cmp_to_key(compareTwoPoints))

        # 转化为两个list，注意x轴的缩放
        for point in points:
            xList.append(point[0]*bucketSize + (bucketSize-1)//2)
            yList.append(point[1])
            roleList.append(role)

        if max(yList)*1.05 > y_lim:
            y_lim = max(yList) * 1.05

    df = pd.DataFrame(zip(xList, yList, roleList), columns=['x', 'y', 'role'])
    # ax.set_xlim([0, 6200])
    # ax.set_xlim([0, y_lim])
    sns.lineplot(x="x", y="y", hue="role", estimator=None, data=df, ax=ax)
    ax.set(xlim=(0, 6200))
    ax.set(ylim=(0, y_lim))
    plt.tight_layout()
    plt.show()
    # print(df)




# _, ax = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
# #d={'baseline':random.choices(range(3000, 3500),k=5000)}
# d={'me':rankValueDistribution, 'baseline':random.choices(range(3000, 3500),k=5000), 'opponent':random.choices(range(2000, 3500),k=5000)}

# drawRankValueDistribution(d, ax)