from gym import Env
from gym import spaces
import numpy as np
from Games.agent_game3 import ArcadeGame, SCREEN_HEIGHT,SCREEN_WIDTH, COLUMN_COUNT

class CustomEnv(Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    num_envs = 1

    def __init__(self):
        # self.config = config 
        self.game = ArcadeGame()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(shape= (SCREEN_WIDTH, SCREEN_HEIGHT, 3),low=0,high=255,dtype=np.uint8)
        self.episode_id = 0
        self.action_id = 0
        self.action_info = {}
        self.request_info = {}
    
    def step(self, action):
        reward, done, info = 0, False, {} 
        
        if action == 0 and self.game.position < (COLUMN_COUNT)-1: # RIGHT
            print("Move RIGHT")
            self.game.position +=1
            self.game.update_spec_grid()
            reward = 0
            info = {"action_info": self.action_info}
        elif action == 1 and self.game.position > 0: #LEFT
            print("Move LEFT")
            self.game.position -=1
            self.game.update_spec_grid()
            reward = 0
            info = {"action_info": self.action_info}
        elif action == 2: # ENTER
            print("ENTER")
            reward, done, self.request_info = self.game.check_solution(self.game.position + 1) # implement this function
            

        print(f"Number of blocks: {self.game.blocks} Score: {self.game.score} High Score: {self.game.highscore}")

        # info for monitor
        self.action_info = {'action_id': self.action_id, 'action': action, 'reward': reward}
        info = {"request_info": self.request_info, "action_info": self.action_info}
        
        observation = self.game.draw_screen()
        self.action_id += 1
        
        return observation, reward, done, info

    def reset(self):
        self.game.new_game()
        print("--- NEW GAME ---")
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