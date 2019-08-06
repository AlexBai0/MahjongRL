import gym
from gym import error,spaces,utils,Env
from gym.utils import seeding
from gym_mahjong.envs.player import Player,convert
from copy import copy
import numpy as np
from utils.state_tran import State_tran
import os
import random

class MahjongEnv(gym.Env):
    metadata = {'render.modes':['human']}
    """"
    Action space is a tuple of :
    the players discarding options (1-34),
    the players calling options (CHI, PON, KAN, RIICHI, WIN)

    All tiles are represented as a number from 0-33
    """
    def __init__(self,gamelog_path = '/System/Volumes/Data/Users/alexbai/Desktop/Project/MahjongAIagent/sxb1376/utils/converted/gamelogs'):
        self.gamelog = gamelog_path
        self.player = Player(0,False)
        self.opponents = [Player(1,True),Player(2,True),Player(3,True)]
        self.players = [self.player].extend(self.opponents)

        # Action include 34 kinds of hand cards
        # 0-33 tile number
        self.action_space = spaces.Discrete(34)

        # Agent's observation of the game state
        self.observation_space = spaces.Tuple([
            spaces.Tuple( [# self player
                spaces.Box(low=0,high=34,shape=(1,34),dtype=np.int) ,   #self hand
                spaces.Box(low=0,high=34,shape=(1,34),dtype=np.int),    #self discarded
                spaces.Discrete(1)                                      #self riichi state
            ]),
            spaces.Tuple([ # opponents
                spaces.Box(low=0, high=34, shape=(1, 34), dtype=np.int),  # opponent discarded
                spaces.Discrete(1)                                        # opponent riichi state
            ]*3),
            # round informations
            spaces.Box(low=0, high=34, shape=(1, 34), dtype=np.int),  # dora indicators
            spaces.Discrete(1),                                                       # round wind
            # spaces.Box(low=0, high=136, shape=(1,136),dtype=np.int)  #deck
        ])

        self.seed()
        self.reset()


    def seed(self,seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """
        Run one step of the environment. When current episode is ended
        (any player calls, the game ends with a winner or draw),then reset is called
        to reset the environment
        :param action: an action of the agent player
        :return: observation of the game state, reward of the action, whether the episode is ended
        """
        # Validate action
        assert (self.action_space.contains(action))
        # Game is finished
        if self.finish:
            return self.state,0.,True,self.state

        # Step one move
        s = self.steps[self.current_step]
        # Draw and discard
        # s[0] = player_number
        # s[1] = move type 0 draw, 1 discard
        # s[2] = card number
        #
        if s[1]>2:
            self.finish = True
            return self.state,
        # TODO

    def deal(self):
        if self.remaining == 14:
            self.finish = True
        else:
            self.remaining -=1
            return self.deck[self.remaining]
    #     TODO

    def possibleActions(self,player_seat,state):
        actions=[]
        #
        # if self.latest_discard:
        #     if self.players[player_seat].canChi(self.latest_discard)[0]:
        #         actions.extend(self.players[player_seat].canChi(self.latest_discard)[1])
        #     if self.players[player_seat].canPon(self.latest_discard):
        #         actions.append(37)
        #     if self.players[player_seat].canKan(self.latest_discard):
        #         actions.append(39)
        #     if self.turn ==player_seat:
        #         if self.players[player_seat].canR(self.latest_discard)[0]:
        #             actions.append(self.players[player_seat].canR(self.latest_discard)[1])
        #         else:
        #             for t in range(34):
        #                 if self.players[player_seat].hand[t]>0:
        #                     actions.append(t)
        for a in range(34):
            if self.players[player_seat].hand[a]>0:
                actions.append(a)

        return actions

    def randomActions(self,player_seat,state):
        if len(self.possibleActions(player_seat,state)) ==0:
            return 'Pass'
        else:
            return np.random.choice(self.possibleActions(player_seat,state))

    def reset(self):
        """
        Reset the environment to a start state
        :return:  initial observation of the state
        """
        file = random.choice(os.listdir(self.gamelog))  # Randomly choose a game to initialize the environment
        state_tran = State_tran(os.path.join(self.gamelog,file))
        self.player = state_tran.players[0]
        for i in range(3):
            self.opponents[i] = state_tran.players[i+1]
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
        [self.player.hand,self.player.discarded,self.player.riichi]
            ]
        for op in self.opponents:
            self.state['Players'].append([op.discarded,op.riichi])
        self.state['Round']=[self.dora_indicators]
        self.state['Previous'] = [copy(self.state['Players']),copy(self.state['Round'])]
        return self.state


    def render(self, mode='human'):
        self
        # TODO

    def close(self):
        self
        # TODO
