from gym.envs.registration import register


register(
    id='Mahjong-v0',
    entry_point='gym_mahjong.envs:MahjongEnv'
)