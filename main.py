import getFiveCardRankListDf as gfcrldf
import getRankValueDistribution as grvd
import decodeUtils as du

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




if __name__ == "__main__":
    fiveCardsDf = gfcrldf.getFiveCardRankListDf()
    #     cardsForSelectionTest = ["H3", "SK", "D2", "D9", "CJ"]
    # bannedCards = []
    # rankValueDistribution = getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelectionTest), bannedCards, fiveCardsDf)
    # printRankValueDistribution(rankValueDistribution)
    cardsForSelection = []
    print("输入两张你的底牌")
    inputACard("输入第1张底牌。", cardsForSelection)
    inputACard("输入第2张底牌。", cardsForSelection)

    grvd.printBaselineRankValueDistribution(fiveCardsDf)
    rankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf)
    # opponentRankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt([]), cardsForSelection[0:2], fiveCardsDf) 不确定性太大，需要提前计算
    grvd.printRankValueDistribution(rankValueDistribution, role='me', showPlot=True)
    # grvd.printRankValueDistribution(opponentRankValueDistribution, opponent=True, showPlot=True)

    print("接下来输入五张公开牌中的前三张")
    inputACard("首先输入第1张公开牌。", cardsForSelection)
    inputACard("首先输入第2张公开牌。", cardsForSelection)
    inputACard("首先输入第3张公开牌。", cardsForSelection)

    rankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf)
    opponentRankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection[2:]), cardsForSelection[0:2], fiveCardsDf)
    grvd.printRankValueDistribution(rankValueDistribution, role='me', showPlot=False)
    grvd.printRankValueDistribution(opponentRankValueDistribution, role='opponent', showPlot=True)

    print("接下来输入五张公开牌中的第四张")
    inputACard("输入第4张公开牌。", cardsForSelection)
    
    rankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf)
    opponentRankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection[2:]), cardsForSelection[0:2], fiveCardsDf)
    grvd.printRankValueDistribution(rankValueDistribution, role='me', enableKde = False, showPlot=False)
    grvd.printRankValueDistribution(opponentRankValueDistribution, role='opponent', enableKde = False, showPlot=True)

    print("最后输入五张公开牌中的第五张")
    inputACard("输入第5张公开牌。", cardsForSelection)

    rankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection), [], fiveCardsDf)
    opponentRankValueDistribution = grvd.getRankValueDistribution(du.readableCardsToCardsInt(cardsForSelection[2:]), cardsForSelection[0:2], fiveCardsDf)
    grvd.printRankValueDistribution(rankValueDistribution, role='me', enableKde = False, showPlot=False)
    grvd.printRankValueDistribution(opponentRankValueDistribution, role='opponent', enableKde = False, showPlot=True)

    print("七张牌中可选的的组合中最大的排排位为"+str(rankValueDistribution)+"/6191.")