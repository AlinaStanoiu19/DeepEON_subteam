from random import seed
from stable_baselines3.dqn import CnnPolicy
from stable_baselines3 import DQN
from envs.custom_env import CustomEnv
from wandb.integration.sb3 import WandbCallback
import wandb
import argparse


game_config = {
  "solution_reward": 10,
  "rejection_reward": -10,
  "move_reward": -1,
  "left_reward": 2,
  "right_reward": 2,
  "seed": 0
}


# print("model loaded")
#parms = model.get_parameters()

#run = wandb.init(
#  project = "test2")#,
#  #config = parms)#,
#  sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
#)

env = CustomEnv(game_config)
model = DQN(CnnPolicy, env,  verbose=1, buffer_size = 5000)
model.learn(total_timesteps = 1000)
model.save("Models/model1")