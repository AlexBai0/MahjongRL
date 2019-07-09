from gym.envs.registration import register

register(
    id='mahjong-v0',
    entry_point='gym_mahjong.envs:MahjongEnv',
)