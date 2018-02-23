from . import Cli
import sys

if __name__ == "__main__":
    try:
        if sys.version_info < (3, 0):
            print("This program needs Python >= 3.0.")
        else:
            Cli.main()
    except KeyboardInterrupt:
        print("\nProgram exited by keyboard-interupt. Bye.")
