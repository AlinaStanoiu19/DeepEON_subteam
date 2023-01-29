from stable_baselines3 import DQN
from envs.custom_env2 import CustomEnv as CustomEnv2
from envs.custom_env3 import CustomEnv as CustomEnv3

if model_config["env"] == 2:
    env = CustomEnv2()
elif model_config["env"] == 3:
    env = CustomEnv3()
else:
    print("env not selected correctly in config.py")
    exit(1)

model = DQN.load("deepq_EON3")
model.set_env(env)
model.learn(
    total_timesteps=all_configs["total_timesteps"],
    tb_log_name="Logs",
    reset_num_timesteps=False,
)
model.save("deepq_EON3_continued_1")