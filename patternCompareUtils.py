# -*- coding: utf-8 -*-

import itertools
import collections
import logging
import functools

def isFlush(countItems, suit):
    # 默认五张牌是从大到小已经排序的
    # 如果同时使顺子，不可能仅仅是同花（否则成为同花顺）
    if suit[4]//4 + 1 == suit[3]//4 and suit[3]//4 + 1 == suit[2]//4 and suit[2]//4 + 1 == suit[1]//4 and suit[1]//4 + 1 == suit[0]//4:
        return False, suit
    
    fullHouse, _, _ = isFullHouse(countItems)
    if fullHouse is True:
        return False, suit
    
    fourOfAKind, _, _ = isFourofAKind(countItems)
    if fourOfAKind is True:
        return False, suit
    
    return suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4, suit


def isStraight(suit):
    # 默认五张牌是从大到小已经排序的
    if suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4:
        return False, None
    
    if suit[4]//4 + 1 == suit[3]//4 and suit[3]//4 + 1 == suit[2]//4 and suit[2]//4 + 1 == suit[1]//4 and suit[1]//4 + 1 == suit[0]//4:
        return True, suit[0]
    else:
        return False, None


def isStraightFlush(suit):
    # 默认五张牌是从大到小已经排序的
    if suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4:
        if suit[4]//4 + 1 == suit[3]//4 and suit[3]//4 + 1 == suit[2]//4 and suit[2]//4 + 1 == suit[1]//4 and suit[1]//4 + 1 == suit[0]//4:
            return True, suit[0]
    return False, None


def isFourofAKind(countItems):
    # count = collections.Counter(card//4 for card in suit).items()
    # 注意返回的cardValue范围已经变为0,1,2...13了
    fourKindCardValue = None
    singleCardValue = None
    
    for cardValue, count in countItems:
        if count == 4:
            fourKindCardValue = cardValue
        elif count == 1:
            singleCardValue = cardValue
    
    if fourKindCardValue is None:
        return False, None, None
    else:
        return True, fourKindCardValue, singleCardValue


def isFullHouse(countItems):
    # count = collections.Counter(card//4 for card in suit).items()
    # 注意返回的cardValue范围已经变为0,1,2...13了
    threeCardValue = None
    twoCardValue = None

    for cardValue, count in countItems:
        if count == 3:
            threeCardValue = cardValue
        elif count == 2:
            twoCardValue = cardValue
        else:
            return False, None, None
    
    # Must be fullhouse if runs to here
    return True, threeCardValue, twoCardValue
        
            
def isThreeofAkind(countItems, suit):
    # count = collections.Counter(card//4 for card in suit).items()
    # 注意返回的cardValue范围已经变为0,1,2...13了

    if suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4:
        return False, None, None
    
    threeCardValue = None
    twoCardsValueList = []
    
    for cardValue, count in countItems:
        if count == 3:
            threeCardValue = cardValue
        elif count == 1:
            twoCardsValueList.append(cardValue)
        else:
            return False, None, None
    
    # 这个if不能去掉，5个单牌也可以运行到此处
    if threeCardValue is not None and len(twoCardsValueList) == 2:
        maxValue = max(twoCardsValueList)
        minValue = min(twoCardsValueList)
        return True, threeCardValue, [maxValue, minValue]
    else:
        return False, None, None
    

def isTwoPair(countItems, suit):
    # count = collections.Counter(card//4 for card in suit).items()
    # 注意返回的cardValue范围已经变为0,1,2...13了

    if suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4:
        return False, None, None, None
    
    maxPairCardValue = None
    minPairCardValue = None
    singleCardValue = None
    
    for cardValue, count in countItems:
        if count == 2:
            if maxPairCardValue is None:
                maxPairCardValue = cardValue
            else:
                if cardValue > maxPairCardValue:
                    minPairCardValue = maxPairCardValue
                    maxPairCardValue = cardValue
                else:
                    minPairCardValue = cardValue
        if count == 1:
            singleCardValue = cardValue
    
    if maxPairCardValue is not None and minPairCardValue is not None and  singleCardValue is not None:
        return True, maxPairCardValue, minPairCardValue, singleCardValue
    else:
        return False, None, None, None
    

def isOnePair(countItems, suit):
    # count = collections.Counter(card//4 for card in suit).items()
    # 注意返回的cardValue范围已经变为0,1,2...13了
    
    if suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4:
        return False, None, None
    
    pairValue = None
    singleCardList = []
    
    for cardValue, count in countItems:
        if count == 2:
            if pairValue is None:
                pairValue = cardValue
            else:
                return False, None, None
        elif count == 1:
            singleCardList.append(cardValue)
        else:
            return False, None, None
        
    # 这个if不能去掉，5个单牌也可以运行到此处
    if pairValue is not None and len(singleCardList) == 3:
        singleCardList.sort(reverse=True)
        # 单排从大到小排列
        return True, pairValue, singleCardList
    else:
        return False, None, None
    

def isNoPair(countItems, suit):
    # count = collections.Counter(card//4 for card in suit).items()
    # 注意返回的cardValue范围已经变为0,1,2...13了
    
    # 不是同花
    if suit[0]%4 == suit[1]%4 and suit[1]%4 == suit[2]%4 and suit[2]%4 == suit[3]%4 and suit[3]%4 == suit[4]%4:
        return False, None
    # 不是顺子
    if suit[4]//4 + 1 == suit[3]//4 and suit[3]//4 + 1 == suit[2]//4 and suit[2]//4 + 1 == suit[1]//4 and suit[1]//4 + 1 == suit[0]//4:
        return False, None
    
    singleCardList = []
    
    for cardValue, count in countItems:
        if count == 1:
            singleCardList.append(cardValue)
        else:
            return False, None
    
    singleCardList.sort(reverse=True)
    return True, singleCardList    


def compareTwoSuits(suit1, suit2):
    # 这里的一个Suit指的是5张牌
    # 牌型大小可以参看：https://github.com/laixintao/HoldemCalculator
    # StraightFlush = 8
    # FourofAKind = 7
    # FullHouse = 6
    # Flush = 5
    # Straight = 4
    # ThreeofAKind = 3
    # TwoPair = 2
    # OnePair = 1
    # NoPair = 0
    # 从出现概率高的牌型开始查
    # if suit1 < suit2, return -1 or negative number
    # if suit1 == suit2, return 0
    # if suit1 > suit2, return 1 or positive number
    
    countItems1 = collections.Counter(card//4 for card in suit1).items()
    countItems2 = collections.Counter(card//4 for card in suit2).items()
    
    noPair1, singleCardList1 = isNoPair(countItems1, suit1)
    noPair2, singleCardList2 = isNoPair(countItems2, suit2)
    if noPair1 is True and noPair2 is False:
        return -1
    elif noPair1 is False and noPair2 is True:
        return 1
    elif noPair1 is True and noPair2 is True: # 两个都为noPair，依次比较单牌大小
        for i in range(5):
            if singleCardList1[i] != singleCardList2[i]:
                return singleCardList1[i] - singleCardList2[i]
        return 0
    
    
    onePair1, pairValue1, singleCardList1 = isOnePair(countItems1, suit1)
    onePair2, pairValue2, singleCardList2 = isOnePair(countItems2, suit2)
    if onePair1 is True and onePair2 is False:
        return -1
    elif onePair1 is False and onePair2 is True:
        return 1
    elif onePair1 is True and onePair2 is True: # 两个都为onePair，比较对子后比较单牌大小
        if pairValue1 != pairValue2:
            return pairValue1 - pairValue2
        else:
            for i in range(3):
                if singleCardList1[i] != singleCardList2[i]:
                    return singleCardList1[i] - singleCardList2[i]
            return 0
    
    
    twoPair1, maxPairCardValue1, minPairCardValue1, singleCardValue1 = isTwoPair(countItems1, suit1)
    twoPair2, maxPairCardValue2, minPairCardValue2, singleCardValue2 = isTwoPair(countItems2, suit2)
    if twoPair1 is True and twoPair2 is False:
        return -1
    elif twoPair1 is False and twoPair2 is True:
        return 1
    elif twoPair1 is True and twoPair2 is True: #两个都为twoPair，比较对子的大小后比较单牌大小
        if maxPairCardValue1 != maxPairCardValue2:
            return maxPairCardValue1 - maxPairCardValue2
        elif minPairCardValue1 != minPairCardValue2:
            return minPairCardValue1 - minPairCardValue2
        elif singleCardValue1 != singleCardValue2:
            return singleCardValue1 - singleCardValue2
        else:
            return 0

        
    threeOfAKind1, threeCardValue1, singleCardList1 = isThreeofAkind(countItems1, suit1)
    threeOfAKind2, threeCardValue2, singleCardList2 = isThreeofAkind(countItems2, suit2)
    if threeOfAKind1 is True and threeOfAKind2 is False:
        return -1
    elif threeOfAKind1 is False and threeOfAKind2 is True:
        return 1
    elif threeOfAKind1 is True and threeOfAKind2 is True: # 比较三张后比较两个单牌的大小
        if threeCardValue1 != threeCardValue2:
            return threeCardValue1 - threeCardValue2
        else:
            for i in range(2):
                if singleCardList1[i] != singleCardList2[i]:
                    return singleCardList1[i] - singleCardList2[i]
            return 0

        
    straight1, maxCardInt1 = isStraight(suit1)
    straight2, maxCardInt2 = isStraight(suit2)
    if straight1 is True and straight2 is False:
        return -1
    elif straight1 is False and straight2 is True:
        return 1
    elif straight1 is True and straight2 is True:
        return maxCardInt1//4 - maxCardInt2//4 #不应受到花色影响，故除以4后比较

    
    flush1, singleCardIntList1 = isFlush(countItems1, suit1)
    flush2, singleCardIntList2 = isFlush(countItems2, suit2)
    if flush1 is True and flush2 is False:
        return -1
    elif flush1 is False and flush2 is True:
        return 1
    elif flush1 is True and flush2 is True:
        for i in range(5):
            if singleCardIntList1[i] != singleCardIntList2[i]:
                return singleCardIntList1[i]//4 - singleCardIntList2[i]//4 #不应受到花色影响，故除以4后比较
        return 0

        
    fullHouse1, threeCardValue1, twoCardValue1 = isFullHouse(countItems1)
    fullHouse2, threeCardValue2, twoCardValue2 = isFullHouse(countItems2)
    if fullHouse1 is True and fullHouse2 is False:
        return -1
    elif fullHouse1 is False and fullHouse2 is True:
        return 1
    elif fullHouse1 is True and fullHouse2 is True:
        if threeCardValue1 != threeCardValue2:
            return threeCardValue1 - threeCardValue2
        if twoCardValue1 != twoCardValue2:
            return twoCardValue1 - twoCardValue2
        return 0

    
    fourOfAKind1, fourKindCardValue1, singleCardValue1 = isFourofAKind(countItems1)
    fourOfAKind2, fourKindCardValue2, singleCardValue2 = isFourofAKind(countItems2)
    if fourOfAKind1 is True and fourOfAKind2 is False:
        return -1
    elif fourOfAKind1 is False and fourOfAKind2 is True:
        return 1
    elif fourOfAKind1 is True and fourOfAKind2 is True:
        if fourKindCardValue1 != fourKindCardValue2:
            return fourKindCardValue1 - fourKindCardValue2
        if singleCardValue1 != singleCardValue2:
            return singleCardValue1 - singleCardValue2
        return 0
    
    straightFlush1, maxSingleCardInt1 = isStraightFlush(suit1)
    straightFlush2, maxSingleCardInt2 = isStraightFlush(suit2)
    if straightFlush1 is True and straightFlush2 is True:
        return maxSingleCardInt1//4 - maxSingleCardInt2//4
    else:
        # This part should never be arrived
        logging.critical("suit1: " + str(suit1) + " suit2: " + str(suit2))
        exit()
