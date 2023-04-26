from datetime import datetime
import json
import re
import os
import Evtx.Evtx as evtx
import pandas as pd
import xmltodict
import tempfile


def findAllFoldersin(directory):
    # find all the folders in the directory
    folders = [directory]
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            folders.append(os.path.join(root, dir))
    return folders


def main():
    # find all the json files in /tmp/test and put the full path in a list
    # print("Enter the root directory to search for json files: ")
    # rootDir = input()
    print("Enter the root directory to search for json files: ")
    rootDir = input()
    # find all the json files in /tmp/test and put the full path in a list
    # print("Enter the root directory to search for json files: ")
    # rootDir = input()
    if rootDir == "":
        rootDir = "testFiles"
    dirs = findAllFoldersin(rootDir)

    jsonFiles = []
    installerLog_files = []
    windows_eventLog_files = []
    categorize_files_to_process(dirs, installerLog_files, jsonFiles, windows_eventLog_files)

    # loop through the list of json files
    for jsonFile in jsonFiles:
        sort_json_file(jsonFile)

    # loop through the list of installerLog files
    for installerLog_file in installerLog_files:
        if "_new" not in installerLog_file:
            fileExtension, fileName, filepath = extract_fileName_fileExt_filePath(installerLog_file)
            date = fileName[13:21]
            date_to_prepend = date[4:8] + "/" + date[2:4] + "/" + date[0:2]
            output_filename = installerLog_file[:-4] + "_new.log"
            change_installerLog_file(installerLog_file, date_to_prepend, output_filename)

    # loop through the list of windows_eventLog files
    for windows_eventLog_file in windows_eventLog_files:
        output_filename = windows_eventLog_file[:-5] + ".log"
        convert_windows_eventLog_files(windows_eventLog_file, output_filename)


def categorize_files_to_process(dirs, installerLog_files, jsonFiles, windows_eventLog_files):
    for dir in dirs:
        for root, dirs, files in os.walk(dir):
            for file in files:
                # if teh file contains \ then skip it
                # print(f"file: {file}")
                # if file contains \\ then skip it
                if "\\" in str(file):
                    continue
                else:
                    # if its a directory then skip it
                    if os.path.isdir(os.path.join(root, file)):
                        continue
                    # if its a file then add it to the list
                    else:
                        # check if the file contains json data by looking for the first character being a {
                        # print(os.path.join(root, file))
                        fileExtension = os.path.splitext(file)[1]
                        full_file_name = os.path.splitext(file)[0]
                        # print(fileExtension)
                        if re.search("InstallerLog_", full_file_name):
                            if not re.search("_new", full_file_name):
                                if os.path.join(root, file) not in installerLog_files:
                                    installerLog_files.append(os.path.join(root, file))

                        elif fileExtension == ".log":
                            try:
                                firstChar = open(os.path.join(root, file)).read(1)
                            except UnicodeDecodeError:
                                pass
                            else:
                                if firstChar == "{":
                                    # add the full path to the json file to the list
                                    if os.path.join(root, file) not in jsonFiles:
                                        jsonFiles.append(os.path.join(root, file))
                        elif fileExtension == ".evtx":
                            if os.path.join(root, file) not in windows_eventLog_files:
                                windows_eventLog_files.append(os.path.join(root, file))


def change_installerLog_file(input_file, date_to_prepend, output_file=None):
    if output_file is None:
        _, output_file = tempfile.mkstemp()

    # print(f"input_file {input_file} output_file {output_file} date_to_prepend {date_to_prepend}")

    with open(input_file, 'r', encoding="utf-16le") as infile, open(output_file, 'w') as outfile:
        # print(infile.read())
        infile = infile.readlines()
        for line in infile:
            time_match = re.search(r'\[\d{2}:\d{2}:\d{2}:\d{3}]', line)

            if time_match:
                time_field = time_match.group(0)
                time_value = time_field[1:-1]
                new_datetime = f"{date_to_prepend} {time_value}"
                modified_line = f"{new_datetime} {line}"
                outfile.write(modified_line)
            else:
                outfile.write(line)

        temp_file_name = outfile.name

    if output_file is None:
        os.replace(temp_file_name, input_file)
        print(f"Replaced {input_file} with {temp_file_name}")
    else:
        print(f"Created {output_file}")



def sort_json_file(jsonFile, create_new_file=True):
    output_file = None
    overwrite = False
    if create_new_file is False:
        _, output_file = tempfile.mkstemp()
        overwrite = True
    else:
        if "_sorted" not in jsonFile:
            fileExtension, fileName, filepath = extract_fileName_fileExt_filePath(jsonFile)
            output_file = str(filepath) + "/" + str(fileName) + "_sorted" + str(fileExtension)

    data_not_containing_time = []
    # open the json file
    if "_sorted" not in jsonFile:
        with open(jsonFile) as f:
            # load the json file with json objects separated by a newline
            data = [json.loads(line) for line in f]
            # Check if the line contains a @t field
            # if it does then check if the time format is correct
            for line in data:
                if "@t" in line:
                    try:
                        datetime.strptime(str(line['@t'])[:-2], "%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError:
                        # remove the line from the data array and add it to the data_containing_time as a tuple containing the line and also the following three lines
                        # if the line is the last line in the file then skip it
                        if data.index(line) + 3 < len(data):
                            data_not_containing_time.append((line, data[data.index(line) + 1], data[data.index(line) + 2], data[data.index(line) + 3]))
                            data.remove(line)
                else:
                    # remove the line from the data array and add it to the data_containing_time as a tuple containing the line and also the following three lines
                    if data.index(line) + 3 < len(data):
                        data_not_containing_time.append((line, data[data.index(line) + 1], data[data.index(line) + 2], data[data.index(line) + 3]))
                        data.remove(line)

        # print(data[0])

        # sort the array of json objects by the date field which has a date format of 2023-03-01T18:54:00.6550062Z
        try:
            data.sort(key=lambda x: datetime.strptime(str(x['@t'])[:-2], "%Y-%m-%dT%H:%M:%S.%f"))
        except ValueError:
            pass
        else:
            # Now add the lines that did not contain a @t field back into the data array in the same order they were in the original file
            for line in data_not_containing_time:
                # Take the 2nd, third, and 4th lines from the tuple and create a search string to find those lines in the data array - you must add a newline to the end of each line
                searchString = str(line[1]) + "\n" + str(line[2]) + "\n" + str(line[3]) + "\n"
                # find the index of the searchString in the data array
                index = data.index(searchString)
                # if the index is not found then add the line to the end of the data array
                if index == -1:
                    print(f"index not found for {searchString}")
                    data.append(line[0])
                else:
                    # insert the line into the data array at the index
                    data.insert(index, line[0])

            # write the sorted array of json objects to a new file in teh same path with each json object on a new line
            with open(output_file, 'w') as f:
                # remove existing contents of file if it exists
                if os.path.exists(output_file):
                    f.truncate(0)
                for item in data:
                    f.write("%s\n" % json.dumps(item))
            if overwrite is True:
                os.replace(output_file, jsonFile)


def extract_fileName_fileExt_filePath(jsonFile):
    # get the file path and name
    filepath, full_file_name = os.path.split(jsonFile)
    # get the file name and extension
    fileName, fileExtension = os.path.splitext(full_file_name)
    # print(f'filepath: {filepath} fileName: {fileName} fileExtension: {fileExtension}')
    return fileExtension, fileName, filepath

def convert_windows_eventLog_files(source_file, output_file):
    """Convert a single Windows EVTX event log file to a jsonLog format log file.
    :param source_file: The path to the source file
    :param output_file: The path to the output file
    """
    levels = {
        0: "Notice",
        1: "Debug",
        2: "Error",
        3: "Warning",
        4: "Info"
    }

    source_file_name = os.path.basename(source_file)
    records_list = []

    with evtx.Evtx(source_file) as log:
        record_length = 0
        for record in log.records():
            record_length += 1

        print(f"Processing {record_length} records from {source_file_name}...")

        for record_item, record in enumerate(log.records()):
            print(f"\rProcessing record {record_item} of {record_length} records from {source_file_name}...", end="")
            try:
                data_dict = xmltodict.parse(record.xml())
            except KeyError:
                pass
            input_datetime = datetime.strptime(f"{data_dict['Event']['System']['TimeCreated']['@SystemTime']}", "%Y-%m-%d %H:%M:%S.%f")
            # input_datetime = f"{input_datetime}0"
            # new time format matching 2023-03-21T16:05:10.0410469Z
            new_dict = {
                # remove the laast three characters from the time field so its the same as the rest of our logfiles.

                '@t': input_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "0Z",
                '@l': levels[int(data_dict['Event']['System']['Level'])],
                'EventID': data_dict['Event']['System']['EventID']['#text'],
                'sourceFile': source_file_name,
                'sourceType': 'win:evtx',
                'Provider': data_dict['Event']['System']['Provider']['@Name'],
                'Computer': data_dict['Event']['System']['Computer'],
                '@mt': data_dict['Event']
            }
            records_list.append(new_dict)

    df = pd.DataFrame(records_list)

    # Write DataFrame to JSON file with one record per line
    with open(output_file, "w") as outfile:
        for _, row in df.iterrows():
            json_record = row.to_json()
            outfile.write(json_record)
            outfile.write('\n')

    print("\nConverted " + source_file + " to " + output_file)


if __name__ == "__main__":
    main()