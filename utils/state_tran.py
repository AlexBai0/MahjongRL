import os
import re
import numpy as np
from gym_mahjong.envs.player import Player


class State_tran():

    def __init__(self,path):
        self.round_file = open(path,"r")
        self.txt = self.round_file.read()
        self.hands = []
        self.steps = []
        self.dora_indicators = []
        self.wind = None
        self.initDora()
        self.initHand()
        self.initSteps()
        self.players = []
        self.initPlayers()
        # self.write(path)

    # def write(self,path):
    #     new_path = re.sub(r'/\d.txt',"",path)
    #     new_path = "./"+re.sub('converted',"toread",new_path)
    #     if not os.path.exists(new_path):
    #         os.makedirs(new_path)
    #     filename = "./" + re.sub('converted','toread',path)
    #     file = open(filename,"w")
    #     for d in self.dora_indicator:
    #         file.write(d)
    #         file.write('\n')
    #     for h in self.hands:
    #         for t in self.hands[h]:
    #             file.write(self.hands[h][t])
    #             file.write(',')
    #         file.write('\n')
    #     for s in self.steps:
    #         for e in self.steps[s]:
    #             file.write(self.steps[s][e])
    #             file.write(',')
    #         file.write('\n')

    def initPlayers(self):
        self.players.append(Player(0,False))
        for i in range(3):
            self.players.append(Player(i,True))
        for j in range(4):
            self.players[j].initHand34(self.hands[j])


    def initHand(self):
        self.oya = int(re.search('oya="(.+?)',self.txt).group(1))
        hands_tem = []
        for i in range(4):
            handtxt = re.findall('hai' + str(i) + '="(.+?)"',self.txt)
            hand = [tile.split(',') for tile in handtxt]
            for j in range(len(hand[0])):
                hand[0][j] = int(int(hand[0][j])/4)
            hands_tem.append(hand[0])
        if self.oya == 0:
            self.hands = hands_tem
        if self.oya == 1:
            self.hands.append(hands_tem[1])
            self.hands.append(hands_tem[2])
            self.hands.append(hands_tem[3])
            self.hands.append(hands_tem[0])
        if self.oya == 2:
            self.hands.append(hands_tem[2])
            self.hands.append(hands_tem[3])
            self.hands.append(hands_tem[0])
            self.hands.append(hands_tem[1])
        if self.oya == 3:
            self.hands.append(hands_tem[3])
            self.hands.append(hands_tem[0])
            self.hands.append(hands_tem[1])
            self.hands.append(hands_tem[2])

            # handtext = [x.split(',') for x in handtext]
            # hand = [[int(x/4) for x in text] for text in handtext]
            # for t in range[len(hand[0])]:
            #     self.hands[i][int(hand[t])/4] += 1

    def initDora(self):
        seedtxt = re.findall('seed="(.+?)"',self.txt)
        seedtxt = [s.split(',') for s in seedtxt]
        seed = seedtxt[0]
        self.dora_indicators.append(int(int(seed[5])/4))
        self.wind = int(int(seed[0])/4)
        print(self.dora_indicators)

    # def initDraws(self):
    #     draws = []
    #     for drawed in re.findall(r'<T(.+?)/>',self.txt):
    #         draws.append(int(int(drawed)/4))
    #     self.draws.append(draws)
    #     draws = []
    #     for drawed in re.findall(r'<U(.+?)/>', self.txt):
    #         draws.append(int(int(drawed)/4))
    #     self.draws.append(draws)
    #     draws = []
    #     for drawed in re.findall(r'<V(.+?)/>', self.txt):
    #         draws.append(int(int(drawed)/4))
    #     self.draws.append(draws)
    #     draws = []
    #     for drawed in re.findall(r'<W(.+?)/>', self.txt):
    #         draws.append(int(int(drawed)/4))
    #     self.draws.append(draws)


    def initSteps(self):
        for tag in re.findall(r'<(.+?)/>',self.txt):
            if tag[0] == 'T':
                self.steps.append([0,0,int(tag[1:])])
            elif tag[0] == 'U':
                self.steps.append([1,0,int(tag[1:])])
            elif tag[0] == 'V':
                self.steps.append([2,0,int(tag[1:])])
            elif tag[0] == 'W':
                self.steps.append([3,0,int(tag[1:])])
            elif tag[0] == 'D' :
                if tag[1]=='O':
                    doratxt = re.findall('hai="(.+?)"',tag)
                    self.steps.append([7,int(int(doratxt[0])/4)])
                else:
                    self.steps.append([0,1,int(tag[1:])])
            elif tag[0] == 'E':
                self.steps.append([1,1,int(tag[1:])])
            elif tag[0] == 'F':
                self.steps.append([2,1,int(tag[1:])])
            elif tag[0] == 'G':
                self.steps.append([3,1,int(tag[1:])])
            elif tag[0] == 'R' and tag[1] == 'E':
                self.steps.append([int(tag[11]), 2])
            elif tag[0] == 'N':
                call = self.tagToMelds(tag)
                if call[1] == 3:
                    if int(tag[7])>0:
                        call[1] = int(tag[7])-1
                    else:
                        call[1] = 3
                elif call[1] ==1:
                    if int(tag[7])==3:
                        call[1]= 0
                    else:
                        call[1]= int(tag[7]) +1
                elif call[1]==2:
                    call[1] = (int(tag[7])%2)*(4-int(tag[7]))+(int(tag[7])%2 -1)*(2-int(tag[7]))
                else:
                    call[1] = int(tag[7])
                call.insert(0,int(tag[7]))
                print(call)
                self.steps.append(call)
            elif tag[0]=='A':
                who = re.search('who="(.+?)"',tag).group(1)
                fromwho = re.search('fromWho="(.+?)"',tag).group(1)
                machi = re.search('machi="(.+?)"',tag).group(1)
                ten = re.search('ten="(.+?)"',tag).group(1)
                ten = ten.split(',')
                who = int(who)
                fromwho = int(fromwho)
                machi = int(machi)
                ten = [int(t) for t in ten]
                self.steps.append([who,8,fromwho,machi,ten[0],ten[1],ten[2]])
            elif tag[0] == 'R':
                self.steps.append(['DRAW'])


    def tagToMelds(self,tag):
        """
        [x,fromwho,num,suit,n]
        x:  3->chi
            4->kakan
            5->pon
            6->kan
        :param tag:
        :return:
        """
        mentsu =int(re.findall('m="(.+?)"',tag)[0])
        fromwho = mentsu&0x0003 # get from who upper 3, opposite 2, next 1
        if mentsu&0x0004 != 0: #Shunzi
            pattern = (mentsu&0xfc00)>>10     #pattern from 0 to 62
            num = pattern%3                       # target tile
            suit =int(int(pattern/3)/7)                    # suit of tile
            n = int(pattern/3)%7 +1               # smallest of shunzi
            return [3,fromwho,num,suit,n]
        elif mentsu&0x0008 !=0:  #Kakan
            pattern = (mentsu&0xfe00) >>9
            num = pattern%3
            pattern = int(pattern/3)
            suit = int(pattern/9)
            n = pattern%9 +1
            return [4,fromwho,num,suit,n]
        elif mentsu&0x0010 != 0: #pon
            pattern = (mentsu & 0xfe00) >> 9
            num = pattern % 3
            pattern = int(pattern / 3)
            suit = int(pattern / 9)
            n = pattern % 9 + 1
            return [5, fromwho, num, suit, n]
        else:           #kan
            pattern = (mentsu & 0xff00) >> 8
            num = pattern % 4
            pattern = int(pattern / 4)
            suit = int(pattern / 9)
            n = pattern % 9 + 1
            return [6, fromwho, num, suit, n]





# state_tran = State_tran('converted/mjlog_pf4-20_n11/2013012805gm-00c1-0000-12155f14&tw=3/1.txt')
#     # print(re.findall(r'<(.+?)/>',state_tran.txt))
#     # print(state_tran.steps)
#     # print(state_tran.hands)
# # print(state_tran.steps)
# print(state_tran.oya)
# print(state_tran.hands)