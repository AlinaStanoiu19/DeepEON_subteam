import os 
from random import seed
from stable_baselines3.dqn import CnnPolicy
from stable_baselines3 import DQN
from envs.custom_env3 import CustomEnv
# from stable_baselines.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor

game_config = {
  "solution_reward": 100,
  "rejection_reward": -10,
  "move_reward": -1,
  "left_reward": 0,
  "right_reward": 0,
  "seed": 0
}

# implement custom callback function
# class ExplainabilityCallback(BaseCallback):
#     """
#     A custom callback that derives from ``BaseCallback``.
#     :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
#     """

#     def __init__(self,log_dir: str, verbose=0):
#         super(ExplainabilityCallback, self).__init__(verbose)
#         self.log_dir = log_dir

#     def _init_callback(self) -> None: 
#         pass

#     def _on_training_start(self) -> None:
#         """
#         This method is called before the first rollout starts.
#         """
#         pass

#     def _on_rollout_start(self) -> None:
#         """
#         A rollout is the collection of environment interaction
#         using the current policy.
#         This event is triggered before collecting new samples.
#         """
#         pass

#     def _on_step(self) -> bool:
#         """
#         This method will be called by the model after each call to `env.step()`.
#         :return: (bool) If the callback returns False, training is aborted early.
#         """

#         return True

#     def _on_rollout_end(self) -> None:
#         """
#         This event is triggered before updating the policy.
#         """
#         pass

#     def _on_training_end(self) -> None:
#         """
#         This event is triggered before exiting the `learn()` method.
#         """
#         pass

# create log directory
log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)

# create and wrap(monitor) the environment
info_keywords  = ('episode_actions', 'episode_rewards')
env = CustomEnv(game_config)
env = Monitor(env, log_dir, info_keywords = info_keywords )

# initiate the agent 
model = DQN(CnnPolicy, env,  verbose=1, buffer_size = 5000)

# create the callack with checking frequency 
# callback = ExplainabilityCallback(log_dir=log_dir)

# train the agent 
time_steps = 100
model.learn(total_timesteps=int(time_steps))
# model.learn(total_timesteps=int(time_steps), callback=callback)

# save the trained agent 
model.save("Models/model_ucl05")