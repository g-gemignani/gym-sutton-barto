from gym_sutton_barto.envs.grid_world import GridWorld


class DynaMaze(GridWorld):
    """
      World:
         0 1 2 3 4 5 6 7 8
      0 | | | | | | | |-|G|
      1 | |-| | | | | |-| |
      2 |S|-| | | | | |-| |
      3 | |-| | | | | | | |
      4 | | | | | |-| | | |
      5 | | | | | | | | | |
      Actions:
      0 = up, 1 = right, 2 = down, 3 = left
      """
    def __init__(self, goal_reward=1, step_reward=0):
        super(DynaMaze, self).__init__(rows=6, columns=9)
        self.block_states = [self.coord_to_state(1, 1), self.coord_to_state(2, 1), self.coord_to_state(3, 1),
                             self.coord_to_state(4, 5), self.coord_to_state(0, 7), self.coord_to_state(1, 7),
                             self.coord_to_state(2, 7)]
        self.goal_reward = goal_reward
        self.goal_states = [self.coord_to_state(0, 8)]
        self.initial_state = self.coord_to_state(2, 0)
        self.step_reward = step_reward
        self.register_state_representation('-', 'block_states')
        self.reset()

    def step(self, action):
        """
        returns next_state, reward, done
        """
        x, y = self.state_to_coord(self.current_state)
        if action == self.actions['up']:
            possible_next_state = self.coord_to_state(x - 1, y)
            if x - 1 < 0 or possible_next_state in self.block_states:
                result = self.current_state, self.step_reward, False
            elif possible_next_state in self.goal_states:
                result = possible_next_state, self.goal_reward, True
            else:
                result = possible_next_state, self.step_reward, False
        elif action == self.actions['right']:
            possible_next_state = self.coord_to_state(x, y + 1)
            if y + 1 >= self.columns or possible_next_state in self.block_states:
                result = self.current_state, self.step_reward, False
            else:
                result = possible_next_state, self.step_reward, False

        elif action == self.actions['left']:
            possible_next_state = self.coord_to_state(x, y - 1)
            if y - 1 < 0 or possible_next_state in self.block_states:
                result = self.current_state, self.step_reward, False
            else:
                result = possible_next_state, self.step_reward, False

        elif action == self.actions['down']:
            possible_next_state = self.coord_to_state(x + 1, y)
            if x + 1 >= self.rows or possible_next_state in self.block_states:
                result = self.current_state, self.step_reward, False
            else:
                result = possible_next_state, self.step_reward, False

        else:
            raise ValueError('Expected action value in {}, received {} in state {}'.
                             format(self.actions, action, self.state_to_coord(self.current_state)))

        self.current_state = result[0]
        return result
