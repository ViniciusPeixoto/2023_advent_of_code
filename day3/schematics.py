import re
from collections import namedtuple
from operator import attrgetter


Index = namedtuple("Index", ["item", "span", "line"])

class Schematics:

    def __init__(self, filename: str, enable_super = False) -> None:
        self.super = enable_super
        self.symbols = {}

        with open(filename) as file:
            self.lines = (line for line in file.readlines())

    def _get_symbols(self, line, line_number):
        symbol_pattern = r"([^\d\.\n])"
        return [Index(m.groups()[0], (m.start() - 1, m.end()), line_number) for m in re.finditer(symbol_pattern, line)]

    def _get_numbers(self, line, line_number):
        number_pattern = r"(\d+)"
        return [Index(m.groups()[0], (m.start(), m.end() -1), line_number) for m in re.finditer(number_pattern, line)]

    def _check_candidates(self, symbols, numbers):
        return [number for symbol in symbols for number in numbers if not any((number.span[1] < symbol.span[0],number.span[0] > symbol.span[1])) and symbol.line - 1 <= number.line <= symbol.line +1]

    def _analyze_lines(self, lines):
        numbers = [number for line, line_number in lines for number in self._get_numbers(line, line_number)]
        symbols = [symbol for line, line_number in lines for symbol in self._get_symbols(line, line_number)]
        return self._check_candidates(symbols, numbers)

    def result(self):
        analysis = set()
        lines = []
        # Avoiding using all lines for memory reasons
        for line_number, line in enumerate(self.lines):
            lines.append((line, line_number))
            if len(lines) == 3:
                for item in self._analyze_lines(lines):
                    analysis.add(item)
                lines.pop(0)

        return sum([int(item.item) for item in analysis])