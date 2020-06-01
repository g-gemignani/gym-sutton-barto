from collections import Iterable

from gym import spaces, Env


class GridWorld(Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, rows, columns):
        # action definition
        self.actions = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        self.action_space = spaces.Discrete(4)
        self.num_actions = {value: key for key, value in self.actions.items()}

        # grid definition
        self.columns = columns
        self.rows = rows
        self.states = [x for x in range(rows * columns)]

        # set initial, target and current states
        self.current_state = None
        self.goal_states = []
        self.initial_state = None

        self._states_repr = {'S': 'current_state',
                             'G': 'goal_states'}

    def coord_to_state(self, x, y):
        """
        :param x: row value
        :param y: column value
        :return: id of the equivalent state
        """
        return self.columns * x + y

    def register_state_representation(self, state_repr, states):
        self._states_repr[state_repr] = states

    def render(self, mode='human'):
        border = "----" * self.columns + "-\n"
        board = border
        for i in range(0, self.rows * self.columns, self.columns):
            line = self.states[i:i + self.columns]
            for field in line:
                cell_occupied = False
                for state_repr, states in self._states_repr.items():
                    states = self.__getattribute__(states)
                    if not isinstance(states, Iterable):
                        states = [states]
                    if field in states:
                        board += "| {} ".format(state_repr)
                        cell_occupied = True
                        # a cell can be occupied only by a single entity
                        break
                if not cell_occupied:
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
        raise NotImplemented
