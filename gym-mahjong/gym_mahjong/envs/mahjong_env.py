import gym
from gym import error,spaces,utils
from gym.utils import seeding
from game.table import Table
from game.player import Player
from game.table_learning import  Table_learning

class MahjongEnv(gym.Env):
    table = None

    dora_indicators = None

    dealer_seat = 0
    round_number = -1
    round_wind_number = 0
    count_of_riichi_sticks = 0
    count_of_honba_sticks = 0

    count_of_remaining_tiles = 0
    count_of_players = 4

    meld_was_called = False

    # array of tiles in 34 format
    revealed_tiles = None

    has_open_tanyao = False
    has_aka_dora = False



    """
    Description:
        A Mahjong game against three tenhou-python-bot players.
    Observation:

        Num     Observation         Min     Max
        0
        1
        2
        3

    """
    def __init__(self):
        self.__init__table()
        self,
        self.action_space = spaces.Discrete()

        # TODO
    def __init__table(self):
        self.table = Table_learning()


    def step(self, action):
        self
        # TODO

    def reset(self):
        self
        # TODO

    def render(self, mode='human'):
        self
        # TODO

    def close(self):
        self
        # TODO