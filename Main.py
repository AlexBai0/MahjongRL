from gym_mahjong.envs.mahjong_his_env import MahjongEnv
import gym
from QLearning import QLearning as QLe
from matplotlib import pyplot as plt
import numpy as np

def playermoveGraph(validation,s):
    import os
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    n = int(len(validation)/s)
    i = 1
    y = []
    while i <= n:
        y.append(np.sum(validation[(i-1)*s:i*s])/s)
        i += 1
    y.append(np.sum(validation[n*s:])/(len(validation)-n*s))
    plt.plot(range(len(y)),y)
    plt.show()

env = gym.envs.make('Mahjong-v0')
QL = QLe(env)
validation = []
for episode in range(30000):
    observation = env.reset_()
    while True:
        action = QL.decision(observation)
        observation_after, reward, finish,validate = env.step(action)
        QL.toHistory(observation,action,reward,observation_after)
        validation.append(validate)
        if (episode > 200) and (episode%5 == 0):
            QL.learn()
            QL.save_model(episode)
            # print('Learned!')

        observation = observation_after

        if finish:
            break

print('done')
QL.toGraph()

playermoveGraph(np.array(validation),100)