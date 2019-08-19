import gym
import numpy as np
import random
import tensorflow as tf
import copy
from matplotlib import pyplot as plt


class Network:
    def __init__(self,collections,observation,state,actions,number):
        self.observations = observation
        self.state = state
        self.actions = actions
        weights_ini = tf.initializers.random_normal(stddev=0.3)
        bias_ini = tf.initializers.constant(value=0.1)
        # First layer of nn
        weights1 = tf.get_variable(shape=[self.observations, number], collections=collections, initializer=weights_ini,
                                   name='weights1')
        bias1 = tf.get_variable(shape=[1, number], collections=collections, initializer=bias_ini, name='bias1')
        layer1 = tf.nn.relu(tf.matmul(self.state, weights1) + bias1)
        #  Second layer of nn
        weights2 = tf.get_variable(shape=[number, self.actions], collections=collections, initializer=weights_ini,
                                   name='weights2')
        bias2 = tf.get_variable(shape=[1, self.actions], collections=collections, initializer=bias_ini,
                                name='bias2')
        self.network = tf.matmul(layer1, weights2) + bias2


class QLearning:
    def __init__(self,
                 env
                 ):
        self.env = env
        self.actions = env.action_space
        self.observations = env.observation_space
        self.learing_rate = 0.01
        self.current_history = 0
        self.current_learn = 0
        self.max_history = 800
        self.history = []
        self.epsilon = 0
        self.sess = tf.Session()
        self.discount_factor = 0.9
        self.loss_log = []

        self.generate_model()

        qpara = tf.get_collection('q_variables')
        tpara = tf.get_collection('target_variables')
        self.update = [tf.assign(t, e) for t, e in zip(qpara, tpara)]

        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()


    # TODO

    def generate_model(self):
        # evaluate network
        self.state = tf.placeholder(tf.float32,[None,self.observations])
        self.target = tf.placeholder(tf.float32,[None,self.actions])

        # Store variables in a scope
        with tf.variable_scope('q_nn'):
            variables = ['q_variables',tf.GraphKeys.GLOBAL_VARIABLES]
            self.q_nn = Network(variables,self.observations,self.state,self.actions,15).network

        self.loss = tf.reduce_mean(tf.squared_difference(self.target,self.q_nn))
        self.train = tf.train.RMSPropOptimizer(self.learing_rate).minimize(self.loss)

        # target network
        self.state_ = tf.placeholder(tf.float32,[None,self.observations])
        with tf.variable_scope('target_nn'):
            variables_ = ['target_variables',tf.GraphKeys.GLOBAL_VARIABLES]
            self.target_nn = Network(variables_,self.observations,self.state_,self.actions,15).network

    def save_model(self,step):
        if step%1000 == 0:
            self.saver.save(self.sess,"model",global_step=step)
            print('model saved')


    def learn(self):
        if self.current_learn % 300 == 0: # update parameters
            self.sess.run(self.update)
            print('Update model')
        if self.current_history < 33:
            sample = np.array(random.sample(self.history,self.current_history))
        else:
            sample = np.array(random.sample(self.history,32))
        # actions_q =np.zeros(34)
        # q_tmp=np.zeros(34)
        rewards = sample[:,2]
        actions = sample[:,1]
        # a = sample[:,0]
        # actions_q,q_tmp = self.sess.run([self.q_nn,self.target_nn],
        #                                 feed_dict={
        #                                     self.state: sample[:,3],
        #                                     self.state_:sample[:,0]
        #                                 })
        # actions_q = self.sess.run(self.q_nn,feed_dict={self.state:sample[0][0]})
        # q_tmp = self.sess.run(self.target_nn,feed_dict={self.state_:sample[0][0]})
        actions_q = [self.sess.run(self.q_nn,feed_dict={self.state:e[0]}) for e in sample]
        q_tmp = [self.sess.run(self.target_nn,feed_dict={self.state_:e[0]}) for e in sample]
        self.reshapeOut(actions_q)
        self.reshapeOut(q_tmp)
        # for e in sample:
        #     a = self.sess.run(self.q_nn,feed_dict={self.state:e[0]})
        #     b = self.sess.run(self.target_nn,feed_dict={self.state_:e[0]})
        #     np.insert(arr=actions_q,obj=0,values=a,axis=0)
        #     np.row_stack((q_tmp,b))
        q_target = np.array(q_tmp.copy())


        for i in range(len(q_target)): #50
            r= rewards[i]
            dis = self.discount_factor * np.max(actions_q[i])
            q_target[i][actions[i]] = r + dis
        a = np.array([x[0] for x in sample[:,0]])
        losses = self.sess.run(self.loss,feed_dict={self.target:q_target,self.state:a})
        self.sess.run(self.train,feed_dict={self.target:q_target,self.state:a})
        self.loss_log.append(losses)

        if self.epsilon < 0.9:  # epsilon increment
            self.epsilon += 0.03
        elif self.epsilon >= 0.9:
            self.epsilon =0.9

        self.current_learn += 1

    # def update(self):
    #     qpara = tf.get_collection('q_variables')
    #     tpara = tf.get_collection('target_variables')
    #     self.replace_target_op = [tf.assign(t, e) for t, e in zip(qpara, tpara)]
    #
    def reshapeOut(self,q):
        for i in range(len(q)):
            q[i] = q[i][0]


    def toHistory(self,state,action,reward,next_state):
        # actions = np.zeros(34)
        # actions[action] += 1
        if self.current_history > self.max_history:
            self.history[self.current_history % self.max_history]= [state,action,reward,next_state]
        else:
            self.history.append([state,action,reward,next_state])
        self.current_history += 1

    def decision(self,observation):
        if np.random.rand()<self.epsilon:
            actions = self.sess.run(self.q_nn,feed_dict={self.state: observation})
            return np.argmax(actions)
        else:
            return np.random.randint(0,34)

    def toGraph(self):
        import os
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        plt.plot(range(len(self.loss_log)),self.loss_log)
        plt.show()
        print('epsilon:',self.epsilon)
        print('learning time:',self.current_learn)
        print('total history:',self.current_history)


# env = gym.envs.make('Mahjong-v0')
# QL = QLearning(env)
# for episode in range(300):
#     observation = env.reset_()
#     while True:
#         action = QL.decision(observation)
#         observation_after, reward, finish = env.step(action)
#         QL.toHistory(observation,action,reward,observation_after)
#         if episode>50:
#             QL.learn()
#             # print('Learned!')
#
#         observation = observation_after
#
#         if finish:
#             break
#
# print('done')
# QL.toGraph()