import pygame
from stable_baselines3 import DQN
from envs.custom_env2 import CustomEnv
import cv2

SCREEN_WIDTH = 920
SCREEN_HEIGHT = 150


def record():
    print("saving..")
    height, width, layers = frame_array[0].shape
    out = cv2.VideoWriter('video2.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 20, (width,height))
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()
        


game_config = {
  "solution_reward": 10,
  "rejection_reward": -10,
  "move_reward": -1,
  "left_reward": 0,
  "right_reward": 0,
  "seed": 0
}


env = CustomEnv(game_config)

model = DQN.load("Models/pleasant-lion-1/model.zip")
print("loaded")

env.highscore = 0
frame_array = []
episodes = 0
while episodes < 10:
    episodes += 1
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        frame = env.render(mode='rgb_array')
        frame_array.append(frame)
        
record()
env.close()
    
