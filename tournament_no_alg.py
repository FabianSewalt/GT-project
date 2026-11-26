# code that plots game length on x-axis, average points per game for strategy x when playing against all other strategies on y-axis (for every strategy)

import matplotlib.pyplot as plt
import numpy as np
from start import game

all_strats = game().all_strats_list()

game_lengths = np.arange(1, 300, 1)

# results[strat] = list of total points, one entry per game length
results = {strat: [] for strat in all_strats}

for game_len in game_lengths:
    points_dict = {}
    for strat in all_strats:
        points_dict[strat] = 0
    for i, stratA in enumerate(all_strats):
        for j, stratB in enumerate(all_strats):
            # playing every strat against every other strat once (and itself)
            if i >= j:
                match = game()
                match.set_playerA_strategy(stratA)
                match.set_playerB_strategy(stratB)
                for x in range(game_len):
                    match.do_one_game()
                
                Apoints, Bpoints = match.get_points()
                points_dict[stratA] += Apoints
                points_dict[stratB] += Bpoints

    for strat in all_strats:
        # we divide by (len(all_strats)-1)*game_len to get the average number of points a strategy earns per game
        results[strat].append(points_dict[strat] / ((len(all_strats)-1)*game_len))

for strat in all_strats:
    plt.plot(game_lengths, results[strat], label=strat)
plt.xlabel("game length (rounds)")
plt.ylabel("average points per round")
plt.legend(fontsize=7)
plt.show()