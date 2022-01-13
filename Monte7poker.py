##프로젝트 목표, 7포커를 할 때 판단을 도와줄 확률 계산 보조 프로그램 구현##

import random
import operator
import copy

class Card:
    def __init__(self, kind, number):
        self.kind = kind        #symbol
        self.number = number

class Player:
    def __init__(self):
        self.hands = []
        self.ongame = 1

    def printCards(self):
        for card in self.hands:
            if card.number == 14:
                print(card.kind + str('A'), end=' ')
                continue
            print(card.kind + str(card.number) ,end =' ')
        if not self.ongame:
            print('Dead', end =' ')
        

class Poker:
    def __init__(self, playerCnt = 1):
        self.playerCnt = playerCnt
        self.deck = []
        self.players = []
        self.generateCards()
        self.shuffleCards()
        self.createPlayers()

    def generateCards(self):
        self.deck = []
        kinds = ['Spade', 'Heart', 'Diamond', 'Clover']
        
        for i in range(4):
            for j in range(13):
                card = Card(kinds[i], j + 2)
                self.deck.append(card)

        return self.deck

    #just shuffle deck
    def shuffleCards(self):
        random.shuffle(self.deck)

    #make players
    def createPlayers(self):
        for i in range(self.playerCnt):
            player = Player()
            self.players.append(player)

    def reorder(self):
        for player in self.players:
            player.hands.sort(key = operator.attrgetter('number', 'kind'))

    def printPlayerCards(self):
        player_num = 0

        for player in self.players:
            print("\nplayer", player_num, ":", end=' ')
            player.printCards()
            player_num += 1
        print()

    def isStraight(self, hands):
        numCnt = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}
        stflag = 0
        stcount = 0
        res = 0
        rank = 0

        for card in hands:
            numCnt[card.number] += 1

        if(numCnt[10] and numCnt[11] and numCnt[12] and numCnt[13] and numCnt[14]):  #mountain
            res = 1
            return (res, rank)

        elif(numCnt[14] and numCnt[2] and numCnt[3] and numCnt[4] and numCnt[5]):  #back
            res = 2
            return (res, rank)

        for key in numCnt.keys() :
            if numCnt[key] :
                stcount += 1
                if stcount > 4 : 
                    rank = key
                    stflag = 1
            else: 
                stcount = 0
        if stflag:
            res = 3
        
        return (res, rank)

    def isFlush(self, hands):
        kindlist = [[0 for col in range(0)] for row in range(4)]
        res = 0
        rank = 0
        for card in hands:             
            if card.kind == 'Spade':
                kindlist[0].append(card)
            elif card.kind == 'Diamond':
                kindlist[1].append(card)
            elif card.kind == 'Heart':
                kindlist[2].append(card)
            else:
                kindlist[3].append(card)

        for i in range(4):
            if len(kindlist[i]) > 4:
                st = self.isStraight(kindlist[i])
                if st[0] == 1:                           #Royal st fl
                    res = 1
                elif st[0] == 2:                         #Back  st fl
                    res = 2
                elif st[0] == 3:
                    res = 3
                else:
                    res = 4
                temp = kindlist[i].pop()
                rank = temp.number
                break
        return (res, rank)


    def isPair(self, hands):
        numCnt = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}
        pairCnt = 0
        tripleCnt = 0
        fourflag = 0
        fourrank, triprank, pairrank, top = 0, 0, 0, 0

        for card in hands :
            numCnt[card.number] += 1

        for key in numCnt.keys() :
            if (numCnt[key] >= 4) :
                fourflag = 1
                fourrank = key

            elif (numCnt[key] == 3) :
                tripleCnt = tripleCnt + 1
                triprank = key
            
            elif (numCnt[key] == 2) :
                pairCnt = pairCnt + 1
                pairrank = key

            elif (numCnt[key] == 1) :
                top = key
        res = [(fourflag, fourrank), (tripleCnt,triprank), (pairCnt, pairrank), top]
        return res

    def checkMade(self, hands):
        stState = self.isStraight(hands)        #Mountain,Back,Straight
        pairState = self.isPair(hands)          #Four,Triple,pair,top
        FlushState = self.isFlush(hands)        #RSF,BSF,SF,Flush
        res = (None,None) 
        if FlushState[0] == 1:          #RSF
            res = (0,FlushState[1])
        elif FlushState[0] == 2:        #BSF
            res = (1,FlushState[1])
        elif FlushState[0] == 3:        #SF
            res = (2,FlushState[1])
        elif pairState[0][0]:           #Four
            res = (3,pairState[0][1])
        elif (pairState == 2) or (pairState[1][0] > 0 and pairState[2][0] > 0):   #Full
            res = (4,pairState[1][1])
        elif FlushState[0] == 4:    #Flush
            res = (5,FlushState[1])
        elif stState[0] == 1:       #Mountain
            res = (6,stState[1])
        elif stState[0] == 2:       #BS
            res = (7,stState[1])
        elif stState[0] == 3:       #Straight
            res = (8,stState[1])
        elif pairState[1][0] > 0:   #Triple
            res = (9,pairState[1][1])
        elif pairState[2][0] > 1:   #2Pair
            res = (10,pairState[2][1])
        elif pairState[2][0]:       #Pair
            res = (11,pairState[2][1])
        else:                       #Top
            res = (12,pairState[3])
        return res

    
    def checkwinner(self):
        playermade = [0 for _ in range(self.playerCnt)]
        winner = []

        for i in range(self.playerCnt):
            if not self.players[i].ongame:
                playermade[i] = (i,(float('inf'),float('inf')))
                continue
            self.reorder()
            playermade[i] = (i,self.checkMade(self.players[i].hands)) #
        
        playermade.sort(key = lambda x: (x[1][0],-x[1][1],x[0]))        #(i,(made,rank))
        maxmade = playermade[0][1]                                      #(made,rank)

        for i in range(len(playermade)):
            if playermade[i][1] == maxmade:
                winner.append(playermade[i])    #(pnum,(made,rank))
        return winner


    def Monte(self, trial, showCase):
        wincnt = 0
        drawcnt = 0
        cnt = 0

        while True:
            if cnt == trial:
                break

            temp = Poker(self.playerCnt)
            temp.deck = copy.deepcopy(self.deck)
            temp.players = copy.deepcopy(self.players)
            temp.shuffleCards()

            for player in temp.players:
                if not player.ongame :
                    continue

                while len(player.hands) < 7:
                    card = temp.deck.pop()
                    player.hands.append(card)
            winner = temp.checkwinner()
            
            if (showCase == 1):
                print('\nCASE :',cnt,end = '')
                temp.printPlayerCards()
                if len(winner) > 1:
                    print('Draw')
                for winp in winner:
                    print('Winner : Player',winp[0], '  Made :', self.decordMade(winp[1][0]), '  Rank : ', winp[1][1])

            if winner[0][0] == 0:
                if len(winner) == 1: wincnt += 1
                else : drawcnt += 1
            cnt += 1

        return wincnt / trial * 100,  drawcnt / trial * 100

##For convinent
    def decordMade(self, num):
        if num == 0:
            return 'Royal'
        elif num == 1:
            return 'Back Straight Flush'
        elif num == 2:
            return 'Straight Flush'
        elif num == 3:
            return 'Four Card'
        elif num == 4:
            return 'Full House'
        elif num == 5:
            return 'Flush'
        elif num == 6:
            return 'Mountain'
        elif num == 7:
            return 'Back Straight'
        elif num == 8:
            return 'Straight'
        elif num == 9:
            return 'Triple'
        elif num == 10:
            return 'TwoPair'
        elif num == 11:
            return 'Pair'
        elif num == 12:
            return 'Top'
        return -1

    def giveCard(self, pnum, kind, num):
        if num == 'A' or num == '1':
            num = 14
        pnum = int(pnum)
        num = int(num)
        if pnum > self.playerCnt or pnum < 0:
            print('Wrong Player Input')
            return - 1

        if kind == 's':
            kind = 'Spade'
        elif kind == 'd':
            kind = 'Diamond'
        elif kind == 'c':
            kind = 'Clover'
        elif kind == 'h':
            kind = 'Heart'
        else:
            print('Wrong Kind Input')
            return - 1

        if num > 14 or num < 1:
            print('Wrong Number input')
            return - 1

        for card in self.deck:
            if card.kind == kind and card.number == num:
                self.players[pnum].hands.append(card)
                self.deck.remove(card)
                return 1
        print("can't find card")
        return -1

    def GoRound(self, round):    
        for i in range(len(self.players)):
            while True:
                if i == 0: 
                    if len(self.players[0].hands) < round + 3:
                        card = self.deck.pop()
                        self.players[0].hands.append(card)
                        if len(self.players[0].hands) >= round + 3:
                            break
                else:
                    if round == 4:
                        break

                    if len(self.players[i].hands) < round + 1:
                        card = self.deck.pop()
                        self.players[i].hands.append(card)
                        if len(self.players[i].hands) >= round + 1:
                            break
        return 1

## testcode ##
def calc_prob(p,trial,showCase):
    p.printPlayerCards()
    winprob, drawprob = p.Monte(trial,showCase)
    print('win prob :', round(winprob,2),'%  ', 'draw prob:', round(drawprob,2),'%')

def AutoSimul(p,trial,showCase):
    for i in range(5):
        print("--------Round :",i,'------------' )
        p.GoRound(i)
        calc_prob(p,trial,showCase)
        print('\n--------End of Round', i,'--------')
        a = input()
        if a == 'q':
            break

    return

def MontePoker(p,trial,showCase):
    while True:
        curin = input('\nInput PlayerNum, Kind, Num: ex) 0 s 5\n').split()
        if curin[0] == 'q':
            break
        if curin[1] == 'x':
            p.players[int(curin[0])].ongame = 0
            calc_prob(p,trial,showCase)
            continue

        p.giveCard(curin[0], curin[1], curin[2])
        calc_prob(p,trial,showCase)

while(True):
    pnum = int(input('input Player num: '))
    if 0 > pnum or pnum > 8:
        print('Wrong Input !')
    else:
        break

p = Poker(pnum)
trial = 1000
while(True):
    modesel,printcase = input('input : AutoMode(1/0) PrintCase(1/0)\n').split(' ')
    modesel = int(modesel)
    printcase = int(printcase)
    if not ((printcase == 0) or (printcase == 1)):
        print("Wrong input !")
        continue
    if modesel == 1:
        AutoSimul(p,trial,printcase)
        break
    elif modesel == 0:
        MontePoker(p,trial,printcase)
        break
    else:
        print("Wrong input !")
print("End Program")