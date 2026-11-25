import start

game = start.game()
cooperate, defect = 0, 1
# Step 1. encoding + initialization
# Switch all rules to rule tables (this will only work for non randomized rules)
def encode_to_rule_table(game):
    C, D = cooperate, defect
    # (last_A, last_B, lastlast_A, lastlast_B)
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
    rule_table_dict = {}
    for strategy in game.all_strats_list():
        rule_table_dict[strategy] = rule_table_blueprint.copy()
        for input_table in rule_table_blueprint:
            game.game_history[-1][0] = input_table[0]
            game.game_history[-1][1] = input_table[1]
            game.game_history[-2][0] = input_table[2]
            game.game_history[-2][1] = input_table[3]
            rule_table_dict[strategy][input_table] = game.output_from_strategy(strategy, "A")
    return rule_table_dict

rule_table = encode_to_rule_table(game)
# Step 1. Selection