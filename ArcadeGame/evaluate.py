from stable_baselines3.common import base_class
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import DQN
from envs.custom_env3 import CustomEnv
import numpy as np
import gym
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd





def evaluate(
    model: "base_class.BaseAlgorithm",
    env: gym.Env,
    n_eval_episodes: int = 1000,
    deterministic: bool = False,
    render: bool = False,
):
    print("Starting..")
    episode_count = 0
    episode_rewards = []
    episode_lengths = []
    while episode_count < n_eval_episodes:
        current_reward = 0
        current_length = 0
        done = False
        observation = env.reset()
        while not done:
            action, state= model.predict(observation, deterministic=deterministic)
            observation, reward, done, info = env.step(action)
            current_reward += reward
            current_length += 1
            if render:
                env.render()
    
        episode_rewards.append(current_reward)
        episode_lengths.append(current_length)
        episode_count += 1
        
        if render:
            env.render()
        else:
            print(episode_count)
    
    return episode_rewards, episode_lengths


n_episodes = 1000
game_config = {
  "solution_reward": 10,
  "rejection_reward": -10,
  "move_reward": -1,
  "left_reward": 0,
  "right_reward": 0,
  "seed": 0
}
env = CustomEnv(game_config)
env.seed(0)
kwargs = {"policy_kwargs":{"replay_buffer_kwargs":True}}
model = DQN.load("Models/curious-hill-22/model",kwargs=kwargs)
print("Loaded")
model.set_env(env)
episode_rewards, episode_lengths = evaluate(model,env,n_episodes,render=False)
index = np.arange(0,n_episodes)
df = pd.DataFrame({"index":index,"Episode Rewards":np.array(episode_rewards), "Episode Lengths": np.array(episode_lengths)})
df.to_json("Evaluation_data/curious-hill-22.json")