from gym_sutton_barto.envs.dyna_maze import DynaMaze


class BlockingMaze(DynaMaze):
    """
      World:
      - for rc < reset_change:
         0 1 2 3 4 5 6 7 8
      0 | | | | | | | | |G|
      1 | | | | | | | | | |
      2 | | | | | | | | | |
      3 | | | | | | | | | |
      4 |-|-|-|-|-|-|-|-| |
      5 | | | |S| | | | | |
      - otherwise:
         0 1 2 3 4 5 6 7 8
      0 | | | | | | | | |G|
      1 | | | | | | | | | |
      2 | | | | | | | | | |
      3 | | | | | | | | | |
      4 | |-|-|-|-|-|-|-|-|
      5 | | | |S| | | | | |
      Actions:
      0 = up, 1 = right, 2 = down, 3 = left
      """
    def __init__(self, goal_reward=100, step_reward=-1, reset_change=1000):
        self.n_resets = 0
        self.reset_change = reset_change

        super(BlockingMaze, self).__init__()
        self.block_states = [self.coord_to_state(4, y) for y in range(self.columns-1)]
        self.goal_reward = goal_reward
        self.goal_states = [self.coord_to_state(0, 8)]
        self.initial_state = self.coord_to_state(5, 3)
        self.step_reward = step_reward
        self.register_state_representation('-', 'block_states')
        self.reset()

    def reset(self):
        self.n_resets += 1
        if self.n_resets == self.reset_change:
            self.block_states = [self.coord_to_state(4, y) for y in range(1, self.columns)]
        return super(BlockingMaze, self).reset()
