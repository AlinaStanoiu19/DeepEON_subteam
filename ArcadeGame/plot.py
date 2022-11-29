from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df1 = pd.read_json("Evaluation_data/evaluation_huristic_ce2.json")      # heuristics
df2 = pd.read_json("Evaluation_data/evaluation_curious-water-6.json")   # DQL arrows
df3 = pd.read_json("Evaluation_data/evaluation_neat-gorge-5.json")      # DQL teleport

print("Heuristics performance")
mean_reward1 = np.mean(df1["Episode Rewards"])
std_reward1 = np.std(df1["Episode Rewards"])
print(f"Mean Reward: {mean_reward1}, STD Reward: {std_reward1}")

print("DQL arrows performance")
mean_reward2 = np.mean(df2["Episode Rewards"])
std_reward2 = np.std(df2["Episode Rewards"])
print(f"Mean Reward: {mean_reward2}, STD Reward: {std_reward2}")

print("DQL teleport performance")
mean_reward3 = np.mean(df3["Episode Rewards"])
std_reward3 = np.std(df3["Episode Rewards"])
print(f"Mean Reward: {mean_reward3}, STD Reward: {std_reward3}")


# df1.plot.line("index",y ="Episode Rewards")
# df2.plot.line("index",y ="Episode Rewards")

# df1.plot.line("index",y ="Episode Lengths")
# df2.plot.line("index",y ="Episode Lengths")

fig, ax = plt.subplots()

plt.title("DeepEON vs Heuristics")
plt.xlabel("Episodes")
plt.ylabel("Score")

# eps = [10,20,30,40,50,60,70,80,90,100]
# print(df2)
# a = 0
# av_rew1 = []
# for i,er in enumerate(df1["Episode Rewards"]):
#     a+=er
#     if (i+1) %10 == 0:
#         av = a /10
#         av_rew1.append(av)
#         a = 0
# a = 0
# av_rew2 = []
# for i,er in enumerate(df2["Episode Rewards"]):
#     a+=er
#     if (i+1) %10 == 0:
#         av = a /10
#         av_rew2.append(av)
#         a = 0

# ax.plot(eps,av_rew2,label = "DeepEON")

# ax.plot(eps,av_rew1,label = "Baseline")

ax.plot(df1["index"], df1["Episode Rewards"], label="Heuristics", linewidth=0.5, color="red")
ax.plot(df2["index"], df2["Episode Rewards"], label="DeepEON arrows", linewidth=0.5, color="deepskyblue")
ax.plot(df3["index"], df3["Episode Rewards"], label="DeepEON teleport", linewidth=0.5, color="navy")

ax.plot(df1["index"], np.full((1000,), mean_reward1), linewidth=2, color="red")
ax.plot(df2["index"], np.full((1000,), mean_reward2), linewidth=2, color="deepskyblue")
ax.plot(df3["index"], np.full((1000,), mean_reward3), linewidth=2, color="navy")

plt.legend()

plt.show()