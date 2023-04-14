#!/usr/bin/env python3
import os

#  This script uses the python-evtx package to parse Windows Event Logs into a JSON format compatible with LNAV.
#  Included also is the LNAV parser for the converted event logs.
#  Written by Leon Letto (leonletto) with help/inspiration from the evtx_dump.py file written by Willi Ballenthin and the evtx_dump_json.py file written by AJ Read (ajread4).
#  This is designed to be used with the LNAV log viewer (https://lnav.org/) and to parse logs for the Workspace ONE UEM Hub (https://www.vmware.com/products/workspace-one.html).
#  The LNAV parser is designed to parse the JSON output of this script and therefore with work with any JSON output that is compatible with the LNAV parser.

import Evtx.Evtx as evtx
import xmltodict
import json


def convert_file(source_file, output_file):
    """Convert a single Windows EVTX event log file to a jsonLog format log file.
    :param source_file: The path to the source file
    :param output_file: The path to the output file
    """
    with evtx.Evtx(source_file) as log:
        # Get the filename of the source file and one folder up
        source_file_name = os.path.basename(source_file)

        levels = {
            0: "Notice",
            1: "Debug",
            2: "Error",
            3: "Warning",
            4: "Info"
        }

        # Instantiate the final json object
        final_json = []

        # Loop through each record in the evtx log
        for record in log.records():
            # Convert the record to a dictionary for ease of parsing
            data_dict = xmltodict.parse(record.xml())
            new_dict = {}
            eventDate = data_dict['Event']['System']['TimeCreated']['@SystemTime']
            provider = data_dict['Event']['System']['Provider']['@Name']
            level = data_dict['Event']['System']['Level']
            levelText = levels[int(level)]
            new_dict['@t'] = eventDate
            new_dict['@l'] = levelText
            new_dict['EventID'] = data_dict['Event']['System']['EventID']['#text']
            new_dict['sourceFile'] = source_file_name
            new_dict['sourceType'] = 'win:evtx'
            new_dict['Provider'] = provider
            new_dict['Computer'] = data_dict['Event']['System']['Computer']
            new_dict['@mt'] = data_dict['Event']

            # print(new_dict)

            final_json.append(new_dict)

        # Write to JSON file
        with open(output_file, "w") as outfile:
            for entry in final_json:
                json.dump(entry, outfile)
                outfile.write('\n')

        print("Converted " + source_file + " to " + output_file)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Pass in a folder and recursively convert all Windows EVTX event logs to jsonLog format logs.")
    parser.add_argument("folder", type=str, action='store',
                        help="Path to the folder containing Windows EVTX event log files")
    args = parser.parse_args()

    folder = args.folder


    for root, dirs, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(".evtx"):
                output_filename = full_path[:-5] + ".log"
                print(full_path)
                convert_file(full_path, output_filename)


if __name__ == "__main__":
    main()
