from gym import Env
from gym import spaces
import numpy as np
from Games.agent_game2 import ArcadeGame, SCREEN_HEIGHT,SCREEN_WIDTH, COLUMN_COUNT

class CustomEnv(Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    num_envs = 1
    def __init__(self, config):
        self.config = config 
        self.game = ArcadeGame(self.config)
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(shape= (SCREEN_WIDTH, SCREEN_HEIGHT, 3),low=0,high=255,dtype=np.uint8)
    
    def step(self, action):
        reward, done, info = 0, False, {} 
        print(f"Action: {action}")
        if action == 0: 
            self.game.first_slot = 0 # teleport to slot
            self.game.update_spec_grid()
            reward, done = self.game.check_solution(self.game.position + 1)
        elif action == 1: 
            self.game.first_slot = 1 # teleport to slot
            self.game.update_spec_grid()
            reward, done = self.game.check_solution(self.game.position + 1)
        elif action == 2: 
            self.game.first_slot = 2 # teleport to slot
            self.game.update_spec_grid()
            reward, done = self.game.check_solution(self.game.position + 1)
        elif action == 3: 
            self.game.first_slot = 3 # teleport to slot
            self.game.update_spec_grid()
            reward, done = self.game.check_solution(self.game.position + 1)
        elif action == 4: 
            self.game.first_slot = 4 # teleport to slot
            self.game.update_spec_grid()
            reward, done = self.game.check_solution(self.game.position + 1)
        elif action == 5: 
            self.game.first_slot = 5 # teleport to slot
            self.game.update_spec_grid()
            reward, done = self.game.check_solution(self.game.position + 1)
            
        observation = self.game.draw_screen()

        return observation, reward, done, info

    def reset(self):
        self.game.new_game()
        observation = self.game.draw_screen()
        return observation 

    def render(self, mode='human'):
        if mode == 'rgb_array':
            return self.game.draw_screen() # return RGB frame suitable for video
        elif mode == 'human':
            self.game.render() # pop up a window and render
        else:
            super(CustomEnv, self).render(mode=mode) # just raise an exceptionset
        
    def close (self):
        self.game.exit()