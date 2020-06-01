from gym.envs.registration import register
register(
    id='blocking-maze-v0',
    entry_point='gym_sutton_barto.envs:BlockingMaze',
)
register(
    id='cliff-walk-v0',
    entry_point='gym_sutton_barto.envs:CliffWalk',
)
register(
    id='dyna-maze-v0',
    entry_point='gym_sutton_barto.envs:DynaMaze',
)
register(
    id='shortcut-maze-v0',
    entry_point='gym_sutton_barto.envs:ShortcutMaze',
)