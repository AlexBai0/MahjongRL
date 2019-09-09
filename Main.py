from utils.tenhouconnection import Connection
import gym
from QLearning import QLearning as QLe
import gym_mahjong.envs.mahjong_his_env

def play():
    env = gym.envs.make('Mahjong-v0')
    QL = QLe(env)
    connection = Connection(QL)
    connection.connect()
    auth = connection.authencate()
    print(auth)
    if auth:
        connection.play()
    else:
        connection.end()

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


    connection.connect()
    auth = connection.authencate()
    print(auth)
    if auth:
        connection.play()
    else:
        connection.end()



if __name__ == '__main__':
    play()
