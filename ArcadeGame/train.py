from random import seed
from stable_baselines3.dqn.policies import CnnPolicy
from stable_baselines3.dqn.dqn import DQN
from stable_baselines3.common.evaluation import evaluate_policy
from wandb.integration.sb3 import WandbCallback
import wandb
import argparse
from datetime import datetime
import os
import pathlib
from config import current_dir, full_name, model_config
from envs.custom_env2 import CustomEnv as CustomEnv2
from envs.custom_env3 import CustomEnv as CustomEnv3
import yaml
import numpy as np

epochs = 1

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
        "total_timesteps": config.get("total_timesteps"),
    }

    config = args_config

def main():

    with open("sweep.yaml", "r") as stream:
        try:
            sweep_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    wandb.init(
        project="EON",
        config=config,
        sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
    )
    
    learning_rate  =  wandb.config.learning_rate
    batch_size = wandb.config.batch_size
    gamma = wandb.config.gamma
    buffer_size = wandb.config.buffer_size
    exploration_fraction = wandb.config.exploration_fraction
    exploration_final_eps = wandb.config.exploration_final_eps
    target_update_interval = wandb.config.target_update_interval
    learning_starts = wandb.config.learning_starts
    train_freq = wandb.config.train_freq

    for epoch in np.arange(1, epochs):
        model = DQN(
            CnnPolicy,
            env,
            verbose=1,
            tensorboard_log=os.path.join("tensorboardEON", wandb.run.name),
            learning_starts=learning_starts,
            buffer_size=buffer_size,
            batch_size=batch_size,
            exploration_final_eps=exploration_final_eps,
            exploration_fraction=exploration_fraction,
            target_update_interval=target_update_interval,
            gamma=gamma,
            learning_rate=learning_rate,
            train_freq=train_freq,
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
        mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

        wandb.log({
            'epoch': epoch, 
            'mean_reward': mean_reward,
            'std_reward': std_reward, 
        })

main()
#sweep_id = wandb.sweep(sweep=sweep_data, project='my-first-sweep')
##wandb.agent(sweep_id, function=main, count=4)
# wandb.run.finish()
# env.close()