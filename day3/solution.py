import os
import sys

from schematics import Schematics

def main():
    if len(sys.argv) < 2:
        raise ValueError("You need to inform the filename.")

    filename = sys.argv[-1]
    if not os.path.isfile(filename):
        raise ValueError("The last argument must be the filename.")

    schematics = Schematics(filename, "-p" in sys.argv)
    print(schematics.result())


if __name__ == "__main__":
    main()