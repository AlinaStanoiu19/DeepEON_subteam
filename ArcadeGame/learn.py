from random import seed
from stable_baselines3.dqn import CnnPolicy
from stable_baselines3 import DQN
from envs.custom_env3 import CustomEnv as CustomEnv3
from wandb.integration.sb3 import WandbCallback
import wandb
import argparse



env = CustomEnv3()
model = DQN(CnnPolicy, env,  verbose=1, buffer_size = 5000)
model.learn(total_timesteps = 100)
