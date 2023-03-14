from gym import Env
from gym import spaces
import numpy as np
from Games.agent_game4 import ArcadeGame, SCREEN_HEIGHT,SCREEN_WIDTH, COLUMN_COUNT

class CustomEnv(Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    num_envs = 1

    def __init__(self):
        # self.config = config 
        self.game = ArcadeGame()
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(
            shape= (SCREEN_WIDTH, SCREEN_HEIGHT, 3),low=0,high=255,dtype=np.uint8
        )
        self.episode_id = 0
        self.action_id = 0
        self.action_info = {}
        self.request_info = {}

        
    
    def step(self, action):
        reward, done, info = 0, False, {} 
        print(f"Action: {action}")
        
        self.game.position = action # teleport to slot
        self.game.update_spec_grid()
        reward, done, self.request_info = self.game.check_solution(self.game.position + 1)
        self.action_info = {'action_id': self.action_id, 'action': action, 'reward': reward}

        # self.render(mode='human')
        observation = self.game.draw_screen()
        self.action_id += 1
        
        # info for the monitor function
        info = {"request_info": self.request_info, "action_info": self.action_info}
        return observation, reward, done, info

    def reset(self):
        self.game.new_game()
        self.episode_id += 1
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