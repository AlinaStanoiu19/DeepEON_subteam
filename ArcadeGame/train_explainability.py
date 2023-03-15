import os 
import pandas as pd
from random import seed
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.dqn.policies import CnnPolicy
from stable_baselines3.dqn.dqn import DQN
from wandb.integration.sb3 import WandbCallback
from csv import DictWriter

from random import seed
import wandb
import argparse
from datetime import datetime
import pathlib
from config import current_dir, full_name, model_config
from envs.custom_env2 import CustomEnv as CustomEnv2
from envs.custom_env3 import CustomEnv as CustomEnv3
from envs.custom_env4 import CustomEnv as CustomEnv4


# # implement custom callback function
class ExplainabilityCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.
    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """

    def __init__(self,log_dir: str, verbose=1):
        super(ExplainabilityCallback, self).__init__(verbose)
        self.log_dir = log_dir
        self.verbose = verbose
        self.env = env 
        self.model = DQN(CnnPolicy, env,  verbose=1, buffer_size = 5000)

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.
        :return: (bool) If the callback returns False, training is aborted early.
        """
        columns = ['episode_id', 'request_id', 'action_id', 'request', 'action', 'reward']
        new_data = {'episode_id': self.env.episode_id,
                    'request_id': self.env.request_info['id'],
                    'action_id': self.env.action_info['action_id'],
                    'request': (self.env.request_info['source'], self.env.request_info['target'],self.env.request_info['slots']),
                    'action': self.env.action_info['action'],
                    'reward': self.env.action_info['reward']}
        
        # Open CSV file in append mode
        # Create a file object for this file
        with open(log_dir+'callback_data.csv', 'a', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=columns)
            dictwriter_object.writerow(new_data)
            f_object.close()

        return True

# create log directory
log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)
columns = ['episode_id', 'request_id', 'action_id', 'request', 'action', 'reward']
df = pd.DataFrame(columns=columns)
df.to_csv(log_dir+'callback_data.csv', index=False)

#-------------------------------------------------------------------------------

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

# create and wrap(monitor) the environment
info_keywords  = ("request_info","action_info")

if model_config["env"] == 2:
    env = CustomEnv2()
    env = Monitor(env, log_dir, info_keywords = info_keywords )
elif model_config["env"] == 3:
    env = CustomEnv3()
    env = Monitor(env, log_dir, info_keywords = info_keywords )
elif model_config["env"] == 4:
    env = CustomEnv4()
    env = Monitor(env, log_dir, info_keywords = info_keywords )
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
    dir=None
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


# create the callack 
callback = ExplainabilityCallback(log_dir=log_dir)

# use this only for hyperparameter tunning
callback_tunning = WandbCallback(
        model_save_path=os.path.join(current_dir, "Models", full_name),
        verbose=2,
    )

model.learn(
    total_timesteps=config["total_timesteps"],
    callback=callback,
    tb_log_name=full_name,
    reset_num_timesteps=False,
)

wandb.run.finish()
env.close()