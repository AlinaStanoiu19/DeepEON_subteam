from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df1 = pd.read_json("Evaluation_data/evaluation_huristic_2.json") #baseline
df2 = pd.read_json("Evaluation_data/evaluation_w8tdjaly.json") #DQL

mean_reward1 = np.mean(df1["Episode Rewards"])
std_reward1 = np.std(df1["Episode Rewards"])
print(f"Mean Reward: {mean_reward1}, STD Reward: {std_reward1}")

mean_reward2 = np.mean(df2["Episode Rewards"])
std_reward2 = np.std(df2["Episode Rewards"])
print(f"Mean Reward: {mean_reward2}, STD Reward: {std_reward2}")


# df1.plot.line("index",y ="Episode Rewards")
# df2.plot.line("index",y ="Episode Rewards")

# df1.plot.line("index",y ="Episode Lengths")
# df2.plot.line("index",y ="Episode Lengths")

fig, ax = plt.subplots()

#ax.plot(df1["index"],df2["Episode Rewards"],label = "DeepEON")
#ax.plot(df1["index"],df1["Episode Rewards"],label = "Baseline")

plt.title("DeepEON vs Baseline")
plt.xlabel("Rounds")
plt.ylabel("Score")

eps = [10,20,30,40,50,60,70,80,90,100]
print(df2)
a = 0
av_rew1 = []
for i,er in enumerate(df1["Episode Rewards"]):
    a+=er
    if (i+1) %10 == 0:
        av = a /10
        av_rew1.append(av)
        a = 0
a = 0
av_rew2 = []
for i,er in enumerate(df2["Episode Rewards"]):
    a+=er
    if (i+1) %10 == 0:
        av = a /10
        av_rew2.append(av)
        a = 0

ax.plot(eps,av_rew2,label = "DeepEON")

ax.plot(eps,av_rew1,label = "Baseline")

plt.legend()

plt.show()