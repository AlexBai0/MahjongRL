from gym.envs.registration import register

register(
    id='    ',
    entry_point='gym_mahjong.envs:MahjongEnv',
    kwargs = {'opponent' : 'random'},
)