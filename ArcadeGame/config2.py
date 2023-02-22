import os

current_dir = os.path.dirname(os.path.abspath(__file__))


temp_configs = {
    "env": 3,
    "episode_end": 2,
    "end_limit":16,
    "number_of_slots": 8,
    "screen_number_of_slots": 24,
    "number_of_slots_evaluated": 8,
    "number_of_episodes_evaluated": 1000,
    "K": 5,
    "solution_reward": 10,
    "rejection_reward": -10,
    "gap_rejection_reward": -15,
    "left_reward": 0,
    "right_reward": 0,
    "seed": 0,
    "total_timesteps": 500000,
    "buffer_size": 10000,
    "batch_size": 256,
    "exploration_final_eps": 0.05,
    "exploration_fraction": 0,
    "gamma": 0.995,
    "learning_rate": 0.001,
    "learning_starts": 50000,
    "target_update_interval": 5000,
    "train_freq": (256, "step"),
    "width": 20,
    "height": 20,
    "screen_width": 0,
    "screen_height": 150,
    "screen_side_offset": 1,
    "path_rows": 5,
    "spectrum_slots_rows_from_top": 6,
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
}

temp_configs["screen_width"] = (
    temp_configs["screen_number_of_slots"] * temp_configs["width"]
    * temp_configs["K"]
    + (temp_configs["K"] + 1) * temp_configs["width"]
)

all_configs = temp_configs

full_name = f"{all_configs['number_of_slots']}_{all_configs['screen_number_of_slots']}_{all_configs['K']}_{all_configs['solution_reward']}_{all_configs['rejection_reward']}_{all_configs['gap_rejection_reward']}_{all_configs['seed']}_{all_configs['env']}_{all_configs['episode_end']}_{all_configs['end_limit']}"

model_config = {
    "env": all_configs["env"],
    "episode_end": all_configs["episode_end"],
    "number_of_slots": all_configs["number_of_slots"],
    "screen_number_of_slots": all_configs["screen_number_of_slots"],
    "K": all_configs["K"],
    "solution_reward": all_configs["solution_reward"],
    "rejection_reward": all_configs["rejection_reward"],
    "left_reward": all_configs["left_reward"],
    "right_reward": all_configs["right_reward"],
    "seed": all_configs["seed"],
    "end_limit": all_configs["end_limit"],
    "total_timesteps": all_configs["total_timesteps"],
    "buffer_size": all_configs["buffer_size"],
    "batch_size": all_configs["batch_size"],
    "exploration_final_eps": all_configs["exploration_final_eps"],
    "exploration_fraction": all_configs["exploration_fraction"],
    "gamma": all_configs["gamma"],
    "learning_rate": all_configs["learning_rate"],
    "learning_starts": all_configs["learning_starts"],
    "target_update_interval": all_configs["target_update_interval"],
    "train_freq": all_configs["train_freq"],
}

game_config = {
    "K": all_configs["K"],
    "solution_reward": all_configs["solution_reward"],
    "rejection_reward": all_configs["rejection_reward"],
    "left_reward": all_configs["left_reward"],
    "right_reward": all_configs["right_reward"],
    "seed": all_configs["seed"],
}