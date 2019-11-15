# All of the imports requirements
import os.path
import csv
from tkinter import filedialog
from tkinter import *
import shutil
import json
import datetime

# Tkinter setup
window = Tk()
window.title('CSV Merge - STUNS Energi')
window.geometry('825x400')
window.configure(background='#9d9d9c')
window.resizable(width=False, height=False)
window.iconbitmap(r'img\stuns_e_icon.ico')

# All of the header presets are located here
# The CSV header preset for weather (WXT530)
weather_preset = ['systemTime,DN,DM,DX,SN,SM,SX,GT3U,GT41,GM41,GP41,RC,RD,RI,HC,HD,HI,RP,HP']

# The JSON header preset for weather (WXT530)
json_weather_preset = ['DN,DM,DX,SN,SM,SX,GT3U,GT41,GM41,GP41,RC,RD,RI,HC,HD,HI,RP,HP']

# The Schneider CSV header preset (Energy meter)
schneider_preset = ['systemTime,I1,I2,I3,U1_U2,U2_U3,U3_U1,'
                    'P1,P2,P3,PVAR,PVA,Pfa,'
                    'HZ,WHAI,WHAE,VARHI,VARHE,WHPAI,'
                    'WHPAE,WHAEI1,WHAEI2,WHAEI3,P']

# The Schneider JSON header preset (Energy meter)
json_schneider_preset = ['I1,I2,I3,U1_U2,U2_U3,U3_U1,P1,P2,P3,PVAR,PVA,Pfa,HZ,WHAI,WHAE,VARHI,VARHE,WHPAI,'
                         'WHPAE,WHAEI1,WHAEI2,WHAEI3,P']

# Cluster control unit 1 CSV header preset
unit1_preset = ['systemTime,V1_P1,V1_P2,V1_P3,V1_U1_L1_N,V1_U2_L2_N,V1_U3_L3_N,V1_HZ,'
                'V1_U1_L1_L2,V1_U2_L2_L3,V1_U3_L3_L1,V1_Itot,V1_I1,V1_I2,V1_I3,'
                'V1_Yield_Wh,V1_Yield_kWh,V1_Yield_MWh,'
                'V1_YieldDay_Wh,V1_YieldDay_kWh,V1_P']

# Cluster control unit 1 JSON header preset
json_unit1_preset = ['V1_P1,V1_P2,V1_P3,V1_U1_L1_N,V1_U2_L2_N,V1_U3_L3_N,V1_HZ,V1_U1_L1_L2,V1_U2_L2_L3,'
                     'V1_U3_L3_L1,V1_Itot,V1_I1,V1_I2,V1_I3,V1_Yield_kWh,V1_Yield_MWh,V1_YieldDay_kWh,'
                     'V1_PV,V1_P']

# Cluster control unit 2 CSV header preset
unit2_preset = ['systemTime,V2_P1,_V2_P2,V2_P3,V2_U1_L1_N,V2_U2_L2_N,V2_U3_L3_N,V2_HZ,'
                'V2_U1_L1_L2,V2_U2_L2_L3,V2_U3_L3_L1,V2_Itot,V2_I1,V2_I2,V2_I3,'
                'V2_Yield_Wh,V2_Yield_kWh,V2_Yield_MWh,'
                'V2_YieldDay_Wh,V2_YieldDay_kWh,V2_P']

# Cluster control unit 2 JSON header preset
json_unit2_preset = ['V2_P1,V2_P2,V2_P3,V2_U1_L1_N,V2_U2_L2_N,V2_U3_L3_N,V2_HZ,V2_U1_L1_L2,V2_U2_L2_L3,'
                     'V2_U3_L3_L1,V2_Itot,V2_I1,V2_I2,V2_I3,V2_Yield_kWh,V2_Yield_MWh,V2_YieldDay_kWh,'
                     'V2_PV,V2_P']

# Cluster control unit 3 CSV header preset
unit3_preset = ['systemTime,V3_P1,V3_P2,V3_P3,V3_U1_L1_N,V3_U2_L2_N,V3_U3_L3_N,V3_HZ,'
                'V3_U1_L1_L2,V3_U2_L2_L3,V3_U3_L3_L1,V3_I1,V3_I2,V3_I3,'
                'V3_Yield_Wh,V3_Yield_kWh,V3_Yield_MWh,'
                'V3_YieldDay_Wh,V3_YieldDay_kWh,V3_P']

# Cluster control unit 3 JSON header preset
json_unit3_preset = ['V3_P1,V3_P2,V3_P3,V3_U1_L1_N,V3_U2_L2_N,V3_U3_L3_N,V3_HZ,V3_U1_L1_L2,V3_U2_L2_L3,'
                     'V3_U3_L3_L1,V3_Itot,V3_I1,V3_I2,V3_I3,V3_Yield_kWh,V3_Yield_MWh,V3_YieldDay_kWh,'
                     'V3_PV,V3_P']

# Name bridge for CSV files (Between site id and date and data type)
bridge = ';'

# Folder search keywords
cluster_keyword = 'cluster'
schneider_keyword = 'schneider'
weather_keyword = 'vader'
temp_keyword = 'temp'

# File search keywords
cluster = 'Unit'
schneider = 'Schneider'
temp = 'Temp'
weather = 'WXT'

# The Temp. CSV header preset
temp_preset = ['systemTime,AmbTemp,ModTemp']

# The Temp. JSON header preset
json_temp_preset = ['AmbTemp,ModTemp']

# Variables for the DataList type names
weather_name = "Weather"
temp_name = "TempSensors"
cluster_name = "ClusterControl"
energy_name = "EnergyMeter"


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    global filename
    global directory
    global folder_list
    global folders
    directory = filedialog.askdirectory()
    display_directory = directory
    while len(display_directory) > 50:
        display_directory = display_directory[1:]
    if len(display_directory) >= 50:
        display_directory = '...' + display_directory
    folder_path.set(display_directory)
    print(directory)
    folders = []
    directory = directory + '/'

    for filename in os.listdir(directory):
        print(filename)
        if filename.__contains__(weather_keyword):
            folders.append(filename)

        elif filename.__contains__(schneider_keyword):
            folders.append(filename)

        elif filename.__contains__(cluster_keyword):
            folders.append(filename)

        elif filename.__contains__(temp_keyword):
            folders.append(filename)

        else:
            print(filename + " Does not match any of the keywords")

    if len(folders) == 0:
        print(os.path.basename(os.path.dirname(directory)))
        test = os.path.basename(os.path.dirname(directory))
        directory = directory.replace(test + '/', '')
        print(directory)
        test = test + '/'
        folders.append(test)

    folder_list = folders


def csv_merging():
    global cluster_list
    global schneider_list
    global temp_list
    global weather_list
    global merge1
    global merge2
    global merge3
    global merge4
    global to_be_merged
    global write
    global added

    cluster_list = []
    schneider_list = []
    temp_list = []
    weather_list = []

    for folder in folders:
        all_files = os.listdir(directory + folder)
        print(os.listdir(directory + folder))
        for file_name in all_files:

            if folder.__contains__(cluster_keyword):
                cluster_list.append(file_name)

            elif folder.__contains__(schneider_keyword):
                schneider_list.append(file_name)

            elif folder.__contains__(temp_keyword):
                temp_list.append(file_name)

            elif folder.__contains__(weather_keyword):
                weather_list.append(file_name)

            else:
                print(file_name)

        if folder.__contains__(schneider_keyword):
            print(len(schneider_list))
            x = 1
            per_merge = 4
            while x == 1:
                to_be_merged = schneider_list[:per_merge]
                # Removes the transferred Files
                del schneider_list[:per_merge]
                if len(schneider_list) == 0:
                    x = 0

                merge1 = open(directory + folder + '/' + to_be_merged[0], 'r')
                merge2 = open(directory + folder + '/' + to_be_merged[1], 'r')
                merge3 = open(directory + folder + '/' + to_be_merged[2], 'r')
                merge4 = open(directory + folder + '/' + to_be_merged[3], 'r')

                generated_filename = to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                with open(destination_filename + '/' + location_id + bridge + str(generated_filename) +
                          '.csv', 'w', newline='') as added:
                    print(generated_filename)
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    selected_preset = schneider_preset
                    write.writerow(selected_preset)

                    merge_4()

        elif folder.__contains__(cluster_keyword):
            per_merge = 3
            print(len(cluster_list))
            x = 1
            while x == 1:
                to_be_merged = cluster_list[:per_merge]
                # Removes the transferred Files
                del cluster_list[:per_merge]
                if len(cluster_list) == 0:
                    x = 0

                merge1 = open(directory + folder + '/' + to_be_merged[0], 'r')
                merge2 = open(directory + folder + '/' + to_be_merged[1], 'r')
                merge3 = open(directory + folder + '/' + to_be_merged[2], 'r')

                generated_filename = to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                with open(destination_filename + '/' + location_id + bridge + str(generated_filename) +
                          '.csv', 'w', newline='') as added:
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    print(generated_filename)

                    if generated_filename.endswith('1_'):
                        selected_preset = unit1_preset
                        write.writerow(selected_preset)

                    elif generated_filename.endswith('2_'):
                        selected_preset = unit2_preset
                        write.writerow(selected_preset)

                    elif generated_filename.endswith('3_'):
                        selected_preset = unit3_preset
                        write.writerow(selected_preset)

                    merge_3()

        elif folder.__contains__(weather_keyword):
            per_merge = 3
            print(len(weather_list))
            x = 1
            while x == 1:
                to_be_merged = weather_list[:per_merge]
                # Removes the transferred Files
                del weather_list[:per_merge]
                if len(weather_list) == 0:
                    x = 0

                merge1 = open(directory + folder + '/' + to_be_merged[0], 'r')
                merge2 = open(directory + folder + '/' + to_be_merged[1], 'r')
                merge3 = open(directory + folder + '/' + to_be_merged[2], 'r')

                generated_filename = to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                with open(destination_filename + '/' + location_id + bridge + str(generated_filename) +
                          '.csv', 'w', newline='') as added:
                    print(generated_filename)
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    selected_preset = weather_preset
                    write.writerow(selected_preset)

                    merge_3()

        elif folder.__contains__(temp_keyword):

            per_merge = 1
            print(len(temp_list))

            x = 1
            while x == 1:
                to_be_merged = temp_list[:per_merge]
                # Removes the transferred Files
                del temp_list[:per_merge]
                if len(temp_list) == 0:
                    x = 0

                merge1 = open(directory + folder + '/' + to_be_merged[0], 'r')

                generated_filename = to_be_merged[0]

                with open(destination_filename + '/' + location_id + bridge + str(generated_filename),
                          'w', newline='') as added:
                    print(generated_filename)
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    selected_preset = temp_preset
                    write.writerow(selected_preset)

                    add_header_temp()

        else:
            print("Folder name did not match our registry")


def add_header_temp():
    print(len(temp_list))
    for row in merge1:
        row = row.replace('\n', '')
        row_list = row.split(";")
        column2 = row_list[1]
        column2 = float(column2)
        column3 = row_list[2]
        column3 = float(column3)
        column2 = column2 / 100
        column3 = column3 / 100
        row_list = [row_list[0] + ',' + str(column2) + ',' + str(column3)]
        csv.writer(added)
        write.writerow(row_list)


def merge_3():
    print(len(cluster_list))
    print(len(weather_list))

    merge_3x = 0
    # Merges the different parts into one
    for (part1, part2, part3) in zip(merge1, merge2, merge3):
        part1 = "".join(part1)
        part2 = "".join(part2)
        part3 = "".join(part3)
        # Removes unnecessary residual code from somewhere
        part1 = part1.replace('\n', '')
        part2 = part2.replace('\n', '')
        part3 = part3.replace('\n', '')

        if part3.endswith(';'):
            part3 = part3[:-1]

        part1list = part1.split(";")
        part2list = part2.split(";")
        part3list = part3.split(";")

        first_file_timestamp = datetime.datetime.strptime(part1list[0], '%Y-%m-%d-%H:%M:%S.%f')
        first_file_timestamp = first_file_timestamp.timestamp()

        second_file_timestamp = datetime.datetime.strptime(part2list[0], '%Y-%m-%d-%H:%M:%S.%f')
        second_file_timestamp = second_file_timestamp.timestamp()

        combine1 = float(first_file_timestamp) - float(second_file_timestamp)
        combine1 = combine1 / 100

        third_file_timestamp = datetime.datetime.strptime(part3list[0], '%Y-%m-%d-%H:%M:%S.%f')
        third_file_timestamp = third_file_timestamp.timestamp()

        combine2 = float(first_file_timestamp) - float(third_file_timestamp)
        combine2 = combine2 / 100

        # Compares the different times
        if combine1 < 2.5 and combine2 < 2.5:
            # Removes the timestamps
            del part2list[0]
            del part3list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list]

            # Removes the brackets at the beginning and end
            complete = complete.pop(0)

            # Replaces the Error codes and Bad values with Null
            complete_list = []
            for cell in complete:
                if cell.__contains__('#NaN') or cell.__contains__(' ') or cell.__contains__('131070.0') \
                        or cell.__contains__('32768.0') or cell.__contains__('32.768') or cell.__contains__('1310.0') \
                        or cell.__contains__('131.0'):
                    cell = cell.replace(cell, 'Null')

                elif len(cell) == 0:
                    cell = cell.replace(cell, 'Null')

                complete_list.append(cell)

            # Converts the complete list to String
            complete_str = ','.join(map(str, complete_list))
            if complete_str.endswith(','):
                complete_str = complete_str[:-1]

            # Writes the line
            csv.writer(added)
            write.writerow([complete_str])

        else:
            print("Here some data did not add up")
            merge_3x += 1
            print("We have missed " + str(merge_3x) + " in total!")


def merge_4():
    print(len(schneider_list))
    merge_4x = 0

    # Merges the different parts into one
    for (part1, part2, part3, part4) in zip(merge1, merge2, merge3, merge4):
        part1 = "".join(part1)
        part2 = "".join(part2)
        part3 = "".join(part3)
        part4 = "".join(part4)
        # Removes unnecessary residual code from somewhere
        part1 = part1.replace('\n', '')
        part2 = part2.replace('\n', '')
        part3 = part3.replace('\n', '')
        part4 = part4.replace('\n', '')

        part1list = part1.split(";")
        part2list = part2.split(";")
        part3list = part3.split(";")
        part4list = part4.split(";")

        first_file_timestamp = datetime.datetime.strptime(part1list[0], '%Y-%m-%d-%H:%M:%S.%f')
        first_file_timestamp = first_file_timestamp.timestamp()

        second_file_timestamp = datetime.datetime.strptime(part2list[0], '%Y-%m-%d-%H:%M:%S.%f')
        second_file_timestamp = second_file_timestamp.timestamp()

        combine1 = float(first_file_timestamp) - float(second_file_timestamp)
        combine1 = combine1 / 100

        third_file_timestamp = datetime.datetime.strptime(part3list[0], '%Y-%m-%d-%H:%M:%S.%f')
        third_file_timestamp = third_file_timestamp.timestamp()

        fourth_file_timestamp = datetime.datetime.strptime(part4list[0], '%Y-%m-%d-%H:%M:%S.%f')
        fourth_file_timestamp = fourth_file_timestamp.timestamp()

        combine2 = float(third_file_timestamp) - float(fourth_file_timestamp)
        combine2 = combine2 / 100

        # Compares the different times
        if combine1 < 2.5 and combine2 < 2.5:
            # Removes the timestamps
            del part2list[0]
            del part3list[0]
            del part4list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list + part4list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)

            # Replaces the Error codes and Bad values with Null
            complete_list = []
            for cell in complete:
                if cell.__contains__(' ') or cell.__contains__('#NaN') or len(cell) == 0:
                    cell = cell.replace(cell, 'Null')

                # if len(complete_list) == 6:
                #     try:
                #         cell = float(cell)
                #         if cell > 52:
                #             cell = cell/100
                #             print(cell)
                #     except(TypeError, ValueError):
                #         pass

                complete_list.append(cell)

            if len(complete_list) < 25:
                complete_list.append('Null')

            # Converts the complete list to String
            complete_str = ','.join(map(str, complete_list))
            if complete_str.endswith(','):
                complete_str = complete_str[:-1]

            # Writes the line
            csv.writer(added)
            write.writerow([complete_str])
        else:
            print("Here some data did not add up")
            merge_4x += 1
            print("We have missed " + str(merge_4x) + " in total!")


def destination_browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global destination_filename
    global destination_folder_name
    global destination_folders

    destination_folders = []
    destination_folder_name = '/Generated'
    destination_filename = filedialog.askdirectory()
    display_directory = destination_filename
    while len(display_directory) > 50:
        display_directory = display_directory[1:]
    if len(display_directory) >= 50:
        display_directory = '...' + display_directory
    destination_folder_path.set(display_directory)
    print(destination_filename)
    destination_filename = destination_filename + destination_folder_name
    try:
        os.makedirs(destination_filename)
    except OSError:
        pass
    print(destination_filename)


def csv_folders():
    try:
        for new_dir in folders:
            created_dir = destination_filename + '/' + new_dir
            destination_folders.append(created_dir)
            os.mkdir(created_dir)
            print(created_dir)

    except OSError:
        pass


# This function moves every file in the destination folder to its righteous place
def generated_move():
    generated_file_list = []
    generated_folder_list = []
    cluster_folder = ''
    schneider_folder = ''
    temp_folder = ''
    weather_folder = ''

    find = os.listdir(destination_filename)
    for file in find:
        if file.endswith('.csv'):
            generated_file_list.append(file)
        elif file.endswith(''):
            generated_folder_list.append(file)

    for folder in generated_folder_list:
        if folder.__contains__(cluster_keyword):
            cluster_folder = folder

        elif folder.__contains__(schneider_keyword):
            schneider_folder = folder

        elif folder.__contains__(temp_keyword):
            temp_folder = folder

        elif folder.__contains__(weather_keyword):
            weather_folder = folder

    for move_file in generated_file_list:
        print(move_file)
        if move_file.__contains__(cluster):
            shutil.move(destination_filename + '/' + move_file, destination_filename + '/' +
                        cluster_folder + '/' + move_file)

        elif move_file.__contains__(schneider):
            shutil.move(destination_filename + '/' + move_file, destination_filename + '/' +
                        schneider_folder + '/' + move_file)

        elif move_file.__contains__(temp):
            shutil.move(destination_filename + '/' + move_file, destination_filename + '/' +
                        temp_folder + '/' + move_file)

        elif move_file.__contains__(weather):
            shutil.move(destination_filename + '/' + move_file, destination_filename + '/' +
                        weather_folder + '/' + move_file)

        else:
            print("Didn't match any of the above")

    print(generated_file_list)
    print(generated_folder_list)


# Generates the zip
def generate_zip():
    print(destination_filename)
    try:
        shutil.make_archive(destination_filename, 'zip', destination_filename)
    except OSError:
        print("Generated did not exist")
    try:
        shutil.rmtree(destination_filename)
    except OSError:
        pass

    json_destination = destination_filename[:-9]
    print(json_destination)
    try:
        shutil.make_archive(json_destination + 'Generatedjson', 'zip', json_destination + 'Generatedjson')
    except OSError:
        print("Generatedjson did not exist")
    try:
        shutil.rmtree(json_destination + 'Generatedjson')
    except OSError:
        print("Generatedjson did not exist")


# Checks if zip checkbox is checked
def zip_file():
    global create_zip
    create_zip = 0
    is_checked = zip_checking.get()

    if is_checked != str(0):
        create_zip = 1

    return create_zip


# Checks if file checking is checked
def perform_audit():
    global do_audit
    do_audit = 0
    is_checked = audit_check.get()
    print(is_checked)
    if is_checked == str(1):
        do_audit = 1

    else:
        do_audit = 0
    return do_audit


# Performs a check on all .CSV files pre CSV merging and/or JSON Generation
def generate_audit():
    print(directory + str(folders))
    file_list = []
    size = []
    rows_in_file = []
    check_these_files = []
    i = 0
    pre_destination = destination_filename[:-9]
    pre_destination = pre_destination + "PreGen/"
    print(pre_destination)
    try:
        os.mkdir(pre_destination)
    except OSError:
        pass
    this_header = ['Filename', 'Folder', 'Rows', 'Bytes']

    with open(pre_destination + "PreMergeDataInfo.json", 'w') as clearing:
        json.dump(' ', clearing, indent=2, ensure_ascii=False)
    # Opens the file info file and adds the header.
    with open(pre_destination + "PreMergeDataInfo.csv", 'w', newline='') as header:
        audit_write = csv.writer(header, delimiter=',', quotechar=' ')
        audit_write.writerows([this_header])

    for folder in folders:
        file_name = os.listdir(directory + folder)
        # A for loop that goes through every file that ends with .csv in the predefined folders
        for file in file_name:
            if file.endswith(".csv"):
                # Checks the size of the file in bytes
                size.append(os.stat(directory + folders[0 + i] + '/' + file).st_size)
                file_list.append(file)
                # Counts the number of lines in a file
                num_lines = sum(1 for line in open(directory + folders[0 + i] + '/' + file))
                rows_in_file.append(num_lines)
                # If the number of rows are less than 120k it will add the important info to a list
                if rows_in_file[0] < 120000:
                    check_these_files.append(str(rows_in_file[0]) + ', ' + file_list[0] + ',' + folder)

            # Writes a CSV file with the filename, folder name, number of rows and size in bytes
            with open(pre_destination + "PreMergeDataInfo.csv", 'a', newline='') as pm_csv_file:
                pre_merge = csv.writer(pm_csv_file, delimiter=',', quotechar=' ')
                complete = [file_list[0] + ", " + folder + ", " + str(rows_in_file[0]) + ", " + str(size[0])]
                pre_merge.writerows([complete])

            # Writes a json file with the filename, folder name, number of rows and size in bytes
            with open(pre_destination + "PreMergeDataInfo.json", 'a') as pm_json_file:
                while len(file_list) != 0:
                    # for sak in (file_list, rows_in_file, size):
                    all_data = {
                        "file": file_list[0],
                        "folder": folder,
                        "amount_rows": rows_in_file[0],
                        "bytes": size[0],
                    }
                    file_list.pop(0)
                    rows_in_file.pop(0)
                    size.pop(0)
                    # Dumps all the json data in the json file
                    json.dump(all_data, pm_json_file, indent=2, ensure_ascii=False)
        i += 1

        # Writes the text file for all in need of a check
    with open(pre_destination + "Potentially_Faulty.txt", 'w') as check_me:
        for i_file in check_these_files:
            check_me.write(i_file)
            check_me.write("\n")

        # Writes the CSV version for the storing of the files in need of a look
    with open(pre_destination + "Potentially_Faulty.csv", 'w') as check_me_csv:
        for i_file_csv in check_these_files:
            check_me_csv.write(i_file_csv)
            check_me_csv.write("\n")


# Checks if the result audit checkbox is checked
def perform_result_audit():
    global do_result_audit
    do_result_audit = 0
    is_checked = result_audit_check.get()
    if is_checked == str(1):
        do_result_audit = 1

    return do_result_audit


# Performs a check on all generated CSV files
def generate_result_audit():
    print(destination_filename)
    all_generated_folders = os.listdir(destination_filename)
    print(all_generated_folders)
    file_list = []
    size = []
    rows_in_file = []
    check_these_files = []
    i = 0
    post_destination = destination_filename[:-9]
    post_destination = post_destination + "PostGen/"
    print(post_destination)
    try:
        os.mkdir(post_destination)
    except OSError:
        pass

    this_header = ['Filename', 'Folder', 'Rows', 'Bytes']

    with open(post_destination + "PostMergeDataInfo.json", 'w') as clearing:
        json.dump(' ', clearing, indent=2, ensure_ascii=False)
    # Opens the file info file and adds the header.
    with open(post_destination + "PostMergeDataInfo.csv", 'w', newline='') as header:
        audit_write = csv.writer(header, delimiter=',', quotechar=' ')
        audit_write.writerows([this_header])

    for folder in all_generated_folders:
        all_generated_files = os.listdir(destination_filename + '/' + folder + '/')
        for file in all_generated_files:
            if file.endswith(".csv"):
                # Checks the size of the file in bytes
                size.append(os.stat(destination_filename + '/' + folder + '/' + file).st_size)
                file_list.append(file)
                # Counts the number of lines in a file
                num_lines = sum(1 for line in open(destination_filename + '/' + folder + '/' + file))
                rows_in_file.append(num_lines)
                # If the number of rows are less than 120k it will add the important info to a list
                if rows_in_file[0] < 120000:
                    check_these_files.append(str(rows_in_file[0]) + ', ' + file_list[0] + ',' +
                                             destination_filename + '/' + folder)

                # Writes a CSV file with the filename, folder name, number of rows and size in bytes
                with open(post_destination + "PostMergeDataInfo.csv", 'a', newline='') as post_csv_file:
                    post_merge = csv.writer(post_csv_file, delimiter=',', quotechar=' ')
                    complete = [file_list[0] + ", " + destination_filename + '/' + folder + ", " +
                                str(rows_in_file[0]) + ", " + str(size[0])]
                    post_merge.writerows([complete])

                # Writes a json file with the filename, folder name, number of rows and size in bytes
                with open(post_destination + "PostMergeDataInfo.json", 'a') as pm_json_file:
                    while len(file_list) != 0:
                        all_data = {
                            "file": file_list[0],
                            "folder": destination_filename,
                            "amount_rows": rows_in_file[0],
                            "bytes": size[0],
                        }
                        file_list.pop(0)
                        rows_in_file.pop(0)
                        size.pop(0)
                        # Dumps all the json data in the json file
                        json.dump(all_data, pm_json_file, indent=2, ensure_ascii=False)
                i += 1

                # Writes the text file for all in need of a check
            with open(post_destination + "Potentially_Faulty_Generated.txt", 'w') as check_me:
                for i_file in check_these_files:
                    check_me.write(i_file)
                    check_me.write("\n")

                # Writes the CSV version for the storing of the files in need of a look
            with open(post_destination + "Potentially_Faulty_Generated.csv", 'w') as check_me_csv:
                for i_file_csv in check_these_files:
                    check_me_csv.write(i_file_csv)
                    check_me_csv.write("\n")


# This function generates the json files
def generate_json():
    global json_selected_preset
    global json_merge1
    global json_merge2
    global json_merge3
    global json_merge4
    global json_added
    global json_schneider_list
    global json_type

    # All of the variables and lists for the json generation
    json_type = ""
    json_selected_preset = []
    json_schneider_list = []
    json_unit1_list = []
    json_unit2_list = []
    json_unit3_list = []
    json_wxt_list = []
    json_temp_list = []
    json_folder_list = []
    json_type_schneider = "EnergyMeter"
    json_type_wxt = "WXT530"
    json_type_cluster = "ClusterControl"
    json_type_temp = "IO"

    # Goes through each folder in the folders list
    for folder in folders:
        json_folder_list.append(folder)
        file_list = os.listdir(directory + folder)
        # Checks if the folder contains the following in name:
        for file in file_list:
            if file.__contains__("Schneider"):
                json_schneider_list.append(file)
            elif file.__contains__("Unit1"):
                json_unit1_list.append(file)
            elif file.__contains__("Unit2"):
                json_unit2_list.append(file)
            elif file.__contains__("Unit3"):
                json_unit3_list.append(file)
            elif file.__contains__("WXT"):
                json_wxt_list.append(file)
            elif file.__contains__("Temp"):
                json_temp_list.append(file)
            else:
                print("nope")
                print(file)

    # Readies the JSON for merging
    for json_folder in json_folder_list:
        print(json_folder_list)

        # Checks if the folder contains any of the following:
        if json_folder.__contains__(schneider_keyword):
            print("Schneider")
            while len(json_schneider_list) != 0:
                print(len(json_schneider_list))
                json_to_be_merged = json_schneider_list[:4]
                json_schneider_list = json_schneider_list[4:]
                json_selected_preset = json_schneider_preset
                json_type = json_type_schneider
                json_merge1 = open(directory + json_folder + '/' + json_to_be_merged[0], 'r')
                json_merge2 = open(directory + json_folder + '/' + json_to_be_merged[1], 'r')
                json_merge3 = open(directory + json_folder + '/' + json_to_be_merged[2], 'r')
                json_merge4 = open(directory + json_folder + '/' + json_to_be_merged[3], 'r')

                generated_filename = json_to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                with open(destination_filename + '/' + str(generated_filename) + '.json', 'w') \
                        as json_added:
                    json_merge_4()

        elif json_folder.__contains__(weather_keyword):
            print("Weather")
            while len(json_wxt_list) != 0:
                print(len(json_wxt_list))
                json_to_be_merged = json_wxt_list[:3]
                json_wxt_list = json_wxt_list[3:]
                json_selected_preset = json_weather_preset
                json_type = json_type_wxt
                json_merge1 = open(directory + json_folder + '/' + json_to_be_merged[0], 'r')
                json_merge2 = open(directory + json_folder + '/' + json_to_be_merged[1], 'r')
                json_merge3 = open(directory + json_folder + '/' + json_to_be_merged[2], 'r')

                generated_filename = json_to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                with open(destination_filename + '/' + str(generated_filename) + '.json', 'w', newline='') \
                        as json_added:
                    json_merge_3()

        elif json_folder.__contains__(cluster_keyword):
            print("Cluster")
            json_unit_list = json_unit1_list + json_unit2_list + json_unit3_list
            while len(json_unit_list) != 0:
                print(len(json_unit_list))
                json_to_be_merged = json_unit_list[:3]
                json_unit_list = json_unit_list[3:]

                json_merge1 = open(directory + json_folder + '/' + json_to_be_merged[0], 'r')
                json_merge2 = open(directory + json_folder + '/' + json_to_be_merged[1], 'r')
                json_merge3 = open(directory + json_folder + '/' + json_to_be_merged[2], 'r')

                generated_filename = json_to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                if generated_filename.__contains__('Unit1_'):
                    json_selected_preset = json_unit1_preset
                    json_type = json_type_cluster

                elif generated_filename.__contains__('Unit2_'):
                    json_selected_preset = json_unit2_preset
                    json_type = json_type_cluster

                elif generated_filename.__contains__('Unit3_'):
                    json_selected_preset = json_unit3_preset
                    json_type = json_type_cluster

                with open(destination_filename + '/' + str(generated_filename) + '.json', 'w', newline='') \
                        as json_added:
                    json_merge_3()

        elif json_folder.__contains__(temp_keyword):
            print("temp")
            per_merge = 1
            json_type = json_type_temp

            x = 1
            while x == 1:
                print(len(json_temp_list))
                json_to_be_merged = json_temp_list[:per_merge]
                # Removes the transferred Files
                del json_temp_list[:per_merge]
                if len(json_temp_list) == 0:
                    x = 0

                json_merge1 = open(directory + json_folder + '/' + json_to_be_merged[0], 'r')

                generated_filename = json_to_be_merged[0]
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                json_selected_preset = json_temp_preset

                with open(destination_filename + '/' + str(generated_filename) + '.json', 'w', newline='') \
                        as json_added:
                    json_merge_1()


# Function that removes the bad values from the tempgivare and converts it from CSV to JSON objects
def json_merge_1():
    for row in json_merge1:
        row = row.replace('\n', '')
        row_list = row.split(';')
        column2 = row_list[1]
        column2 = float(column2)
        column3 = row_list[2]
        column3 = float(column3)
        column2 = column2 / 100
        column3 = column3 / 100
        complete = [row_list[0], str(column2), str(column3)]

        all_data = complete
        json.dump(all_data, json_added, ensure_ascii=False)
        json_added.write('\n')


# Function for Cluster and Weather that merges and converts them from CSV to JSON
def json_merge_3():
    merge_3x = 0

    # Merges the different parts into one
    for (part1, part2, part3) in zip(json_merge1, json_merge2, json_merge3):
        part1 = "".join(part1)
        part2 = "".join(part2)
        part3 = "".join(part3)
        # Removes unnecessary residual code from somewhere
        part1 = part1.replace('\n', '')
        part2 = part2.replace('\n', '')
        part3 = part3.replace('\n', '')

        part1list = part1.split(";")
        part2list = part2.split(";")
        part3list = part3.split(";")

        first_file_timestamp = datetime.datetime.strptime(part1list[0], '%Y-%m-%d-%H:%M:%S.%f')
        first_file_timestamp = first_file_timestamp.timestamp()

        second_file_timestamp = datetime.datetime.strptime(part2list[0], '%Y-%m-%d-%H:%M:%S.%f')
        second_file_timestamp = second_file_timestamp.timestamp()

        combine1 = float(first_file_timestamp) - float(second_file_timestamp)
        combine1 = combine1 / 100

        third_file_timestamp = datetime.datetime.strptime(part3list[0], '%Y-%m-%d-%H:%M:%S.%f')
        third_file_timestamp = third_file_timestamp.timestamp()

        combine2 = float(first_file_timestamp) - float(third_file_timestamp)
        combine2 = combine2 / 100

        # Compares the different times
        if combine1 < 2.5 and combine2 < 2.5:
            # Removes the timestamps
            del part2list[0]
            del part3list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)
            # Replaces the Error codes and Bad values with Null
            complete_list = []
            for cell in complete:
                if cell.__contains__('#NaN') or cell.__contains__(' ') or cell.__contains__('131070.0') \
                        or cell.__contains__('32768.0') or cell.__contains__('32.768') or cell.__contains__('1310.0') \
                        or cell.__contains__('131.0'):
                    cell = cell.replace(cell, 'Null')
                complete_list.append(cell)

            # Converts the complete list to String
            complete_str = ','.join(map(str, complete_list))
            if complete_str.endswith(','):
                complete_str = complete_str[:-1]

            complete_str = complete_str.split(',')

            all_data = complete_str
            # Rock the Casbah
            json.dump(all_data, json_added, ensure_ascii=False)
            json_added.write('\n')
        else:
            print("Here some data did not add up")
            merge_3x += 1
            print("We have missed " + str(merge_3x) + " in total!")


# Function that merges and converts the Schneider data from CSV to JSON objects
def json_merge_4():
    merge_4x = 0

    # Merges the different parts into one
    for (part1, part2, part3, part4) in zip(json_merge1, json_merge2, json_merge3, json_merge4):
        part1 = "".join(part1)
        part2 = "".join(part2)
        part3 = "".join(part3)
        part4 = "".join(part4)
        # Removes unnecessary residual code from somewhere
        part1 = part1.replace('\n', '')
        part2 = part2.replace('\n', '')
        part3 = part3.replace('\n', '')
        part4 = part4.replace('\n', '')

        part1list = part1.split(";")
        part2list = part2.split(";")
        part3list = part3.split(";")
        part4list = part4.split(";")

        # Converts the dates to timestamps for better comparisons
        first_file_timestamp = datetime.datetime.strptime(part1list[0], '%Y-%m-%d-%H:%M:%S.%f')
        first_file_timestamp = first_file_timestamp.timestamp()

        second_file_timestamp = datetime.datetime.strptime(part2list[0], '%Y-%m-%d-%H:%M:%S.%f')
        second_file_timestamp = second_file_timestamp.timestamp()

        combine1 = float(first_file_timestamp) - float(second_file_timestamp)
        combine1 = combine1 / 100

        third_file_timestamp = datetime.datetime.strptime(part3list[0], '%Y-%m-%d-%H:%M:%S.%f')
        third_file_timestamp = third_file_timestamp.timestamp()

        fourth_file_timestamp = datetime.datetime.strptime(part4list[0], '%Y-%m-%d-%H:%M:%S.%f')
        fourth_file_timestamp = fourth_file_timestamp.timestamp()

        combine2 = float(third_file_timestamp) - float(fourth_file_timestamp)
        combine2 = combine2 / 100

        # Compares the different times
        if combine1 < 2.5 and combine2 < 2.5:
            # Removes the timestamps
            del part2list[0]
            del part3list[0]
            del part4list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list + part4list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)

            # Replaces the Error codes and Bad values with Null
            complete_list = []
            for cell in complete:
                if cell.__contains__(' ') or cell.__contains__('#NaN'):
                    cell = cell.replace(cell, 'Null')

                elif len(cell) == 0:
                    cell = cell.replace(cell, 'Null')

                complete_list.append(cell)

            if len(complete_list) < 25:
                complete_list.append('Null')

            # Converts the complete list to String
            complete_str = ','.join(map(str, complete_list))
            if complete_str.endswith(','):
                complete_str = complete_str[:-1]

            complete_str = complete_str.split(',')

            # Dumps the data in to JSON
            all_data = complete_str
            # Heart-Shaped Box
            json.dump(all_data, json_added, ensure_ascii=False)
            json_added.write('\n')
        else:
            print("Here some data did not add up")
            merge_4x += 1
            print("We have missed " + str(merge_4x) + " in total!")


def json_combine():
    json_all_files = []
    json_all_all_files = os.listdir(destination_filename)
    for file in json_all_all_files:
        if file.endswith('.json'):
            json_all_files.append(file)
    json_all_all_files.clear()
    json_merge = []
    compare_name = ''
    unit1 = ""
    unit2 = ""
    unit3 = ""
    temp_1 = ""
    schneider_1 = ""
    weather_1 = ""
    while len(json_all_files) > 0:
        # The list still remains for the second run which causes a infinite loop
        print(len(json_all_files))
        json_date = json_all_files[0]
        json_date = json_date[:10]
        print(json_date)
        while len(json_merge) < 6:
            if len(json_all_files) == 0:
                break
            elif json_all_files[0].__contains__(json_date):
                json_merge.append(json_all_files[0])
                del json_all_files[0]
            else:
                break

        for file in json_merge:
            if file.__contains__("Unit1"):
                unit1 = file
            elif file.__contains__("Unit2"):
                unit2 = file
            elif file.__contains__("Unit3"):
                unit3 = file
            elif file.__contains__("Temp"):
                temp_1 = file
            elif file.__contains__("Schneider"):
                schneider_1 = file
            elif file.__contains__("WXT"):
                weather_1 = file

            if len(unit1) == 0:
                print("Unit 1 is isn´t here")

        json_merge.clear()
        weather_file = []
        json_destination = destination_filename + "json/"

        # Tries to open all of the files
        # Works as long as the WXT exists (Weather)

        try:
            unit1_file = open(destination_filename + '/' + unit1, 'r')
        except OSError:
            print("Unit1 is missing!")
            unit1 = destination_filename + '/' + str(json_date) + "_Unit1.json"
            unit1_empty = ["Null", "Null", "Null", "Null", "Null", "Null",
                           "Null", "Null", "Null", "Null", "Null", "Null", "Null",
                           "Null", "Null", "Null", "Null", "Null", "Null", "Null"]
            num_lines = sum(1 for line in open(destination_filename + '/' + weather_1))
            x = 0
            unit1_create = open(unit1, 'w')
            while x < num_lines:
                json.dump(unit1_empty, unit1_create, ensure_ascii=False)
                # unit1_create.write(unit1_empty)
                unit1_create.write('\n')
                x += 1
            unit1_create.close()
            unit1_file = open(unit1, 'r')
        try:
            unit2_file = open(destination_filename + '/' + unit2, 'r')
        except OSError:
            print("Unit2 is missing!")
            unit2_empty = ["Null", "Null", "Null", "Null", "Null", "Null",
                           "Null", "Null", "Null", "Null", "Null", "Null", "Null",
                           "Null", "Null", "Null", "Null", "Null", "Null", "Null"]
            unit2 = destination_filename + '/' + str(json_date) + "_Tempgivare.json"
            num_lines = sum(1 for line in open(destination_filename + '/' + weather_1))
            x = 0
            unit2_create = open(unit2, 'w')
            while x < num_lines:
                json.dump(unit2_empty, unit2_create, ensure_ascii=False)
                unit2_create.write('\n')
                x += 1
            unit2_create.close()
            unit2_file = open(unit2, 'r')
        try:
            unit3_file = open(destination_filename + '/' + unit3, 'r')
        except OSError:
            print("Unit3 is missing!")
            unit3_empty = ["Null", "Null", "Null", "Null", "Null", "Null",
                           "Null", "Null", "Null", "Null", "Null", "Null", "Null",
                           "Null", "Null", "Null", "Null", "Null", "Null", "Null"]
            unit3 = destination_filename + '/' + str(json_date) + "_Tempgivare.json"
            num_lines = sum(1 for line in open(destination_filename + '/' + weather_1))
            x = 0
            unit3_create = open(unit3, 'w')
            while x < num_lines:
                json.dump(unit3_empty, unit3_create, ensure_ascii=False)
                unit3_create.write('\n')
                x += 1
            unit3_create.close()
            unit3_file = open(unit3, 'r')
        try:
            schneider_file = open(destination_filename + '/' + schneider_1, 'r')
        except OSError:
            print("Schneider is missing!")
            schneider_empty = "[Null,Null,Null]"
            schneider_1 = destination_filename + '/' + str(json_date) + "_Tempgivare.json"
            num_lines = sum(1 for line in open(destination_filename + '/' + weather_1))
            x = 0
            schneider_create = open(schneider_1, 'w')
            while x < num_lines:
                schneider_create.write(schneider_empty)
                schneider_create.write('\n')
                x += 1
            schneider_create.close()
            schneider_file = open(schneider_1, 'r')
        try:
            temp_file = open(destination_filename + '/' + temp_1, 'r')
        except OSError:
            print("Temp Is missing!")
            temp1_empty = "[Null,Null,Null]"
            temp1 = destination_filename + '/' + str(json_date) + "_Tempgivare.json"
            num_lines = sum(1 for line in open(destination_filename + '/' + weather_1))
            x = 0
            temp1_create = open(temp1, 'w')
            while x < num_lines:
                temp1_create.write(temp1_empty)
                temp1_create.write('\n')
                x += 1
            temp1_create.close()
            temp_file = open(temp1, 'r')
        try:
            weather_file = open(destination_filename + '/' + weather_1, 'r')
        except OSError:
            print("Weather is missing!")

        for (weather1, temp1, cluster1, cluster2, cluster3, energy_meter) \
                in zip(weather_file, temp_file, unit1_file, unit2_file, unit3_file, schneider_file):

            # Converts the input data of all data types to a list
            weather1 = weather1.replace("[", '')
            weather1 = weather1.replace("]", '')
            weather1 = weather1.replace('"', '')
            weather1 = weather1.replace(' ', '')
            weather1 = weather1.replace('\n', '')
            weather1 = weather1.split(',')
            if weather1[0].__contains__('Null'):
                weather1_timestamp = '2017-02-05-06:31:32.768'
            else:
                weather1_timestamp = weather1[0]
            del weather1[0]
            cell_list = []
            for cell in weather1:
                if cell.__contains__(',') or cell.__contains__('.'):
                    cell = cell.replace(",", ".")

                    try:
                        if cell.__contains__("Null"):
                            cell = None
                    except(TypeError, ValueError):
                        pass

                    try:
                        cell = float(cell)
                    except(ValueError, TypeError):
                        pass

                else:
                    try:
                        cell = int(cell)
                    except(ValueError, TypeError):
                        pass

                cell_list.append(cell)
            weather1 = cell_list

            temp1 = temp1.replace("[", '')
            temp1 = temp1.replace("]", '')
            temp1 = temp1.replace('"', '')
            temp1 = temp1.replace(' ', '')
            temp1 = temp1.replace('\n', '')
            temp1 = temp1.split(',')
            if temp1[0].__contains__('Null'):
                temp1_timestamp = weather1_timestamp
            else:
                temp1_timestamp = temp1[0]
            del temp1[0]
            cell_list = []
            for cell in temp1:
                if cell.__contains__(',') or cell.__contains__('.'):
                    cell = cell.replace(",", ".")
                    try:
                        cell = float(cell)
                    except(ValueError, TypeError):
                        pass

                else:
                    try:
                        cell = int(cell)
                    except(ValueError, TypeError):
                        pass

                try:
                    if cell.__contains__("Null"):
                        cell = None
                except(TypeError, ValueError):
                    pass

                cell_list.append(cell)
            temp1 = cell_list

            cluster1 = cluster1.replace("[", '')
            cluster1 = cluster1.replace("]", '')
            cluster1 = cluster1.replace('"', '')
            cluster1 = cluster1.replace(' ', '')
            cluster1 = cluster1.replace('\n', '')
            cluster1 = cluster1.split(',')
            if cluster1[0].__contains__('Null'):
                cluster1_timestamp = weather1_timestamp
            else:
                cluster1_timestamp = cluster1[0]
            del cluster1[0]
            cell_list = []
            for cell in cluster1:

                if cell.__contains__(',') or cell.__contains__('.'):
                    cell = cell.replace(",", ".")
                    try:
                        cell = float(cell)
                    except(ValueError, TypeError):
                        pass

                else:
                    try:
                        cell = int(cell)
                    except(ValueError, TypeError):
                        pass

                if len(cell_list) == 6:
                    try:
                        if cell > 52:
                            cell = cell/100
                    except(TypeError, ValueError):
                        pass

                try:
                    if cell.__contains__("Null"):
                        cell = None
                except(TypeError, ValueError):
                    pass

                cell_list.append(cell)
            cluster1 = cell_list

            cluster2 = cluster2.replace("[", '')
            cluster2 = cluster2.replace("]", '')
            cluster2 = cluster2.replace('"', '')
            cluster2 = cluster2.replace(' ', '')
            cluster2 = cluster2.replace('\n', '')
            cluster2 = cluster2.split(',')
            if cluster2[0].__contains__('Null'):
                cluster2_timestamp = weather1_timestamp
            else:
                cluster2_timestamp = cluster2[0]
            del cluster2[0]
            cell_list = []
            for cell in cluster2:

                if cell.__contains__(',') or cell.__contains__('.'):
                    cell = cell.replace(",", ".")

                    try:
                        cell = float(cell)
                    except(ValueError, TypeError):
                        pass

                else:
                    try:
                        cell = int(cell)
                    except(ValueError, TypeError):
                        pass

                try:
                    if cell.__contains__("Null"):
                        cell = None
                except:
                    pass

                if len(cell_list) == 6:
                    try:
                        if cell > 52:
                            cell = cell/100
                    except(TypeError, ValueError):
                        pass

                cell_list.append(cell)
            cluster2 = cell_list

            cluster3 = cluster3.replace("[", '')
            cluster3 = cluster3.replace("]", '')
            cluster3 = cluster3.replace('"', '')
            cluster3 = cluster3.replace(' ', '')
            cluster3 = cluster3.replace('\n', '')
            cluster3 = cluster3.split(',')
            if cluster3[0].__contains__('Null'):
                cluster3_timestamp = weather1_timestamp
            else:
                cluster3_timestamp = cluster3[0]
            del cluster3[0]
            cell_list = []
            for cell in cluster3:

                if cell.__contains__(',') or cell.__contains__('.'):
                    cell = cell.replace(",", ".")

                    try:
                        cell = float(cell)
                    except(ValueError, TypeError):
                        pass

                else:
                    try:
                        cell = int(cell)
                    except(ValueError, TypeError):
                        pass

                try:
                    if cell.__contains__("Null"):
                        cell = None
                except:
                    pass

                if len(cell_list) == 6:
                    try:
                        if cell > 52:
                            cell = cell/100
                    except(TypeError, ValueError):
                        pass

                cell_list.append(cell)
            cluster3 = cell_list

            energy_meter = energy_meter.replace("[", '')
            energy_meter = energy_meter.replace("]", '')
            energy_meter = energy_meter.replace('"', '')
            energy_meter = energy_meter.replace(' ', '')
            energy_meter = energy_meter.replace('\n', '')
            energy_meter = energy_meter.replace('\\u0019', '')
            energy_meter = energy_meter.split(',')
            if energy_meter[0].__contains__('Null'):
                energy_meter_timestamp = weather1_timestamp
            else:
                energy_meter_timestamp = energy_meter[0]
            del energy_meter[0]
            cell_list = []
            for cell in energy_meter:
                if cell.__contains__(',') or cell.__contains__('.'):
                    cell = cell.replace(",", ".")

                    try:
                        cell = float(cell)
                    except(ValueError, TypeError):
                        pass

                else:
                    try:
                        cell = int(cell)
                    except(ValueError, TypeError):
                        pass

                try:
                    if cell.__contains__("Null"):
                        cell = None
                except:
                    pass

                cell_list.append(cell)
            energy_meter = cell_list

            first_file_timestamp = datetime.datetime.strptime(weather1_timestamp, '%Y-%m-%d-%H:%M:%S.%f')
            first_file_timestamp_t = first_file_timestamp.timestamp()
            file_timestamp = weather1_timestamp[:-10]
            file_name = location_id + "-" + file_timestamp + ".json"
            folder_month_timestamp = file_timestamp[:-6]
            folder_month = folder_month_timestamp
            folder_day_timestamp = file_timestamp[:-3]
            folder_day = folder_day_timestamp

            # Timestamp conversion

            second_file_timestamp = datetime.datetime.strptime(temp1_timestamp, '%Y-%m-%d-%H:%M:%S.%f')
            second_file_timestamp_t = second_file_timestamp.timestamp()

            combine1 = float(first_file_timestamp_t) - float(second_file_timestamp_t)
            combine1 = combine1 / 100

            third_file_timestamp = datetime.datetime.strptime(cluster1_timestamp, '%Y-%m-%d-%H:%M:%S.%f')
            third_file_timestamp_t = third_file_timestamp.timestamp()

            fourth_file_timestamp = datetime.datetime.strptime(cluster2_timestamp, '%Y-%m-%d-%H:%M:%S.%f')
            fourth_file_timestamp_t = fourth_file_timestamp.timestamp()

            combine2 = float(third_file_timestamp_t) - float(fourth_file_timestamp_t)
            combine2 = combine2 / 100

            fifth_file_timestamp = datetime.datetime.strptime(cluster3_timestamp, '%Y-%m-%d-%H:%M:%S.%f')
            fifth_file_timestamp_t = fifth_file_timestamp.timestamp()

            sixth_file_timestamp = datetime.datetime.strptime(energy_meter_timestamp, '%Y-%m-%d-%H:%M:%S.%f')
            sixth_file_timestamp_t = sixth_file_timestamp.timestamp()

            combine3 = float(fifth_file_timestamp_t) - float(sixth_file_timestamp_t)
            combine3 = combine3 / 100

            # If true it will merge all of the data types
            if combine1 < 2.5 and combine2 < 2.5 and combine3 < 2.5 and combine1 > -2.5 \
                    and combine2 > -2.5 and combine3 > -2.5:
                json_weather_preset_str = ''.join(json_weather_preset)
                json_weather_preset_list = json_weather_preset_str.split(',')
                weather_dict = dict(zip(json_weather_preset_list, weather1))

                json_temp_preset_str = ''.join(json_temp_preset)
                json_temp_preset_list = json_temp_preset_str.split(',')
                temp1_dict = dict(zip(json_temp_preset_list, temp1))

                json_unit1_preset_str = ''.join(json_unit1_preset)
                json_unit1_preset_list = json_unit1_preset_str.split(',')
                cluster1_dict = dict(zip(json_unit1_preset_list, cluster1))

                json_unit2_preset_str = ''.join(json_unit2_preset)
                json_unit2_preset_list = json_unit2_preset_str.split(',')
                cluster2_dict = dict(zip(json_unit2_preset_list, cluster2))

                json_unit3_preset_str = ''.join(json_unit3_preset)
                json_unit3_preset_list = json_unit3_preset_str.split(',')
                cluster3_dict = dict(zip(json_unit3_preset_list, cluster3))

                json_energy_meter_preset_str = ''.join(json_schneider_preset)
                json_energy_meter_preset_list = json_energy_meter_preset_str.split(',')
                energy_meter_dict = dict(zip(json_energy_meter_preset_list, energy_meter))

                cluster_control = {**cluster1_dict, **cluster2_dict, **cluster3_dict}

                # All data puts all of the data types in to one for the json

                all_data = {"ID": location_id,
                            "timestamp": weather1_timestamp, "DataList": {weather_name: weather_dict,
                                                                          temp_name: temp1_dict,
                                                                          cluster_name: cluster_control,
                                                                          energy_name: energy_meter_dict}}

                # Tries to make the dirs
                if file_name != compare_name:
                    try:
                        os.makedirs(json_destination)
                    except OSError:
                        pass

                    try:
                        os.mkdir(json_destination + folder_month + '/')
                    except OSError:
                        pass
                    try:
                        os.mkdir(json_destination + folder_month + '/' + folder_day + '/')
                    except OSError:
                        pass
                    complete_json = open(json_destination + folder_month + '/' + folder_day + '/' + file_name, 'a')
                    json.dump(all_data, complete_json, indent=4, ensure_ascii=False)
                    complete_json.write('\n')
                    compare_name = file_name

                    # Opens and writes the Json
                else:
                    json.dump(all_data, complete_json, indent=4, ensure_ascii=False)
                    complete_json.write('\n')

def file_remove():
    # Removes the JSON files from Generated
    files = os.listdir(destination_filename + '/')
    for file in files:
        if file.endswith('json'):
            os.remove(destination_filename + '/' + file)
    if len(os.listdir(destination_filename + '/')) == 0:
        os.rmdir(destination_filename + '/')


# Takes the result from the Json checkbox
def json_file():
    global create_json
    create_json = 0
    is_checked = json_checkbox.get()
    if is_checked != str(0):
        create_json = 1


# Takes the result from the Json checkbox
def csv_file():
    global create_csv
    create_csv = 0
    is_checked = csv_checkbox.get()
    if is_checked != str(0):
        create_csv = 1


# Code for the id selection
def set_id():
    global location_id
    try:
        location_id = enter_id_entry.get()
    except (ValueError, TypeError):
        location_id = location_id = "A1157_AS3"

    if len(location_id) == 0:
        location_id = "A1157_AS3"


# Checks if the runs all the functions if the are selected
def generate():
    set_id()
    try:
        if do_audit == 1:
            generate_audit()
    except NameError:
        print("Do_audit Was not selected")

    try:
        if create_csv == 1:
            csv_folders()
            csv_merging()
    except NameError:
        print("Do CSV was not selected")

    generated_move()

    try:
        if create_json == 1:
            generate_json()
            json_added.close()
            json_combine()
            file_remove()
    except NameError:
        print("Do Json was not selected")

    try:
        if create_zip == 1:
            generate_zip()
    except NameError:
        print("Generate_Zip Was not selected")

    try:
        if do_result_audit == 1:
            generate_result_audit()
    except NameError:
        print("Do_result_audit was not selected")


# GUI Code for the folders which will be used
folder_path = StringVar()
select_folder_title = Label(text=" Select the folder: ", background='#9d9d9c')
select_folder_title.grid(row=1, column=1)
select_folder_title.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
select_folder_button = Button(text=" Select Folder ", command=browse_button)
select_folder_button.grid(row=1, column=4)
select_folder = Label(master=window, textvariable=folder_path)
select_folder.config(width=50)
select_folder.grid(row=1, column=2)

# GUI Code for the destination selection
destination_folder_path = StringVar()
select_destination_folder_title = Label(text=" Select the destination folder: ", background='#9d9d9c')
select_destination_folder_title.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
select_destination_folder_title.grid(row=2, column=1)
select_destination_folder_button = Button(text=" Select Folder ", command=destination_browse_button)
select_destination_folder_button.grid(row=2, column=4)
select_destination_folder = Label(master=window, textvariable=destination_folder_path)
select_destination_folder.config(width=50)
select_destination_folder.grid(row=2, column=2)

# GUI Code for the site id
enter_id_label = Label(window, text="Enter Site ID:", background='#9d9d9c')
enter_id_label.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
enter_id_label.grid(row=3, column=1)
enter_id_entry = Entry()
enter_id_entry.grid(row=3, column=2)
enter_id_confirm = Button(text="Confirm", command=set_id)
enter_id_confirm.grid(row=3, column=4)

# GUI Code for the ZIP creation of the generated files
zip_check = Label(text=" Do you want the results in a Zip?: ", background='#9d9d9c')
zip_check.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
zip_check.grid(row=6, column=1)
zip_checking = Variable(value=0)
zip_checked = Checkbutton(window, text='', variable=zip_checking, command=zip_file)
zip_checked.grid(row=6, column=2)

# GUI Code for the JSON generation checkbox
json_check = Label(text=" Do you want it as JSON?: ", background='#9d9d9c')
json_check.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
json_check.grid(row=4, column=1)
json_checkbox = Variable(value=0)
json_checked = Checkbutton(window, text='', variable=json_checkbox, command=json_file)
json_checked.grid(row=4, column=2)

# GUI Code for the CSV generation checkbox
csv_check = Label(text=" Do you want it as CSV?: ", background='#9d9d9c')
csv_check.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
csv_check.grid(row=5, column=1)
csv_checkbox = Variable(value=0)
csv_checked = Checkbutton(window, text='', variable=csv_checkbox, command=csv_file)
csv_checked.grid(row=5, column=2)

# GUI Code for file checking
audit = Label(text=" Do you want to perform a pre process check?: ", background='#9d9d9c')
audit.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
audit.grid(row=7, column=1)
audit_check = Variable(value=0)
audit_checked = Checkbutton(window, text='', variable=audit_check, command=perform_audit)
audit_checked.grid(row=7, column=2)

# GUI Code for the result check
result_audit = Label(text=" Do you want to perform a check on the resulting files?: ", background='#9d9d9c')
result_audit.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
result_audit.grid(row=8, column=1)
result_audit_check = Variable(value=0)
result_audit_checked = Checkbutton(window, text='', variable=result_audit_check, command=perform_result_audit)
result_audit_checked.grid(row=8, column=2)

# Creates a gap between the 2nd column and the buttons
spacing = Label(window, text="a", background='#9d9d9c')
spacing.config(font=("Helvetica", 6, "roman italic"), fg='#9d9d9c')
spacing.grid(row=999, column=3)

# GUI Code for the Generate button
generate_button = Button(window, text=" Generate ", command=generate)
generate_button.config(font=("Helvetica", 11, "roman italic"), fg='#e16b02')
generate_button.place(relx=.5, rely=.9, anchor='c')

window.mainloop()
