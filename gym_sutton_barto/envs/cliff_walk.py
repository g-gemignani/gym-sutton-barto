import gym
from gym import spaces


class CliffWalk(gym.Env):
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
    metadata = {'render.modes': ['human']}

    def __init__(self, rows=4, columns=12):
        self.actions = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        self.action_space = spaces.Discrete(4)
        self.cliff_states = [self.coord_to_state(3, y) for y in range(1, self.columns - 1)]
        self.columns = columns
        self.initial_state = self.coord_to_state(3, 0)
        self.num_actions = {value: key for key, value in self.actions.items()}
        self.rows = rows
        self.states = [x for x in range(self.rows * self.columns)]
        self.target_state = self.coord_to_state(3, 11)

        self.current_state = self.initial_state

    def coord_to_state(self, x, y):
        """
        :param x: row value
        :param y: column value
        :return: id of the equivalent state
        """
        return self.columns * x + y

    def render(self, mode='human'):
        border = "----" * self.columns + "-\n"
        board = border
        for i in range(0, self.rows * self.columns, self.columns):
            line = self.states[i:i + self.columns]
            for field in line:
                if field == self.current_state:
                    board += "| A "
                elif field in self.cliff_states:
                    board += "| X "
                elif field == self.target_state:
                    board += "| T "
                else:
                    board += "|   "
            board += "|\n"
            board += border
        print(board)

    def reset(self):
        """
        resets the environment
        """
        self.current_state = self.initial_state
        return self.current_state

    def state_to_coord(self, state):
        """
        :param state: input id of state in the env
        :return: (x, y) coord equivalent to the input state
        """
        return int(state / self.columns), state % self.columns

    def step(self, action):
        """
        returns next_state, reward, done
        """
        x, y = self.state_to_coord(self.current_state)
        if action == self.actions['up']:
            if x == 0:
                result = self.current_state, -1, False
            else:
                result = self.coord_to_state(x - 1, y), -1, False
        elif action == self.actions['right']:
            if x == self.rows - 1:
                result = self.initial_state, -100, False
            elif y == self.columns - 1:
                result = self.current_state, -1, False
            else:
                result = self.coord_to_state(x, y + 1), -1, False

        elif action == self.actions['left']:
            if y == 0:
                result = self.current_state, -1, False
            else:
                result = self.coord_to_state(x, y - 1), -1, False

        elif action == self.actions['down']:
            if x == 2:
                if y == 0:
                    result = self.current_state, -1, False
                elif y == self.columns - 1:
                    result = self.target_state, -1, True
                else:
                    result = self.initial_state, -100, False
            elif x == self.rows - 1:
                result = self.current_state, -1, False
            else:
                result = self.coord_to_state(x + 1, y), -1, False

        else:
            raise ValueError('Expected action value in {}, received {} in state {}'.
                             format(self.actions, action, self.state_to_coord(self.current_state)))

        self.current_state = result[0]
        return result
