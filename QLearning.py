import gym
import numpy as np
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
        self.current_history = 0
        self.max_history = 800
        self.history = []
        self.epsilon = 0.9
        self.sess = tf.Session()
        self.generate_model()

    # TODO

    def generate_model(self):
        # evaluate network
        self.state = tf.placeholder(tf.int32,[None,self.observations])
        self.target = tf.placeholder(tf.float32,[None,self.actions])

        # Store variables in a scope
        variables = ['evaluate_variables',tf.GraphKeys.GLOBAL_VARIABLES]
        weights1_ini = tf.initializers.random_normal(stddev=0.3)
        bias1_ini = tf.initializers.constant(value=0.1)
        # First layer of nn
        weights1 = tf.get_variable(shape=[self.observations,10],collections=variables,initializer=weights1_ini)
        bias1 = tf.get_variable(shape=[1,10],collections=variables,initializer=bias1_ini)
        layer1 = tf.nn.relu(tf.matmul(self.state,weights1)+bias1)
        #  Second layer of nn
        weights2 = tf.get_variable(shape=[10,self.actions],collections=variables,initializer=weights1_ini)
        bias2 = tf.get_variable(shape=[1,self.actions],collections=variables,initializer=bias1_ini)
        self.evaluate_nn = tf.matmul(layer1,weights2) + bias2

        self.loss = tf.reduce_mean(tf.square(self.evaluate_nn-self.target),reduction_indices=[1])
        self.train_one = tf.train.GradientDescentOptimizer(self.learing_rate).minimize(self.loss)

        # target network
        self.state_ = tf.placeholder(tf.int32,[None,self.observations])
        variables_ = ['target_variables',tf.GraphKeys.GLOBAL_VARIABLES]
        # First layer
        weights1_ = tf.get_variable(shape=[self.observations,10],collections=variables_,initializer=weights1_ini)
        bias1_ = tf.get_variable(shape=[1, 10], collections=variables_, initializer=bias1_ini)
        layer1_ = tf.nn.relu(tf.matmul(self.state_,weights1_)+bias1_)
        #Second layer
        weights2_ = tf.get_variable(shape=[10,self.actions],collections=variables_,initializer=weights1_ini)
        bias2_ = tf.get_variable(shape=[1,self.actions], collections=variables_, initializer=bias1_ini)
        self.target_nn = tf.matmul(layer1_,weights2_)+bias2_

    def learn(self):
        return
    # TODO

    def toHistory(self,state,action,reward,next_state):
        if self.current_history > self.max_history:
            self.history[self.current_history % self.max_history]= [state,action,reward,next_state]
        else:
            self.history.append([state,action,reward,next_state])
        self.current_history += 1

    def decision(self,observation):
        if np.random.rand()<self.epsilon:
            actions = self.sess.run(self.evaluate_nn,feed_dict={self.state:observation})
            return np.argmax(actions)
        else:
            return np.random.randint(0,34,np.int)

