import re
from math import pow

class Scratchcards:

    def __init__(self, filename: str, enable_super = False) -> None:
        self.super = enable_super

        with open(filename) as file:
            self.lines = (line for line in file.readlines())

    def _get_winning_numbers(self, line):
        """
        Returns all winning numbers in a game.
        """
        winning_pattern = r"(:\s+)(\d+(\s+\d+)*) \|"
        return re.search(winning_pattern, line).group(2).split()

    def _get_ticket_numbers(self, line):
        """
        Returns all ticket numbers in a game.
        """
        ticket_pattern = r"(\|\s+)(\d+(\s+\d+)*)"
        return re.search(ticket_pattern, line).group(2).split()

    def _get_number_of_wins(self, winning_numbers, ticket_numbers):
        """
        Returns how many lucky numbers in a game.
        """
        return len([number for number in ticket_numbers if number in winning_numbers])

    def _get_points(self, winning_numbers, ticket_numbers):
        """
        Returns how many points the game made.
        """
        n_of_wins = self._get_number_of_wins(winning_numbers, ticket_numbers)
        return int((n_of_wins > 0) * 2 ** (n_of_wins - 1))

    def _calculate_scratches(self, line, scratches, line_number):
        """
        Verify and extends the number of scratchcards available according to how many lucky numbers.
        """
        n_of_wins = self._get_number_of_wins(self._get_winning_numbers(line), self._get_ticket_numbers(line))
        for next_lines in range(line_number, line_number + n_of_wins):
            try:
                scratches[str(next_lines + 1)] += 1
            except KeyError:
                scratches[str(next_lines + 1)] = 1

    def result(self):
        """
        Calculates the sum of points in all cards. If in `super` mode, calculates the total number of scratchcards.
        """
        if not self.super:
            return sum([self._get_points(self._get_winning_numbers(line), self._get_ticket_numbers(line)) for line in self.lines])

        scratchcards = 0
        scratches = {"0": 0}
        for line_number, line in enumerate(self.lines):
            try:
                for _ in range(scratches[str(line_number)] + 1):
                    self._calculate_scratches(line, scratches, line_number)
                    scratchcards += 1
            except KeyError:
                self._calculate_scratches(line, scratches, line_number)
                scratchcards += 1

        return scratchcards