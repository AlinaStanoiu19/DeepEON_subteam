import os 
import pandas as pd
from random import seed
from stable_baselines3.dqn import CnnPolicy
from stable_baselines3 import DQN
from envs.custom_env4 import CustomEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from csv import DictWriter

game_config = {
  "solution_reward": 100,
  "rejection_reward": -10,
  "move_reward": -1,
  "left_reward": 0,
  "right_reward": 0,
  "seed": 0
}


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

# create and wrap(monitor) the environment
info_keywords  = ("request_info","action_info")
env = CustomEnv()
env = Monitor(env, log_dir, info_keywords = info_keywords )

# initiate the agent 
model = DQN(CnnPolicy, env,  verbose=1, buffer_size = 5000)

# create the callack with checking frequency 
callback = ExplainabilityCallback(log_dir=log_dir)

# train the agent 
time_steps = 15
# model.learn(total_timesteps=int(time_steps))
model.learn(total_timesteps=int(time_steps), callback=callback)

# save the trained agent 
model.save("Models/model_ucl05")