from utils.tenhouconnection import Connection
import tensorflow as tf
import gym
from QLearning import QLearning as QLe
import gym_mahjong
import numpy as np

# states= np.zeros(34)
# # state = tf.placeholder(tf.float32,[None,34])
# # model = Network(observation=34,state=state,actions=34,number=15,path='/System/Volumes/Data/Users/alexbai/Desktop/Project/MahjongAIagent/sxb1376/model-2000')
# with tf.Session() as sess:
#     saver = tf.train.import_meta_graph('/System/Volumes/Data/Users/alexbai/Desktop/Project/MahjongAIagent/sxb1376/model-3000.meta')
#     saver.restore(sess,'/System/Volumes/Data/Users/alexbai/Desktop/Project/MahjongAIagent/sxb1376/model-3000')
#     y = tf.get_collection('q_nn')
#     graph = tf.get_default_graph()
#     state = graph.get_operation_by_name('state')
#     sess.run(y,feed_dict={state:states})

def train_and_play():
    env = gym.envs.make('Mahjong-v0')
    QL = QLe(env)
    validation = []
    for episode in range(300):
        observation = env.reset_()
        while True:
            action = QL.decision(observation)
            observation_after, reward, finish, validate = env.step(action)
            QL.toHistory(observation, action, reward, observation_after)
            validation.append(validate)
            if (episode > 200) and (episode % 5 == 0):
                QL.learn()
                # print('Learned!')

            observation = observation_after

            if finish:
                break
    connection = Connection(QL)
    # a = np.zeros(34)
    # b = [0, 1, 2, 3, 55, 66, 77, 89, 111, 60, 123, 131, 132]
    # convert(b,a)
    # connection.hand136 = b
    # connection.hand34 = a
    # print(connection.decision())

    connection.connect()
    auth = connection.authencate()
    print(auth)
    if auth:
        connection.play()
    else:
        connection.end()


def convert(t136,t34):
    for i in t136:
        t34[int(i/4)] +=1

if __name__ == '__main__':
    train_and_play()
