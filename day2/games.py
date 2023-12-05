import re
from functools import reduce

class Games:

    def __init__(self, filename: str, configuration: dict, enable_super = False) -> None:
        self.super = enable_super
        self.config = configuration

        with open(filename) as file:
            self.lines = (line.strip() for line in file.readlines())

    def _get_game_runs(self, line):
        """
        Returns a list of individual runs in a game.
        """
        run_pattern = r"(?P<run>((\d+) [a-z]+[, ]*)+\;)"
        return [m.group("run") for m in re.finditer(run_pattern, line + ";")]

    def _get_run_values(self, run):
        """
        Returns a dict with all values from the colored dice in a run.
        """
        value_pattern = f"(\d+) ({'|'.join(f'{color}' for color in ['red', 'green', 'blue'])})"
        return {key: int(value) for value, key in re.findall(value_pattern, run)}

    def _get_possible(self, line):
        """
        Returns `True` if the game in line is possible. Returns `False` otherwise.
        """
        results = []
        runs = self._get_game_runs(line)

        for run in runs:
            values = self._get_run_values(run[:-1])
            for key in values:
                results.append(self.config[key] >= values[key])

        return all(results)

    def _get_minimum_values_per_game(self, line):
        """
        Returns a dict with the lowest values required for every colored die for a game
        to be possible.
        """
        biggest_values_in_run = {key: 0 for key in self.config}
        runs = self._get_game_runs(line)
        for run in runs:
            values = self._get_run_values(run[:-1])
            for key in values:
                if values[key] > biggest_values_in_run[key]:
                    biggest_values_in_run[key] = values[key]

        return biggest_values_in_run

    def verify(self):
        """
        Returns the sum of all possible games IDs, or the sum of all Power of games.
        """
        games = []
        for line in self.lines:
            
            game_number = int(re.match(r"Game (\d+):", line).group(1))
            if not self.enable_power:
                if self._get_possible(line):
                    games.append(game_number)
            else:
                games.append(reduce(lambda x, y: x* y, list(self._get_minimum_values_per_game(line).values())))

        return sum(games)
