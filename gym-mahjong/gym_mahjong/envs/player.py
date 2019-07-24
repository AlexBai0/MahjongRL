import  numpy as np
from gym import error
from mahjong.shanten import Shanten

def convert(t136):
    return int(t136/4)

class Player(object):
    def __init__(self,player_seat,opponent):
        self.playereat = player_seat
        self.isOpponent = opponent
        self.hand = np.zeros(34,int)
        self.discarded = np.zeros(34,int)
        self.melds = np.zeros((34,3),int)
        self.lastDraw = None
        self.riichi = False

    def initHand(self,hand):
        for t136 in hand:
            t34 = convert(t136)
            self.hand[t34] +=1

    def draw(self,tile):
        t34 = convert(tile)
        self.hand[t34] +=1
        self.lastDraw = t34

    def discard(self,tile):
        if(tile>33):
            return False
            raise error.Error('Wrong format')
        if(self.hand[tile]==0):
            return False
            raise error.Error('Illegal discard')
        self.hand[tile] -=1
        self.discarded[tile] -=1
        return True

    def canChi(self,tile):
        chiOpt=[]
        if self.isLowChi(tile):
            chiOpt.append(34)
        if self.isMidChi(tile):
            chiOpt.append(35)
        if self.isHighChi(tile):
            chiOpt.append(36)
        return (self.isHighChi(tile) or self.isMidChi(tile) or self.isLowChi(tile)), chiOpt

    def chi(self,tile,chiOpt):
        if chiOpt==34:
            self.hand[tile-1] -=1
            self.hand[tile-2] -=1
            self.melds[0][tile] +=1
            self.melds[0][tile-1] +=1
            self.melds[0][tile-2] +=1
        if chiOpt == 35:
            self.hand[tile - 1] -= 1
            self.hand[tile +1] -= 1
            self.melds[0][tile] += 1
            self.melds[0][tile - 1] += 1
            self.melds[0][tile +1] += 1
        if chiOpt == 36:
            self.hand[tile + 1] -= 1
            self.hand[tile + 2] -= 1
            self.melds[0][tile] += 1
            self.melds[0][tile + 1] += 1
            self.melds[0][tile + 2] += 1

    def pon(self,tile):
        self.hand[tile] -= 2
        self.melds[1] += 3
        return True

    def kakan(self):
        self.hand[self.lastDraw] -=1
        self.melds[1][self.lastDraw] -= 3
        self.melds[2][self.lastDraw] +=4
        return True

    def kan(self,tile):
        self.hand[tile] -=3
        self.melds[2][tile] +=4

    def canKan(self,tile):
        return self.hand[tile]>2

    def canKakan(self,):
        return self.melds[1][self.lastDraw]>2

    def canPon(self,tile):
        return self.hand[tile] > 1

    def isMidChi(self,tile):
        if tile%9==0 and tile%9==8:
            return False
        else:
            return self.hand[tile-1]>0 and self.hand[tile+1]>0

    def isLowChi(self,tile):
        if tile%9<2:
            return False
        else:
            return self.hand[tile-1]>0 and self.hand[tile-2]>0

    def isHighChi(self,tile):
        if tile%9 >6:
            return False
        else:
            return self.hand[tile+1]>0 and self.hand[tile+1]>0

    def canCall(self,tile):
        return self.canChi(tile) or self.canPon(tile) or self.canKan(tile)

    def canR(self,tile):
        # TODO
        return
