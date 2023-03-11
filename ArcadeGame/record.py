import pygame
from stable_baselines3 import DQN
from envs.custom_env2 import CustomEnv as CustomEnv2
from envs.custom_env3 import CustomEnv as CustomEnv3
from envs.custom_env4 import CustomEnv as CustomEnv4
import cv2
import os
from config import current_dir, full_name, all_configs


SCREEN_HEIGHT = all_configs["height"]
SCREEN_WIDTH = all_configs["width"]

if all_configs["env"] == 2:
    env = CustomEnv2()
elif all_configs["env"] == 3:
    env = CustomEnv3()
elif all_configs["env"] == 4:
    env = CustomEnv4()
else:
    print("env not selected correctly in config.py")
    exit(1)


def record():
    print("saving..")
    height, width, layers = frame_array[0].shape
    out = cv2.VideoWriter(
        os.path.join(current_dir, "Recordings", f"video_{full_name}.mp4"),
        cv2.VideoWriter_fourcc(*"mp4v"),
        20,
        (width, height),
    )
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()


model = DQN.load(os.path.join(current_dir, "Models", f"{full_name}", "model"))
print("model loaded")

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
        frame = env.render(mode="rgb_array")
        frame_array.append(frame)

record()
env.close()