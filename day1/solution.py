import os
import sys

from trebuchet import Trebuchet

def main():
    if len(sys.argv) < 2:
        raise ValueError("You need to inform the filename.")

    filename = sys.argv[-1]
    if not os.path.isfile(filename):
        raise ValueError("The last argument must be the filename.")

    trebuchet = Trebuchet(filename, "-c" in sys.argv)
    print(trebuchet.get_calibration_sum())


if __name__ == "__main__":
    main()