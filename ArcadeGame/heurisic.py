from datetime import datetime
import pygame
from stable_baselines3 import DQN
from envs.custom_env import CustomEnv
from Games.game5 import ArcadeGame
import numpy as np
import pandas as pd
import datetime as dt
import os
 
K = 5
episode_count_targets = 10
game_config = {
  "solution_reward": 10,
  "rejection_reward": -10,
  "left_reward": 0,
  "right_reward": 0,
  "seed": 1
}
 
game = ArcadeGame(game_config)
episode_count = 0
episode_rewards = []
while episode_count < episode_count_targets:
    episode_reward = 0
    fs = 0
    done = False
    game.new_game()
    game.draw_screen()
    game.render()
    while not done:
        solution = False
        for k in range(K):
            for i in range(8-game.slots):
                first_slot = k*9 + i
                if game.is_solution(first_slot=first_slot):
                    solution = True
                    fs = first_slot
                    break
            if solution:
                break

        game.first_slot = fs
        game.update_spec_grid()
        game.draw_screen()
        game.render()
        reward, done = game.check_solution()
        episode_reward += reward
        print(episode_reward)
    
    episode_rewards.append(episode_reward)
    episode_count += 1
    
    
mean_reward = np.mean(episode_rewards)
std_reward = np.std(episode_rewards)
print(mean_reward)
index = np.arange(0,episode_count_targets)
df = pd.DataFrame({"index":index,"Episode Rewards":np.array(episode_rewards)})
time = dt.datetime 

if not os.path.exists("./Evaluation data"):
    os.makedirs("./Evaluation data")
df.to_json("./Evaluation data/evaluation_huristic_2.json")
    