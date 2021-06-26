#! /usr/bin/python3
"""# Mod Pokemon Encounters Script by aith
Made for pret's gen3 decomps using the CLI
"""
__all__ = []
__author__ = "aith"
__version__ = "1.0"

import sys
import getopt
import json

HELP_MESSAGE = """
Change the Encounters for a gen 3 Pokemon Game - aith

Flags:
-h             --help
--list-groups                   List the uppermost encounter groups
"""
# --groups <file_path>                 Show encounter groups
# --

DEFAULT_PATH = "../pokeemerald/src/data/wild_encounters.json"

TAB1 = "   "

if __name__ == '__main__':
    argv = sys.argv[1:]

    # Get DEFAULT_PATH
    file_path = DEFAULT_PATH
    if len(argv) == 0 or argv[0][0] == "-":
        print("No path given: choosing script's DEFAULT_PATH")
        if len(argv) > 1: argv = argv[1:]  # Remove from args

    # Load Json
    def load_json(fp):
        try:
            f = open(file_path)
            json_data = json.load(f)
            return json_data
        except FileNotFoundError:
            print("First argument should be file path. Could not find file path. Exiting")
            sys.exit(1)

    json_data = load_json(file_path)

    # Get CLI args
    options = ['','list-groups', 'leavesign', 'inctick']
    try:
        opts, args = getopt.getopt(argv, 'a:t:s:f:',
                                   options)
    except getopt.GetoptError:
        help()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ['-h', '--h', '--help']:
            print(HELP_MESSAGE)
            sys.exit(0)
        elif opt == '--list-groups':
            groups = json_data['wild_encounter_groups']
            print("Encounter groups are:")
            for group in groups:
                print(TAB1+group['label'])


