import os
import sys
import time

from scratchcards import Scratchcards

def main():
    if len(sys.argv) < 2:
        raise ValueError("You need to inform the filename.")

    filename = sys.argv[-1]
    if not os.path.isfile(filename):
        raise ValueError("The last argument must be the filename.")

    scratchcards = Scratchcards(filename, "-p" in sys.argv)
    start_time = time.time()
    print(scratchcards.result())
    end_time = time.time()
    print(f"Run in {(end_time-start_time):.2f} s")


if __name__ == "__main__":
    main()