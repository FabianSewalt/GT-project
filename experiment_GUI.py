from pyics import Model, GUI
from start import game, cooperate, defect

class TournamentSim(Model):
    def __init__(self):
        Model.__init__(self)

        self.make_param("rounds", 200)
        self.make_param("self_play", True)

    def reset(self):
        self.t = 0 # rounds played so far
        self.strategies = game().all_strats_list()
        self.matches = []

        for i, strat_A in enumerate(self.strategies):
            for j, strat_B in enumerate(self.strategies):
                if i > j or (i == j and self.self_play):
                    match = game()
                    match.set_playerA_strategy(strat_A)
                    match.set_playerB_strategy(strat_B)
                    self.matches.append(match)

    def step(self):
        if self.t >= self.rounds:
            return True

        for match in self.matches:
            match.do_one_game() # one round in every match up
        self.t += 1

        return self.t >= self.rounds # return True or False based on wether we are done

    def average_scores(self):
        totals = {strat: 0 for strat in self.strategies}
        for match in self.matches:
            points_A, points_B = match.get_points()
            totals[match.playerA_strategy] += points_A
            # only adding points of B if A is not B, prevents double adding points when A plays against A 
            if match.playerA_strategy != match.playerB_strategy:
                totals[match.playerB_strategy] += points_B

        if self.self_play:
            n_opponents = len(self.strategies)
        else:
            n_opponents = len(self.strategies) - 1
        rounds_played = max(self.t, 1) # avoid dividing by 0 before round 1

        avg_scores = {}
        for strat in self.strategies:
            avg_scores[strat] = totals[strat] / (n_opponents * rounds_played)
        return avg_scores

    def draw(self):
        import matplotlib.pyplot as plt

        scores = self.average_scores()
        # sort the strats on scores from low to high
        ranking = sorted(scores, key=scores.get)

        plt.cla()
        plt.barh(ranking, [scores[strat] for strat in ranking])
        plt.xlim(0, 5)
        plt.xlabel("average points per round")
        plt.title(f"round {self.t} / {self.rounds}")
        plt.tight_layout()


if __name__ == "__main__":
    sim = TournamentSim()
    cx = GUI(sim)
    cx.start()