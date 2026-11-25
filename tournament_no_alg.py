from start import game
import matplotlib.pyplot as plt

tournament = game()

all_strats = tournament.all_strats_list()

game_length = 100

for stratA in all_strats:
    for stratB in all_strats:
        if stratA != stratB:
            tournament.set_playerA_strategy(stratA)
            tournament.set_playerB_strategy(stratB)


# stratA = 'evenpoints'
# stratB = 'titfortat'

# game1.set_playerA_strategy(stratA)
# game1.set_playerB_strategy(stratB)


# number_of_games_list = []
# A_points_list = []
# B_points_list = []

# for i in range(200):
#     game1.do_one_game()
#     pointsA, pointsB = game1.get_points()
#     A_points_list.append(pointsA)
#     B_points_list.append(pointsB)
#     number_of_games_list.append(i+1)

# plt.plot(number_of_games_list, A_points_list, label="points of A")
# plt.plot(number_of_games_list, B_points_list, label="points of B")
# plt.xlabel("number of games played")
# plt.ylabel('points')
# plt.legend()
# plt.show()