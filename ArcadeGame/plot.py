from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df1 = pd.read_json("Evaluations/heuristic_evaluation_8_24_5_10_-10_-15_0_3_2_16_8_1000.json")      # heuristics
df2 = pd.read_json("Evaluations/agent_evaluation_8_24_5_10_-10_-15_0_3_2_16_8_1000.json")   # DQL arrows
# df3 = pd.read_json("Evaluation_data/evaluation_neat-gorge-5.json")      # DQL slot selection

print("Heuristics performance")
mean_reward1 = np.mean(df1["Episode Rewards"])
std_reward1 = np.std(df1["Episode Rewards"])
print(f"Mean Reward: {mean_reward1}, STD Reward: {std_reward1}")

print("DQL arrows performance")
mean_reward2 = np.mean(df2["Episode Rewards"])
std_reward2 = np.std(df2["Episode Rewards"])
print(f"Mean Reward: {mean_reward2}, STD Reward: {std_reward2}")

# print("DQL slot selection performance")
# mean_reward3 = np.mean(df3["Episode Rewards"])
# std_reward3 = np.std(df3["Episode Rewards"])
# print(f"Mean Reward: {mean_reward3}, STD Reward: {std_reward3}")

# Start plotting

fig, ax = plt.subplots()

plt.title("DeepEON vs Heuristics")
plt.xlabel("Episodes")
plt.ylabel("Score")

##### PLOT ALL EPISODES #####

# ax.plot(df1["index"], df1["Episode Rewards"], label="Heuristics", linewidth=0.5, color="red")
# ax.plot(df2["index"], df2["Episode Rewards"], label="DeepEON arrows", linewidth=0.5, color="deepskyblue")
# ax.plot(df3["index"], df3["Episode Rewards"], label="DeepEON teleport", linewidth=0.5, color="navy")

# ax.plot(df1["index"], np.full((1000,), mean_reward1), linewidth=2, color="red")
# ax.plot(df2["index"], np.full((1000,), mean_reward2), linewidth=2, color="deepskyblue")
# ax.plot(df3["index"], np.full((1000,), mean_reward3), linewidth=2, color="navy")

# plt.legend()

# plt.show()

##### PLOT ALL EPISODES #####



new_eps = []
avg_df1 = []
avg_df2 = []
avg_df3 = []
num_avg = 20
y_avg = int(1000/num_avg)

for i in range(10, 1001, num_avg):
    new_eps.append(i)

a = 0
for i, er in enumerate(df1["Episode Rewards"]):
    a += er
    if (i+1) % num_avg == 0:
        avg = a / num_avg
        avg_df1.append(avg)
        a = 0
a = 0
for i, er in enumerate(df2["Episode Rewards"]):
    a += er
    if (i+1) % num_avg == 0:
        avg = a / num_avg
        avg_df2.append(avg)
        a = 0
# a = 0
# for i, er in enumerate(df3["Episode Rewards"]):
#     a += er
#     if (i+1) % num_avg == 0:
#         avg = a / num_avg
#         avg_df3.append(avg)
#         a = 0

ax.plot(new_eps, avg_df1, label="Heuristics", linewidth=0.5, color="red")
ax.plot(new_eps, avg_df2, label="DeepEON Arrows", linewidth=0.5, color="deepskyblue")
#ax.plot(new_eps, avg_df3, label="DeepEON SL", linewidth=0.5, color="navy")

ax.plot(new_eps, np.full((y_avg,), mean_reward1), linewidth=2, color="red")
ax.plot(new_eps, np.full((y_avg,), mean_reward2), linewidth=2, color="deepskyblue")
#ax.plot(new_eps, np.full((y_avg,), mean_reward3), linewidth=2, color="navy")

plt.legend()

plt.show()