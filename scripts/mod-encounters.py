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
import string

HELP_MESSAGE = """
Change the Encounters for a gen 3 Pokemon Game - aith

Flags:
-h             --help
--list-groups                   List the uppermost encounter groups
--list-maps=<GROUPNAME>         List maps in a given group
--choose-groups                 Choose maps to modify, comma delimited
--choose-maps                   Choose maps to modify, comma delimited
--choose-all-maps               Choose all the maps in the FIRST group chosen
--delete-all-mons               Delete all encounters
--add-mons                      Add encounters with the format PKMN1-MINLVL1-MAXLVL1,PKMN2-MINLVL2-MAXLVL2
"""
# --groups <file_path>                 Show encounter groups
# --

DEFAULT_PATH = "../pokeemerald/src/data/wild_encounters.json"
DEFAULT_GROUP = "gWildMonHeaders"

DEFAULT_ENCOUNTER_RATE = 20
TERRAIN_GROUPS = ["land_mons", "fishing_mons", "water_mons", "rock_smash_mons"]

TAB1 = "   "

if __name__ == '__main__':
    argv = sys.argv[1:]

    # Get DEFAULT_PATH
    file_path = DEFAULT_PATH
    if len(argv) == 0 or argv[0][0] == "-":
        print("No path given: choosing script's DEFAULT_PATH")
        # if len(argv) > 1: argv = argv[1:]  # Remove from args

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
    try:
        char_opts = 'L:l:c:a:h:'
        long_opts = ['list-maps=', 'choose-all-maps', 'choose-maps=', 'choose-groups=', 'list-groups', "delete-mons", "delete-all-mons", "add-mons=", "save-to="]
        opts, args = getopt.getopt(argv, 'l:', long_opts)
    except getopt.GetoptError:
        print("Error processing args")
        print(HELP_MESSAGE)
        sys.exit(1)

    # Common Data
    all_groups = json_data['wild_encounter_groups']

    def guard_against_empty_arrays(arrays):
        for array in arrays:
            if len(array) == 0:
                print(
                    "Error: use --choose-groups=<GROUPNAME1>,<GROUPNAME2>,... and --choose-maps=<GROUPNAME1>,<GROUPNAME2>,... before modifying")
                sys.exit(1)

    def get_maps(chosen_groups, chosen_maps):
        found_maps = []
        for group_name in chosen_groups:
            group_i = 0
            for unk_group in all_groups:
                if unk_group['label'] == group_name:
                    break
                group_i += 1
            group_struct = json_data['wild_encounter_groups'][group_i]
            map_structs = group_struct['encounters']
            for map_name in chosen_maps:
                map_i = 0
                for unk_map in map_structs:
                    if unk_map['base_label'] == map_name:
                        break
                    map_i += 1
                found_map = map_structs[map_i]
                found_maps.append(found_map)
        return found_maps


    # Parse
    chosen_groups = [DEFAULT_GROUP]  # Default
    chosen_maps = []
    for opt, arg in opts:
        if opt in ['-h', '--h', '--help']:
            print(HELP_MESSAGE)
            sys.exit(0)
        elif opt in ['-L', '--list-groups']:
            print("Encounter groups are:")
            for group in all_groups:
                print(TAB1+group['label'])
        elif opt in ['-l', '--list-maps']:
            desired_group_name = arg
            def find_group(groups, desired_group_name):
                for group in groups:
                    if group["label"] == desired_group_name:
                        return group
                sys.exit(1)
            found_group = find_group(all_groups, desired_group_name)
            i = 0
            for encounter_data in found_group['encounters']:
                print(encounter_data["base_label"], end=' ')
                i+=1
                if i == 2:
                    print('') # newline
                    i = 0
        elif opt in ['-c', '--choose-groups']:
            chosen_groups = arg.split(',')
        elif opt in ['-c', '--choose-maps']:
            chosen_maps = arg.split(',')
        elif opt in ['-c', '--choose-all-maps']:
            chosen_maps = []
            desired_group_name = chosen_groups[0]
            def find_group(groups, desired_group_name):
                for group in groups:
                    if group["label"] == desired_group_name:
                        return group
                sys.exit(1)
            found_group = find_group(all_groups, desired_group_name)
            for encounter_data in found_group['encounters']:
                chosen_maps.append(encounter_data["base_label"])
        elif opt in ['-d', '--delete-mons']:
            print("--delete-mons isn't implemented")
            sys.exit(1)
        elif opt in ['-D', '--delete-all-mons']:
            guard_against_empty_arrays([chosen_maps, chosen_groups])
            maps_to_modify = get_maps(chosen_groups, chosen_maps)
            for map_to_modify in maps_to_modify:
                for terrain_group in TERRAIN_GROUPS:
                    if terrain_group in map_to_modify:
                        map_to_modify[terrain_group]['mons'].clear()
        # elif opt in ['-a', '--add-mons']:
        #     guard_against_empty_arrays([chosen_maps, chosen_groups])
        elif opt in ['-a', '--add-mons']:
            guard_against_empty_arrays([chosen_maps, chosen_groups])
            mons = arg.split(',')
            maps_to_modify = get_maps(chosen_groups, chosen_maps)
            for map_to_modify in maps_to_modify:
                for mon in mons:
                    mon_data = mon.split('-')
                    if len(mon_data) != 4:
                        print("Error: mon data formatted incorrectly. Exiting")
                        sys.exit(1)
                    mon_name, min_lvl, max_lvl, terrain_type = mon_data
                    if terrain_type not in TERRAIN_GROUPS:
                        print("Error: invalid terrain group. Must be in [land_mons, fishing_mons, water_mons, rock_smash_mons]. Exiting")
                    if not max_lvl.isnumeric() or not min_lvl.isnumeric():
                        print("Error: max lvl or min lvl aren't numeric. Exiting")
                        sys.exit(1)
                    if terrain_type not in map_to_modify:
                        map_to_modify[terrain_type] = {
                            "mons": [],
                            "encounter_rate": DEFAULT_ENCOUNTER_RATE
                        }
                    map_to_modify[terrain_type]['mons'].append({
                        "min_level": min_lvl,
                        "max_level": max_lvl,
                        "species": mon_name
                    })
        elif opt in ['-s', '--save-to']:
            save_path = arg
            save_file = open(save_path, 'w')
            json.dump(json_data, save_file, ensure_ascii=False, indent=4)
            print("saved to "+save_path)







