from random import seed
from stable_baselines3.dqn.policies import CnnPolicy
from stable_baselines3.dqn.dqn import DQN
from wandb.integration.sb3 import WandbCallback
import wandb
import argparse
from datetime import datetime
import os
import pathlib
from config import current_dir, full_name, model_config
from envs.custom_env2 import CustomEnv as CustomEnv2
from envs.custom_env3 import CustomEnv as CustomEnv3


parse = False
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


config = model_config

if model_config["env"] == 2:
    env = CustomEnv2()
elif model_config["env"] == 3:
    env = CustomEnv3()
else:
    print("env not selected correctly in config.py")
    exit(1)

if parse:
    parser = setup_parser()

    # Get the hyperparameters
    args = parser.parse_args()

    args_config = {
        "number_of_slots": config.get("number_of_slots"),
        "screen_number_of_slots": config.get("screen_number_of_slots"),
        "solution_reward": config.get("solution_reward"),
        "rejection_reward": config.get("rejection_reward"),
        "left_reward": config.get("left_reward"),
        "right_reward": config.get("right_reward"),
        "seed": config.get("seed"),
        "end_limit": config.get("end_limit"),
        "K": config.get("K"),
        "buffer_size": int(args.buffer_size),
        "batch_size": int(args.batch_size),
        "exploration_final_eps": float(args.exploration_final_eps),
        "exploration_fraction": float(args.exploration_fraction),
        "gamma": float(args.gamma),
        "learning_rate": float(args.learning_rate),
        "learning_starts": int(args.learning_starts),
        "target_update_interval": int(args.target_update_interval),
        "train_freq": int(args.train_freq),
        "total_timesteps": int(args.total_timesteps),
    }

    config = args_config

wandb.init(
    project="EON",
#    entity="deepeon",
#    name=full_name,
    config=config,
    sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
)

model = DQN(
    CnnPolicy,
    env,
    verbose=1,
    tensorboard_log=os.path.join("tensorboardEON", wandb.run.name),
    learning_starts=config["learning_starts"],
    buffer_size=config["buffer_size"],
    batch_size=config["batch_size"],
    exploration_final_eps=config["exploration_final_eps"],
    exploration_fraction=config["exploration_fraction"],
    gamma=config["gamma"],
    learning_rate=config["learning_rate"],
    train_freq=config["train_freq"],
)


model.learn(
    total_timesteps=config["total_timesteps"],
    callback=WandbCallback(
        model_save_path=os.path.join(current_dir, "Models", full_name),
        verbose=2,
    ),
    tb_log_name=full_name,
    reset_num_timesteps=False,
)

wandb.run.finish()
env.close()