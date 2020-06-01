from gym_sutton_barto.envs.grid_world import GridWorld


class CliffWalk(GridWorld):
    """
      World:
         0 1 2 3 4 5 6 7 8 9 10 11
      0 | | | | | | | | | | | | |
      1 | | | | | | | | | | | | |
      2 | | | | | | | | | | | | |
      3 |S|C|C|C|C|C|C|C|C|C|C|G|
      Actions:
      0 = up, 1 = right, 2 = down, 3 = left
      """
    def __init__(self, cliff_reward=-100, goal_reward=-1, step_reward=-1):
        super(CliffWalk, self).__init__(rows=4, columns=11)
        self.cliff_reward = cliff_reward
        self.cliff_states = [self.coord_to_state(3, y) for y in range(1, self.columns - 1)]
        self.goal_reward = goal_reward
        self.goal_states = [self.coord_to_state(self.rows - 1, self.columns - 1)]
        self.initial_state = self.coord_to_state(3, 0)
        self.step_reward = step_reward
        self.register_state_representation('C', 'cliff_states')
        self.reset()

    def step(self, action):
        """
        returns next_state, reward, done
        """
        x, y = self.state_to_coord(self.current_state)
        if action == self.actions['up']:
            possible_next_state = self.coord_to_state(x - 1, y)
            if x - 1 < 0:
                result = self.current_state, self.step_reward, False
            else:
                result = possible_next_state, self.step_reward, False
        elif action == self.actions['right']:
            possible_next_state = self.coord_to_state(x, y + 1)
            if y + 1 >= self.columns:
                result = self.current_state, self.step_reward, False
            elif possible_next_state in self.cliff_states:
                result = self.initial_state, self.cliff_reward, False
            else:
                result = possible_next_state, self.step_reward, False

        elif action == self.actions['left']:
            possible_next_state = self.coord_to_state(x, y - 1)
            if y - 1 < 0:
                result = self.current_state, self.step_reward, False
            else:
                result = possible_next_state, self.step_reward, False

        elif action == self.actions['down']:
            possible_next_state = self.coord_to_state(x + 1, y)
            if x + 1 >= self.rows:
                result = self.current_state, self.step_reward, False
            elif possible_next_state in self.cliff_states:
                result = self.initial_state, self.cliff_reward, False
            elif possible_next_state in self.goal_states:
                result = possible_next_state, self.goal_reward, True
            else:
                result = possible_next_state, self.step_reward, False

        else:
            raise ValueError('Expected action value in {}, received {} in state {}'.
                             format(self.actions, action, self.state_to_coord(self.current_state)))

        self.current_state = result[0]
        return result
