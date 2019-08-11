import gym
import tensorflow as tf
from matplotlib import pyplot as plot
from gym_mahjong.envs.mahjong_his_env import MahjongEnv

env = gym.envs.make('Mahjong-v0')
print(env.action_space)
class QLearning:
    def __init__(self,
                 env,
                 ):
        self.env = env
        self.actions = env.action_space
        self.observations = env.observation_space
        self.learing_rate = 0.01


    # TODO

    def build_network(self):
        # target net
        self.state = tf.placeholder(tf.int32,[None,self.observations],'state')
        # self.target = tf.placeholder(tf.int32,[None,self.actions],'Target_Q')
        with tf.variable_scope('target_network'):
            variables = ['target_variables',tf.GraphKeys.GLOBAL_VARIABLES]


        return
    # TODO

    def learn(self):
        return
    # TODO