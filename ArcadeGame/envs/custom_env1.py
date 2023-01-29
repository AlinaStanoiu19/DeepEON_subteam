from gym import Env
from gym import spaces
import numpy as np
from Games.agent_game1 import ArcadeGame, SCREEN_HEIGHT, SCREEN_WIDTH, COLUMN_COUNT

class CustomEnv(Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    num_envs = 1
    def __init__(self, config):
        self.config = config 
        self.game = ArcadeGame(self.config)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(shape= (SCREEN_WIDTH, SCREEN_HEIGHT, 3),low=0,high=255,dtype=np.uint8)
        
    def step(self, action):
        reward, done, info = 0, False, {} 

        if action == 0 and self.game.position < (COLUMN_COUNT)-1: # RIGHT
            print("Move RIGHT")
            self.game.position +=1
            self.game.update_spec_grid()
            reward = self.config["right_reward"]
        elif action == 1 and self.game.position > 0: #LEFT
            print("Move LEFT")
            self.game.position -=1
            self.game.update_spec_grid()
            reward = self.config["left_reward"]
        elif action == 2: # ENTER
            print("ENTER")
            reward, done = self.game.check_node()

        print(f"Number of blocks: {self.game.blocks} Score: {self.game.score} High Score: {self.game.highscore}")
           
        observation = self.game.draw_screen()

        return observation, reward, done, info

    def reset(self):
        if self.game.score == "CHANGE" or self.game.blocks == 4:
            self.game.new_game()
        else:
            self.game.new_round()
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
        
    