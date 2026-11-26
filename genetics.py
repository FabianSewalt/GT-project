import start
import random
import matplotlib.pyplot as plt

cooperate, defect = 0, 1
C, D = cooperate, defect
rule_table_blueprint = {
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
game = start.game()

def encode_to_rule_table(game):
    # (last_A, last_B, lastlast_A, lastlast_B)
    rule_table_dict = {}
    for strategy in game.all_strats_list():
        if not "random" in strategy:
            rule_table_dict[strategy] = rule_table_blueprint.copy()
            for input_table in rule_table_blueprint:
                game.game_history[-1][0] = input_table[0]
                game.game_history[-1][1] = input_table[1]
                game.game_history[-2][0] = input_table[2]
                game.game_history[-2][1] = input_table[3]
                rule_table_dict[strategy][input_table] = game.output_from_strategy(strategy, "A")
    return rule_table_dict

def find_fittest_relative(game, rule_table, steps=200):
    point_dict = {}
    for rule in rule_table:
        point_dict[rule] = 0
    i = 0
    n_rules = len(rule_table)
    for rule_A in rule_table:
        j = 0
        for rule_B in rule_table:
            if j > i:
                # X_1 is last step, X_2 is two steps ago
                A_1, A_2, B_1, B_2 = None, None, None, None
                for x in range(steps):
                    choice_A = rule_table[rule_A][(A_1, B_1, A_2, B_2)]
                    choice_B = rule_table[rule_B][(B_1, A_1, B_2, A_2)]
                    a, b = game.calculate_payoff(choice_A, choice_B)
                    point_dict[rule_A] += a
                    point_dict[rule_B] += b
                    A_2 = A_1
                    B_2 = B_1
                    A_1 = choice_A
                    B_1 = choice_B
            j += 1
        i += 1
    fittest = []
    scores = []
    i = 1
    for key in sorted(point_dict, key=point_dict.get):
        if i > len(rule_table) - 4:
            fittest.append(key)
            # normalize scores to an average
            scores.append(point_dict[key]/(n_rules * steps))
        i += 1
    return fittest, scores

def find_fittest_original(game, rule_table, steps=200):   
    point_dict = {}
    for rule in rule_table:
        point_dict[rule] = 0
    steps = 200
    n_rules = len(rule_table) 
    original_rule_table = encode_to_rule_table(game)
    for i, rule_A in enumerate(rule_table):
        for j, rule_B in enumerate(original_rule_table):
            # X_1 is last step, X_2 is two steps ago
            A_1, A_2, B_1, B_2 = None, None, None, None
            for x in range(steps):
                choice_A = rule_table[rule_A][(A_1, B_1, A_2, B_2)]
                choice_B = original_rule_table[rule_B][(B_1, A_1, B_2, A_2)]
                a, b = game.calculate_payoff(choice_A, choice_B)
                point_dict[rule_A] += a
                A_2 = A_1
                B_2 = B_1
                A_1 = choice_A
                B_1 = choice_B
    fittest = []
    scores = []
    i = 1
    for key in sorted(point_dict, key=point_dict.get):
        if i > len(rule_table) - 4:
            fittest.append(key)
            # normalize scores to an average
            scores.append(point_dict[key]/(n_rules))
        i += 1
    return fittest, scores

def crossover(fittest, rule_table, gen):
    new_rule_table = {}
    child = 0

    for i, rule in enumerate(fittest):
        new_rule_table[f"parent{i}"] = rule_table[rule]

    for i, rule1 in enumerate(fittest):
        for j, rule2 in enumerate(fittest):
            if j > i:
                new_rule_table_1 = rule_table_blueprint.copy()
                new_rule_table_2 = rule_table_blueprint.copy()
                # Take a random selection from rule table 1 and the other rules from rule table 2
                rule1_rules = random.sample(range(len(rule_table[rule1])), random.randint(0, len(rule_table_blueprint)//2))
                for k, (a, b, c, d) in enumerate(rule_table_blueprint):
                    if k in rule1_rules:
                        new_rule_table_1[(a, b, c, d)] = rule_table[rule1][(a, b, c, d)]
                        new_rule_table_2[(a, b, c, d)] = rule_table[rule2][(a, b, c, d)]
                    else:
                        new_rule_table_1[(a, b, c, d)] = rule_table[rule2][(a, b, c, d)]
                        new_rule_table_2[(a, b, c, d)] = rule_table[rule1][(a, b, c, d)]
                new_rule_table[f"gen{gen}child{child}"] = new_rule_table_1.copy()
                new_rule_table[f"gen{gen}child{child+1}"] = new_rule_table_2.copy()
                child += 2
    return new_rule_table

def mutation(rule_table, mutation_rate = 0.01):
    mutations = 0
    for rule in rule_table:
        for k, (a, b, c, d) in enumerate(rule_table[rule]):
            if random.random() < mutation_rate and not "parent" in rule:
                rule_table[rule][(a, b, c, d)] = abs(rule_table[rule][(a, b, c, d)] - 1)
                mutations += 1
    return rule_table

for mutation_rate in [0.01, 0.02, 0.03, 0.04, 0.05]:
    iterations = 100
    # Step 1. encoding + initialization
    # Switch all rules to rule tables (this will only work for non randomized rules)
    rule_table = encode_to_rule_table(game)
    max_score = []
    for i in range(iterations):
        # Step 2. Selection
        # select the fittest strategies at the current generation
        if i > 0:
            # Score based on how strong compared to the original the rule_table is to find point of convergence
            fittest, scores = find_fittest_original(game, rule_table, steps=200)
        else:
            # Since the rule table is still the original, it should be based against itself
            fittest, scores = find_fittest_relative(game, rule_table, steps=200)
        max_score.append(max(scores))

        # Step 3. Crossover
        rule_table = crossover(fittest, rule_table, gen=i)

        # Step 4. Mutation
        rule_table = mutation(rule_table, mutation_rate=mutation_rate)
    plt.plot([i for i in range(iterations)], max_score, label=f"Score at mutation rate: {mutation_rate}")
plt.legend()
plt.show()