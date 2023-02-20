from random import seed
from stable_baselines3.dqn import CnnPolicy
from stable_baselines3 import DQN
from envs.custom_env import CustomEnv
from wandb.integration.sb3 import WandbCallback
import wandb
import argparse

parse = True
# Build your ArgumentParser however you like
def setup_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument("--buffer_size")
  parser.add_argument("--batch_size")
  parser.add_argument("--exploration_final_eps")
  parser.add_argument("--exploration_fraction")
  parser.add_argument("--gamma")
  parser.add_argument("--learning_rate")
  parser.add_argument("--learning_starts")
  parser.add_argument("--target_update_interval")
  parser.add_argument("--train_freq")
  parser.add_argument("--total_timesteps")
  return parser


model_config = {
  "buffer_size":10000, 
  "batch_size":32,
  "exploration_final_eps":0.1,
  "exploration_fraction":0.5,
  "gamma":0.999,
  "learning_rate":0.00025,
  "learning_starts":50000,
  "target_update_interval":10000,
  "train_freq":4,
  "total_timesteps":500000
}

config = model_config

if parse:
  parser = setup_parser()
  
  # Get the hyperparameters
  args = parser.parse_args()
  
  args_config = {
    "buffer_size":int(args.buffer_size), 
    "batch_size":int(args.batch_size),
    "exploration_final_eps":float(args.exploration_final_eps),
    "exploration_fraction":float(args.exploration_fraction),
    "gamma":float(args.gamma),
    "learning_rate":float(args.learning_rate),
    "learning_starts":int(args.learning_starts),
    "target_update_interval":int(args.target_update_interval),
    "train_freq":int(args.train_freq),
    "total_timesteps":int(args.total_timesteps)
  }
  
  config = args_config

game_config = {
  "solution_reward": 10,
  "rejection_reward": -10,
  "left_reward": 0,
  "right_reward": 0,
  "seed": 0
}

run = wandb.init(
  project = "EON",
  config=config,
  sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
)

env = CustomEnv(game_config)

model = DQN(CnnPolicy, 
            env, verbose=1, 
            tensorboard_log=f"./tensorboardEON/{run.id}", 
            learning_starts=config["learning_starts"],
            buffer_size=config["buffer_size"],
            batch_size=config["batch_size"],
            exploration_final_eps=config["exploration_final_eps"],
            exploration_fraction=config["exploration_fraction"],
            gamma=config["gamma"],
            learning_rate=config["learning_rate"],
            train_freq=config["train_freq"]
)

model.learn(total_timesteps=config["total_timesteps"], 
            callback=WandbCallback(model_save_path = f"Models/{run.name}",
            verbose = 2,),
            )
run.finish()
env.close()

