from start import game
import matplotlib.pyplot as plt

tournament = game()

all_strats = tournament.all_strats_list()

game_length = 100

points_dict = {}
for strat in all_strats:
    points_dict[strat] = 0

for stratA in all_strats:
    for stratB in all_strats:
        if stratA != stratB:
            tournament.set_playerA_strategy(stratA)
            tournament.set_playerB_strategy(stratB)
            for i in range(game_length):
                tournament.do_one_game()
            
            Apoints, Bpoints = tournament.get_points()
            points_dict[stratA] += Apoints
            points_dict[stratB] += Bpoints
            tournament.reset_points()

print(points_dict)