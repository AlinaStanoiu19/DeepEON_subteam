from datetime import datetime
from Games.game5 import ArcadeGame
import numpy as np
import pandas as pd
import os
from config import current_dir, all_configs, full_name


NUMBER_OF_SLOTS = all_configs["number_of_slots"]
K = all_configs["K"]
episode_count_targets = all_configs["number_of_episodes_evaluated"]
SOLUTION_REWARD = all_configs["solution_reward"]

# initialise ids 
episode_id = 0
action_id = 0


 # df with episode performance data
episode_count = 0
episode_rewards = []
episode_lengths = []

# df with action-level analytics
episode_ids = []
action_ids = []
request_info = []
actions = []
action_rewards = []


game = ArcadeGame()
while episode_count < episode_count_targets:
    print("---------------NEW EPISODE---------------")
    episode_reward = 0
    current_length = 0
    done = False
    game.new_game()
    game.draw_screen()
    #game.render()
    while not done:
        solution = False
        for k in range(K):
            for i in range(
                NUMBER_OF_SLOTS - game.slots
            ):  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                first_slot = k * (NUMBER_OF_SLOTS + 1) + i
                if game.is_solution(first_slot=first_slot):
                    solution = True
                    action = k
                    game.first_slot = first_slot
                    break
            if solution:
                break
        if not solution:
            game.first_slot = 0
        game.update_spec_grid()
        game.draw_screen()
        # game.render()
        reward, done, info = game.check_solution()
        episode_reward += reward
        current_length += 1
        action_info =  {'action_id': action_id, 'action': action, 'reward': reward}
        print(f"action id: {action_id}, action: {action}, request info: {info}")
        episode_ids.append(episode_count)
        action_ids.append(action_info['action_id'])
        request_info.append(info)
        actions.append(action_info['action'])
        action_rewards.append(action_info['reward'])
        action_id += 1


    episode_rewards.append(episode_reward)
    episode_lengths.append(current_length)
    episode_count += 1
    print(f"-----------------EPISODE: {episode_count}-------------------------")
    
# Print overall statistics
mean_reward = np.mean(episode_rewards)
std_reward = np.std(episode_rewards)
print(mean_reward)

index = np.arange(0, episode_count_targets)

# performance dataframe and export to json
perf_df = pd.DataFrame(
    {
        "index": index,
        "Episode Rewards": np.array(episode_rewards),
        "Episode Lengths": np.array(episode_lengths),
    }
)
perf_df.to_json(
    os.path.join(
        current_dir,
        "Evaluations",
        f"heuristic_evaluation_{full_name}_{NUMBER_OF_SLOTS}_{episode_count_targets}.json",
    )
)

# data & analytics dataframe and export to json
da_df = pd.DataFrame(
    {
        "Episode IDs": np.array(episode_ids),
        "Action IDs": np.array(action_ids),
        "Request Info": np.array(request_info),
        "Actions": np.array(actions),
        "Action Rewards": np.array(action_rewards),
    }
)


# Adding path lengths to the dataframe
da_df['Path length']  = da_df['Request Info'].apply(lambda x: len(x['constructed_path'])-1)

# Calculating allocated slots for each episode
episode_sum = {}
lastid = -1

for index, row in da_df.iterrows():
    episode = row['Episode IDs']
    info = row['Request Info']
    info_id = info['id']
    info_slots = info['slots']
    if info_id>lastid:
        lastid = info_id
        if episode not in episode_sum.keys():
            episode_sum[episode] = info_slots
        else:
            episode_sum[episode] += info_slots   

da_df['Utility'] = da_df['Episode IDs'].map(episode_sum)

print(da_df)

# Saving dataframe
da_df.to_json(
    os.path.join(
        current_dir,
        "Analytics",
        f"heuristic_evaluation_{full_name}_{NUMBER_OF_SLOTS}_{episode_count_targets}.json",
    )
)


