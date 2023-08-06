"""Main script for arexecute application."""


import argparse
from ctypes import ArgumentError

from .core import executer, recorder

INSTRUCTIONS = """(->) Denotes press first one key, then the next
                  Alt                - Stop recording any time
             W -> any number         - Add waiting time of seconds equal to the number, floats allowed with a dot
                   I                 - Starts writing anything, commands allowed
               Caps Lock             - Stops any action (for example set the final wait time or stop clicking)
                  Ctrl               - Move mouse to current mouse position
             Shift n times           - Clicks n times in the last mouse position or current if there were no movements before
                   v                 - Adds a variable to be defined later
"""


def main():
    parser = argparse.ArgumentParser(
        description="Record/Execute keyboard and mouse actions.",
        prog="Recorder/Executer",
    )

    parser.add_argument(
        "-e",
        action="store",
        dest="execute",
        default=None,
        help="Runs the execution recursively until process killed or for a number of iterations if -i option is specificed. No effect on recording.",
    )
    parser.add_argument(
        "-r", action="store", dest="record", default=None, help="Runs recording mode."
    )
    parser.add_argument(
        "-i",
        nargs="?",
        const=-1,
        default=1,
        action="store",
        dest="iterations",
        type=int,
        help="Sets the execution mode on with i iterations (defaults to 1 iteration when number not specified).",
    )

    args = parser.parse_args()

    if not ((args.execute is None) != (args.record is None)):
        raise ArgumentError(
            "Please specify either the -e option or the -r option with a filename (specify only one)."
        )

    print("\n========================ACTION RECORD EXECUTE========================\n")

    if args.execute is not None:
        json_filename = args.execute
        execute = True

    else:
        json_filename = args.record
        execute = False

    iterations = args.iterations

    if execute:
        e = executer.Executer(json_filename, verbose=1)
        if iterations == -1:
            while True:
                e.start()

        else:
            for _ in range(iterations):
                e.start()

    else:
        print(INSTRUCTIONS)
        r = recorder.Recorder(json_filename, verbose=1)
        r.start()

    input("Process finished successfully, press enter to leave...\n")


if __name__ == "__main__":
    main()
