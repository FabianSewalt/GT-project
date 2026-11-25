import math
import numpy as np
import random
import matplotlib.pyplot as plt

defect = 1
cooperate = 0

def rule_to_base_2(n):
    """Converts a given decimal (i.e. base-10 integer) to a list containing the
    base-2 equivalant."""

    # n is the rule = number to be converted to base_k, k = base
    base_2_list = []
    base_2_part = n

    while base_2_part > 0:
        base_2_remainder = base_2_part % 2  # calculate remainder 
        base_2_part = base_2_part // 2  # floor division
        base_2_list.append(base_2_remainder)

    base_2_list.reverse()
    # 21 because the rule length should be 21.
    base_2_list = [0] * (21 - len(base_2_list)) + base_2_list

    return base_2_list

def make_rule_i(i):
    if i < 0 or i >= 2**21:
        raise ValueError("rule number must be between 0 and 2**21 - 1")
    rule_list = rule_to_base_2(i)
    C, D = cooperate, defect
    standard_rule = {
        (None, None, None, None): None,
        (C, C, None, None): None,
        (C, D, None, None): None,
        (D, C, None, None): None,
        (D, D, None, None): None,
        (C, C, C, C): None,
        (C, C, C, D): None,
        (C, C, D, C): None,
        (C, C, D, D): None,
        (C, D, C, C): None,
        (C, D, C, D): None,
        (C, D, D, C): None,
        (C, D, D, D): None,
        (D, C, C, C): None,
        (D, C, C, D): None,
        (D, C, D, C): None,
        (D, C, D, D): None,
        (D, D, C, C): None,
        (D, D, C, D): None,
        (D, D, D, C): None,
        (D, D, D, D): None,
    }
    for index, prev_moves in enumerate(standard_rule):
        standard_rule[prev_moves] = rule_list[index]

    return standard_rule
        

class game:
    def __init__(self):
        self.game_history = [[None, None], [None, None]]
        self.playerA_strategy = None
        self.playerB_strategy = None
        self.pointsA = 0
        self.pointsB = 0
        

    def do_one_game(self):
        # look into game history to define what the player should do next
        # put the outputs of what both players do in calculate payoff and add this to their total payoff and print who wins and why
        strat_A, strat_B = self.playerA_strategy, self.playerB_strategy
        output_A = self.output_from_strategy(strat_A, 'A')
        output_B = self.output_from_strategy(strat_B, 'B')
        self.game_history.append([output_A, output_B])

        P_A, P_B = self.calculate_payoff(output_A, output_B)
        self.pointsA += P_A
        self.pointsB += P_B
        print(f"A {'defected' if output_A == defect else 'cooperated'} and B {'defected' if output_B == defect else 'cooperated'} resulting in {P_A} points for A and {P_B} points for B")

    def output_from_strategy(self, strategy, player):
        if not isinstance(strategy, dict) and strategy not in self.all_strats_list():
            raise ValueError(f"{strategy} is not an existing strategy")

        if player == 'A':
            last_self, last_other = self.game_history[-1][0], self.game_history[-1][1]
            lastlast_self, lastlast_other = self.game_history[-2][0], self.game_history[-2][1]
            self_points = self.pointsA
            other_points = self.pointsB
        if player == 'B':
            last_other, last_self = self.game_history[-1][0], self.game_history[-1][1]
            lastlast_other, lastlast_self = self.game_history[-2][0], self.game_history[-2][1]
            self_points = self.pointsB
            other_points = self.pointsA

        if isinstance(strategy,dict):
            return strategy[(last_self, last_other, lastlast_self, lastlast_other)]

        if strategy == 'titfortat':
            if last_self == last_other == None:
                return cooperate
            return last_other
        if strategy == 'cooperate':
            return cooperate
        if strategy == 'defect':
            return defect
        if strategy == 'anti-titfortat':
            if last_other == last_self == None:
                return defect
            return abs(last_other - 1) 
        if strategy == 'pointcounter': 
            if self_points < other_points:
                return defect
            return cooperate
        if strategy == 'anti-pointcounter': 
            if self_points < other_points:
                return cooperate
            return defect
        if strategy == 'lookingback':
            if last_other == cooperate or lastlast_other == cooperate:
                return defect
            return cooperate
        if strategy == 'tiktok':
            if last_self == None:
                return defect
            return abs(last_self - 1)
        if strategy == 'evenpoints':
            if self_points % 2 == 0:
                return defect
            return cooperate

        # Tom's strategies
        if strategy == "biased_random_evil":
            if random.random() <= 0.3:
                return cooperate
            else:
                return defect
        if strategy == "biased_random_friendly":
            if random.random() <= 0.3:
                return defect
            else:
                return cooperate
        if strategy == "double_switchup":
            if last_self == cooperate:
                if lastlast_self == cooperate:
                    return defect
                else:
                    return cooperate
            else:
                if lastlast_self == defect:
                    return cooperate
                else:
                    return defect
        if strategy == "become_more_evil":
            if last_self == None:
                self.bias = 0
            if random.random() <= self.bias:
                return defect
            else:
                self.bias += 0.05
                return cooperate
        if strategy == "sine_bias":
            self.sine_bias = math.sin((len(self.game_history) - 2)/(2 * np.pi))
            if random.random() <= self.bias:
                return defect
            else:
                return cooperate

            
    def set_playerA_strategy(self, strategy):
        self.playerA_strategy = strategy

    def set_playerB_strategy(self, strategy):
        self.playerB_strategy = strategy
    
    def calculate_payoff(self, choice_A, choice_B):
        if choice_A == defect and choice_B == defect:
            return 1, 1
        if choice_A == defect and choice_B == cooperate:
            return 5, 0
        if choice_A == cooperate and choice_B == defect:
            return 0, 5
        if choice_A == cooperate and choice_B == cooperate:
            return 3, 3

    def get_points(self):
        return self.pointsA, self.pointsB

    def all_strats_list(self):
        # 'titfortat' cooperates at first game and then copies opponent
        # 'cooperate' always cooperates
        # 'defect' always defects
        # 'antititfortat' defects at first and then does opposite of what opponent did last
        # 'pointcounter' defects if it has less points than the other player and otherwise cooperates
        # 'anti-pointcounter' cooperates if it has less points than the other player and otherwise defects
        # 'lookingback' defects if the oponent cooperated at least once in the last two moves and otherwise cooperates 
        # 'tiktok' starts with defecting and then does the opposite of what it previously did (so it will loop)
        # 'evenpoints' defects if it has an even amount of points and cooperates otherwise
        return ['titfortat', 'defect', 'cooperate', 'anti-titfortat', 'pointcounter', 'anti-pointcounter', 'lookingback', 'tiktok', 'evenpoints', "biased_random_evil", "biased_random_friendly", "double_switchup", "become_more_evil", "sine_bias"]

game1 = game()

stratA = 'evenpoints'
stratB = 'titfortat'

game1.set_playerA_strategy(stratA)
game1.set_playerB_strategy(stratB)

print(f"strategy A: {stratA}, strategy B: {stratB}")

number_of_games_list = []
A_points_list = []
B_points_list = []

for i in range(200):
    game1.do_one_game()
    pointsA, pointsB = game1.get_points()
    A_points_list.append(pointsA)
    B_points_list.append(pointsB)
    number_of_games_list.append(i+1)

plt.plot(number_of_games_list, A_points_list, label="points of A")
plt.plot(number_of_games_list, B_points_list, label="points of B")
plt.xlabel("number of games played")
plt.ylabel('points')
plt.legend()
plt.show()