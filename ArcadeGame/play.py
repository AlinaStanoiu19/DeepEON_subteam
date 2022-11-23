import pygame
from stable_baselines3 import DQN
from envs.custom_env import CustomEnv

game_config = {
  "solution_reward": 10,
  "rejection_reward": -10,
  "move_reward": -1,
  "left_reward": 2,
  "right_reward": 2,
  "seed": 0
}

env = CustomEnv(game_config)

model = DQN.load("Models/model_ucl1")
print("loaded")

env.highscore = 0

while True:
    
    obs = env.reset()
    done = False

    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            env.close()
    
