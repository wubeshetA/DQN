import gym
import numpy as np
from gym import spaces

class HospitalNavigationEnv(gym.Env):
    def __init__(self):
        super(HospitalNavigationEnv, self).__init__()
        
        # Define the size of the grid
        self.grid_size = 5
        
        # Define action and observation space
        self.action_space = spaces.Discrete(4)  # Up, Down, Left, Right
        self.observation_space = spaces.Box(low=0, high=5, shape=(self.grid_size, self.grid_size), dtype=np.float32)
        
        # Define positions of static objects
        self.medicine_cabinet = (4, 4)
        self.beds = [(0, 1), (2, 1), (4, 1), (1, 3), (3, 3)]
        self.doctor = (3, 2)
        self.nurse = (3, 2)
    
        # Initialize agent position
        self.agent_pos = None
        
        # Set maximum steps
        self.max_steps = 100
        self.current_step = 0

    def reset(self):
        # Reset agent to a random position
        self.agent_pos = (np.random.randint(0, self.grid_size), np.random.randint(0, self.grid_size))
        self.current_step = 0
        return self._get_observation()

    def step(self, action):
        self.current_step += 1
        
        # Move agent based on action
        if action == 0:  # Up
            self.agent_pos = (max(0, self.agent_pos[0] - 1), self.agent_pos[1])
        elif action == 1:  # Down
            self.agent_pos = (min(self.grid_size - 1, self.agent_pos[0] + 1), self.agent_pos[1])
        elif action == 2:  # Left
            self.agent_pos = (self.agent_pos[0], max(0, self.agent_pos[1] - 1))
        elif action == 3:  # Right
            self.agent_pos = (self.agent_pos[0], min(self.grid_size - 1, self.agent_pos[1] + 1))
        
        # Check for termination conditions
        done = False
        reward = -0.1  # Small negative reward for each step
        
        if self.agent_pos == self.medicine_cabinet:
            reward = 10
            done = True
        elif self.agent_pos in [self.doctor, self.nurse]:
            reward = -5
            done = True
        elif self.agent_pos in self.beds:
            reward += 1
        elif self.current_step >= self.max_steps:
            done = True
        
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        obs = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        obs[self.agent_pos] = 1
        obs[self.medicine_cabinet] = 2
        for bed in self.beds:
            obs[bed] = 3
        obs[self.doctor] = 4
        obs[self.nurse] = 5
        return obs

    def render(self, mode='human'):
        if mode == 'human':
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if (i, j) == self.agent_pos:
                        print('🙂', end=' ')
                    elif (i, j) == self.medicine_cabinet:
                        print('💊', end=' ')
                    elif (i, j) in self.beds:
                        print('🛏️', end=' ')
                    elif (i, j) == self.doctor:
                        print('👨‍⚕️', end=' ')
                    elif (i, j) == self.nurse:
                        print('👩‍⚕️', end=' ')
                    else:
                        print('.', end=' ')
                print()
            print('\n')