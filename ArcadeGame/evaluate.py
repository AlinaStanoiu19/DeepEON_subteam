from stable_baselines3.common import base_class
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.dqn.dqn import DQN
import numpy as np
import gym
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd
from config2 import current_dir, all_configs, full_name, model_config
from envs.custom_env2 import CustomEnv as CustomEnv2
from envs.custom_env3 import CustomEnv as CustomEnv3
import os

NUMBER_OF_EPISODES_EVALUATED = all_configs["number_of_episodes_evaluated"]
NUMBER_OF_SLOTS_EVALUATED = all_configs["number_of_slots_evaluated"]

def evaluate(
    model: "base_class.BaseAlgorithm",
    env: gym.Env,
    n_eval_episodes: int = NUMBER_OF_EPISODES_EVALUATED,
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
            action, state = model.predict(observation, deterministic=deterministic)
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


if all_configs["env"] == 2:
    env = CustomEnv2()
elif all_configs["env"] == 3:
    env = CustomEnv3()
else:
    print("env not selected correctly in config.py")
    exit(1)


env.seed(all_configs["seed"])
model = DQN.load(os.path.join(current_dir, "Models", full_name, "model"))
print("Loaded")
model.set_env(env)

episode_rewards, episode_lengths = evaluate(
    model, env, NUMBER_OF_EPISODES_EVALUATED, render=False
)

index = np.arange(0, NUMBER_OF_EPISODES_EVALUATED)

df = pd.DataFrame(
    {
        "index": index,
        "Episode Rewards": np.array(episode_rewards),
        "Episode Lengths": np.array(episode_lengths),
    }
)

df.to_json(
    os.path.join(
        current_dir,
        "Evaluations",
        f"agent_evaluation_{full_name}_{NUMBER_OF_SLOTS_EVALUATED}_{NUMBER_OF_EPISODES_EVALUATED}.json",
    )
)