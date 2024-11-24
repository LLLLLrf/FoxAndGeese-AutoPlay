import numpy as np
import gym
from gym import spaces

class FoxAndGeeseEnv(gym.Env):
    def __init__(self):
        super(FoxAndGeeseEnv, self).__init__()
        self.grid_size = 7
        self.action_space = gym.spaces.Discrete(4)  # Up, Down, Left, Right
        self.observation_space = gym.spaces.Box(
            low=0, high=2, shape=(self.grid_size, self.grid_size), dtype=np.int32
        )
        self.seed()

    def seed(self, seed=None):
        self.np_random = np.random.default_rng(seed)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.seed(seed)

        # Reset positions: Fox = 2, Geese = 1
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.fox_position = [0, 0]  # Ensure fox position is a list
        self.geese_positions = [[3, 2], [3, 3], [4, 2], [4, 3], [5, 2], [5, 3]]
        
        # Update grid
        self.grid[tuple(self.fox_position)] = 2
        for pos in self.geese_positions:
            self.grid[tuple(pos)] = 1

        self.done = False
        self.steps = 0
        return self.grid, {}

    def step(self, action):
        # Define movement deltas for actions (up, down, left, right)
        delta = {
            0: (-1, 0),  # up
            1: (1, 0),   # down
            2: (0, -1),  # left
            3: (0, 1)    # right
        }

        # Calculate new position
        new_pos = [self.fox_position[0] + delta[action][0],
                   self.fox_position[1] + delta[action][1]]

        # Ensure new position is within grid boundaries
        if 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size:
            # Update position
            self.grid[tuple(self.fox_position)] = 0  # Clear old position
            self.fox_position = new_pos  # Update fox position to list
            self.grid[tuple(self.fox_position)] = 2  # Mark new position

            # Check if the fox captures a goose
            if self.fox_position in self.geese_positions:
                self.geese_positions.remove(self.fox_position)  # Remove the goose
                reward = 10  # Reward for capturing a goose
            else:
                reward = -1  # Penalty for a regular move
        else:
            reward = -5  # Penalty for trying to move out of bounds

        # Check game-over conditions
        terminated = len(self.geese_positions) == 0  # All geese captured
        truncated = self.steps >= 100  # Example step limit

        self.steps += 1

        return self.grid, reward, terminated, truncated, {}

    def render(self):
        print("\n".join([" ".join(map(str, row)) for row in self.grid]))
        print("\n")
