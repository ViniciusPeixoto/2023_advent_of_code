import os
import sys

from games import Games

def main():
    if len(sys.argv) < 2:
        raise ValueError("You need to inform the filename.")

    filename = sys.argv[-1]
    if not os.path.isfile(filename):
        raise ValueError("The last argument must be the filename.")

    with open("config") as config:
        configs = {line.split("=")[0].strip(): int(line.split("=")[1].strip()) for line in config.readlines()}

    games = Games(filename, configs, "-p" in sys.argv)
    print(games.verify())


if __name__ == "__main__":
    main()