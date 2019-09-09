'''
A gym environment for mahjong game
Alex-Bai 7.7.2019
'''
import gym
from gym import error,spaces,utils,Env
from gym.utils import seeding
from gym_mahjong.envs.player import Player,convert
from copy import copy
import numpy as np
from utils.state_tran import State_tran
import os
import random
from mahjong.shanten import Shanten
import settings

class MahjongEnv(gym.Env):
    metadata = {'render.modes':['human']}
    """"
    Action space is a tuple of :
    the players discarding options (1-34),
    the players calling options (CHI, PON, KAN, RIICHI, WIN)

    All tiles are represented as a number from 0-33
    """
    def __init__(self,gamelog_path = settings.GAMELOG_PATH):
        self.gamelog = gamelog_path
        self.player = Player(0,False)
        self.opponents = [Player(1,True),Player(2,True),Player(3,True)]
        self.players = []

        # Action include 34 kinds of hand cards
        # 0-33 tile number
        self.action_space = 34

        # Agent's observation of the game state
        # self.observation_space = spaces.Tuple([
        #     spaces.Tuple( [# self player
        #         spaces.Box(low=0,high=34,shape=(1,34),dtype=np.int) ,   #self hand
        #         spaces.Box(low=0,high=34,shape=(1,34),dtype=np.int),    #self discarded
        #         spaces.Discrete(1)                                      #self riichi state
        #     ]),
        #     spaces.Tuple([ # opponents
        #         spaces.Box(low=0, high=34, shape=(1, 34), dtype=np.int),  # opponent discarded
        #         spaces.Discrete(1)                                        # opponent riichi state
        #     ]*3),
        #     # round informations
        #     spaces.Box(low=0, high=34, shape=(1, 34), dtype=np.int),  # dora indicators
        #     spaces.Discrete(1),                                                       # round wind
        #     # spaces.Box(low=0, high=136, shape=(1,136),dtype=np.int)  #deck
        # ])
        self.observation_space = 34
        self.seed()
        self.reset_()


    def seed(self,seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """
        Run one step of the environment. When current episode is ended
        (any player calls, the game ends with a winner or draw),then reset is called
        to reset the environment
        :param action: an action of the agent player
        :return: observation of the game state, reward of the action, whether the episode is ended, whether the move is validated
        as real players move
        """
        # Episode is finished
        if self.finish:
            return self.toReturn(self.state),0.,True,False
        # Action is not a possible move
        if action not in self.possibleActions(self.state):
            return self.toReturn(self.state),0.,False,False


        s = self.steps[self.current_step]
        # Step until player's discarding
        while s[0] > 0 or (s[0] == 0 and s[1] == 0):
            self.playermove()
            if self.current_step >= len(self.steps):
                return self.toReturn(self.state), 0., True,0
            s = self.steps[self.current_step]
            # Episode is finished by opponents
            if self.finish:
                return self.toReturn(self.state), 0., True,0
        # Draw and discard
        # s[0] = player_number
        # s[1] = move type 0 draw, 1 discard
        # s[2] = card number
        is_playermove = 0
        called = 0
        next_s = self.steps[self.current_step+1]
        if s[0] == 0 and s[1] == 1:  # Player discarding, possible move
            if action == convert(s[2]): # Move validated as the same as real player, good
                self.playerdiscard(action)
                is_playermove = True
                shanten = Shanten().calculate_shanten(self.state['Players'][0][0]) # Calculate the distance from winning
                shanten_prv = Shanten().calculate_shanten(self.state['Previous'][0][0][0]) # Calculate previous distance
                if next_s[1] > 1 and next_s[0] == 0: #Discarded get called, bad
                    called = 1
                return self.toReturn(self.state),self.cal_reward(shanten,shanten_prv,is_playermove,called),False,is_playermove
            else: # unexpected move, finish
                self.playerdiscard(action)
                self.finish = True
                shanten = Shanten().calculate_shanten(self.state['Players'][0][0]) # Calculate the distance from winning
                shanten_prv = Shanten().calculate_shanten(self.state['Previous'][0][0][0]) # Calculate previous distance
                return self.toReturn(self.state),self.cal_reward(shanten,shanten_prv,is_playermove,called),True,is_playermove

        return self.toReturn(self.state),-10.,True,0

    def cal_reward(self,shanten,shanten_prv,playermove,called):
        impro = shanten_prv - shanten  # Improvement of hand, larger the better, -1, 0, 1
        # return 3 * impro - shanten - playermove*called + playermove*0.2
        return 2*impro+1

    def toReturn(self,state):
        p = state['Players']
        # ob = np.append(np.append(np.append(np.append(p[0][0],p[0][1]),p[1][0]),p[2][0]),p[3][0])
        # a = ob.reshape(ob.shape[0],1)
        ob = p[0][0]
        return ob.reshape(ob.shape[0],1).T

    def possibleActions(self,state):
        actions=[]
        for a in range(34):
            if state['Players'][0][0][a]>0:
                actions.append(a)
        return actions

    def playerdiscard(self,action):
        """
        Discard, and update state
        :param action: action of player
        :return:
        """
        self.state['Previous'] = [copy(self.state['Players']),copy(self.state['Round'])]
        self.player.discard(action)
        self.update()

    def playermove(self):
        """
        Moves doesn't affect learning
        :return:
        """
        s = self.steps[self.current_step]
        if s[0] == 0: #Player move
            if s[1] == 0: #Draw
                self.player.draw(s[2])
        elif s[1] == 0: # Opponents draw
            self.players[s[0]].draw(s[2])
        elif s[1] == 1: # Opponents discard
            self.players[s[0]].discard(convert(s[2]))
        elif s[1] > 1: # Opponents call, episode finish
            self.finish = True
        self.current_step+=1
        self.update()

    def update(self):
        self.state['Players']=[
        [self.player.hand,self.player.discarded,self.player.riichi]
            ]
        for op in self.opponents:
            self.state['Players'].append([op.discarded,op.riichi])
        self.state['Round']=[self.dora_indicators]

    # def randomActions(self,player_seat,state):
    #     if len(self.possibleActions(player_seat,state)) ==0:
    #         return 'Pass'
    #     else:
    #         return np.random.choice(self.possibleActions(player_seat,state))

    def reset_(self):
        """
        Reset the environment to a start state
        :return:  initial observation of the state
        """
        file = random.choice(os.listdir(self.gamelog))  # Randomly choose a game to initialize the environment
        state_tran = State_tran(os.path.join(self.gamelog,file))
        self.player = state_tran.players[0]
        self.players.append(self.player)
        for i in range(3):
            self.opponents[i] = state_tran.players[i+1]
            self.players.append(self.opponents[i])
        self.steps = state_tran.steps
        self.current_step = 0
        self.dora_indicators = state_tran.dora_indicators

        # if self.opponents == 'random': #Using env with random opponents
        self.state = {}
        self.finish = False
        #     self.turn = 0
        #     self.deck =random.shuffle(range(0,135))   #136 format
        #     self.remaining = 84
        #     self.kans = 0
        #     self.latest_discard = None
        self.state['Players']=[
        [self.player.hand,self.player.discarded]
            ]
        for op in self.opponents:
            self.state['Players'].append([op.discarded])
        self.state['Round']=[self.dora_indicators]
        self.state['Previous'] = [copy(self.state['Players']),copy(self.state['Round'])]
        return self.toReturn(self.state)


    def render(self, mode='human'):
        self
        # TODO

    def close(self):
        self
        # TODO
