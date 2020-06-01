from gym.envs.registration import register

register(
    id='cliff-walk-v0',
    entry_point='gym_sutton_barto.envs:CliffWalk',
)
