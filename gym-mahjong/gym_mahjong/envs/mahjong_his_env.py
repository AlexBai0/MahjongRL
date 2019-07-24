import gym
from gym import error,spaces,utils
from gym.utils import seeding
from gym_mahjong.envs.player import Player
from copy import copy
import numpy as np
import random


class MahjongEnv(gym.envs):
    """"
    Action space is a tuple of :
    the players discarding options (1-34),
    the players calling options (CHI, PON, KAN, RIICHI, WIN)

    All tiles are represented as a number from 0-33
    """
    def __init__(self,player_seat = 0,opponents = 'random'):
        self.player = Player(0,False)
        self.opponents = [Player(1,True),Player(2,True),Player(3,True)]
        self.players = [self.player].extend(self.opponents)

        # Action include 34 kinds of hand cards, call chi(3) ,  pon,kakan ,kan,riichi, and ron
        # 0-33 tile number , 34-38 call riichi, chi ,pon, kan and ron
        self.action_space = spaces.Discrete(34+8)

        # Agent's observation of the game state
        self.observation_space = spaces.Tuple([
            spaces.Tuple( # self player
                spaces.Box(low=0,high=34,shape=(1,34),dtype=np.int) ,   #self hand
                spaces.Box(low=0,high=34,shape=(1,34),dtype=np.int),    #self discarded
                spaces.Box(low=0,high=34,shape=(1,34,3),dtype=np.int),  #self called melds
                spaces.Discrete(1)                                                     #self riichi state
            ),
            spaces.Tuple([ # opponents
                spaces.Box(low=0, high=34, shape=(1, 34), dtype=np.int),  # opponent discarded
                spaces.Box(low=0, high=34, shape=(1, 34, 3), dtype=np.int),  # opponent called melds
                spaces.Discrete(1)                                                          # opponent riichi state
            ]*3),
            # round informations
            spaces.Box(low=0, high=34, shape=(1, 34), dtype=np.int),  # dora indicators
            spaces.Discrete(1)                                                       # round wind
        ])

        self.seed()
        self.reset()
        print(self.seed())

    def seed(self,seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """
        Run one step of the environment. When current episode is ended
        (agent win the game, opponent win the game or a draw), reset is called
        to reset the environment
        :param action: an action of the agent player
        :return: observation of the game state, reward of the action, whether the episode is ended
        """
        # Validate action
        assert (self.action_space.contains(action))
        if self.finish:
            return self.state,0.,True

        # TODO
    def possibleActions(self,player_seat,state):
        actions=[]
        if self.latest_discard:
            if self.players[player_seat].canChi(self.latest_discard)[0]:
                actions.extend(self.players[player_seat].canChi(self.latest_discard)[1])
            if self.players[player_seat].canPon(self.latest_discard):
                actions.append(37)
            if self.players[player_seat].canKan(self.latest_discard):
                actions.append(39)
            if self.turn ==player_seat:
                if self.players[player_seat].canR(self.latest_discard)[0]:
                    actions.append(self.players[player_seat].canR(self.latest_discard)[1])
                else:
                    for t in range(34):
                        if self.players[player_seat].hand[t]>0:
                            actions.append(t)
        return actions

    def reset(self):
        """
        Reset the environment to a start state
        :return:  initial observation of the state
        """
        if self.opponents == 'random': #Using env with random opponents
            self.state = {}
            self.finish = False
            self.turn = 0
            self.deck =random.shuffle(range(0,135))   #136 format
            self.remaining = 84
            self.kans = 0
            self.latest_discard = None
            self.state['Players']=[
                [self.player.hand,self.player.discarded,self.player.melds,self.player.riichi]
            ]
            for op in self.opponents:
                self.state['Players'].append([op.discarded,op.melds,op.riichi])
            self.dora_indicators = [int(self.deck[4]/4)]
            self.wind = 0
            self.state['Round']=[self.dora_indicators,self.wind,self.remaining,self.kans]
            self.state['Previous'] = [copy(self.state['players']),copy(self.state['Round'])]
            return self.state

    def render(self, mode='human'):
        self
        # TODO

    def close(self):
        self
        # TODO
