import re


CONVERTER = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class Trebuchet:

    def __init__(self, calibration_filename: str, enable_super = False) -> None:
        self.super = enable_super
        self.calibration_total = 0

        try:
            with open(calibration_filename) as file:
                self.calibration = (line.strip() for line in file.readlines())
        except Exception as e:
            raise e

    def _get_first_and_last_digits(self, line: str) -> tuple:
        """
        Returns a tuple containing the first and last digits and their indexes in pairs.
        """
        search_pattern = r"\D*(\d)[\D|\d]*?(\d)*\D*$"
        search_indexes = [
            m.span(group)[0] for m in re.finditer(search_pattern, line) for group in range(1, 1+len(m.groups()))
        ]

        digits = re.search(search_pattern, line)
        if not digits:
            return (None, -1), (None, -1)

        first, last = digits.groups()
        return (first, search_indexes[0]), (last, search_indexes[-1])

    def _get_numbers(self, line: str):
        """
        Returns a integer formed from two digits. If there's only one digit, it is duplicated.
        """
        first, last = self._get_first_and_last_digits(line)

        if first[0] is None:
            # There are no digits in this line
            return 0

        return int(f"{first[0]}{last[0] if last[0] else first[0]}")

    def _get_number_names_indexes(self, line: str):
        """
        Retrieves spelled out numbers indexes and their span in a string.
        """
        sub_pattern = f"(?={'|'.join(f'({number})' for number in CONVERTER.keys())})"
        sub_indexes = [index+1 for m in re.findall(sub_pattern, line) for index, value in enumerate(m) if value]

        return [m.span(index) for m in re.finditer(sub_pattern, line) for index in sub_indexes if all(num >= 0 for num in m.span(index))]

    def _convert_line(self, line: str, positions: list, first: int, last: int):
        """
        Converts spelled out numbers into digits in a string.
        """
        try:
            start_prefix, stop_prefix = positions[0][0], positions[0][1]
            start_suffix, stop_suffix = positions[-1][0],positions[-1][1]
            prefix = line[start_prefix:stop_prefix]
            suffix = line[start_suffix:stop_suffix]
        except IndexError:
            raise IndexError

        for number in CONVERTER:
            if last < 0:
                # There's only one digit in the line
                if start_suffix > first:
                    if number in suffix:
                        line = line[:start_suffix] + suffix.replace(number, CONVERTER[number])
            elif start_suffix > last:
                if number in suffix:
                    line = line[:start_suffix] + suffix.replace(number, CONVERTER[number])

            if first < 0:
                # This line doesn't have any digits
                if number in prefix:
                    line = prefix.replace(number, CONVERTER[number]) + line[stop_prefix:]
                    start_suffix -= len(prefix) - 1
                    stop_suffix -= len(prefix) - 1
            elif start_prefix < first:
                if number in prefix:
                    line = prefix.replace(number, CONVERTER[number]) + line[stop_prefix:]
                    start_suffix -= len(prefix) - 1
                    stop_suffix -= len(prefix) - 1

        for number in CONVERTER:
            if number in line:
                line = line.replace(number, CONVERTER[number])

        return line

    def _get_converted_numbers(self, line: str) -> str:
        """
        Retrieves digits from spelled out numbers.
        """
        first, last = self._get_first_and_last_digits(line)

        positions = self._get_number_names_indexes(line)
    
        if positions:
            # There are numbers spelled out. Needs conversion.
            line = self._convert_line(line, positions, first[1], last[1])

        return self._get_numbers(line)

    def get_calibration_sum(self) -> int:
        """
        Adds all values from the lines to the calibration total.
        """
        for line in self.calibration:
            self.calibration_total += self._get_converted_numbers(line) if self.super else self._get_numbers(line)

        return self.calibration_total
