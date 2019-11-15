import os.path
import csv
from tkinter import filedialog
from tkinter import *
import shutil
import json
import datetime


window = Tk()
window.title('STUNS Energi - CSV Merge')
window.geometry('815x400')
window.configure(background='#9d9d9c')
window.resizable(width=False, height=False)
window.iconbitmap(r'img\stuns_e_icon.ico')


# All of the header presets are located here
weather_preset = ['systemTime, GW3U_DN, GW3U_DM, GW3U_DX, GW3U_SN, GW3U_SM, GW3U_SX, '
                  'GW3U_GT3U, GW3U_GT41, GW3U_GM41, GW3U_GP41, GW3U_RC, GW3U_RD, '
                  'GW3U_RI, GW3U_HC, GW3U_HD, GW3U_HI, GW3U_RP, GW3U_HP']

json_weather_preset = ['DN,DM,DX,SN,SM,SX,GT3U,GT41,GM41,GP41,RC,RD,RI,HC,HD,HI,RP,HP']

schneider_preset = ['systemTime, I1, I2, I3, U1_U2, U2_U3, U3_U1, '
                    'P1, P2, P3, PVAR, PVA, Pfa, '
                    'HZ, WHAI, WHAE, VARHI, VARHE, WHPAI, '
                    'WHPAE, WHAEI1, WHAEI2, WHAEI3, P']

json_schneider_preset = ['I1,I2,I3,U1_U2,U2_U3,U3_U1,U1_N,U2_N,P1,P2,P3,P,PVAR,PVA,PFA,'
                         'HZ,WHAI,WHAE,VARHI,VARHE,WHPAI,WHPAE,WHAEI1,WHAEI2,WHAEI3']

unit1_preset = ['systemTime, CCtrl_V1_P1, CCtrl_V1_P2, CCtrl_V1_P3, CCtrl_V1_U1_L1_N, '
                'CCtrl_V1_U2_L2_N, CCtrl_V1_U3_L3_N, CCtrl_V1_HZ, '
                'CCtrl_V1_U1_L1_L2, CCtrl_V1_U2_L2_L3, CCtrl_V1_U3_L3_L1, CCtrl_V1_Itot, '
                'CCtrl_V1_I1, CCtrl_V1_I2, CCtrl_V1_I3, '
                'CCtrl_V1_Yield_Wh, CCtrl_V1_Yield_kWh, CCtrl_V1_Yield_MWh, '
                'CCtrl_V1_YieldDay_Wh, CCtrl_V1_YieldDay_kWh, CCtrl_V1_P']

json_unit1_preset = ['V1_P,V1_P1,V1_P2,V1_P3,V1_U1_L1_N,V1_U2_L2_N,V1_U3_L3_N,V1_U1_L1_L2,V1_U2_L2_L3,'
                     'V1_U3_L3_L1,V1_Itot,V1_I1,V1_I2,V1_I3,V1_Yield_kWh,V1_Yield_MWh,V1_YieldDay_kWh,'
                     'V1_PV,V1_HZ']

unit2_preset = ['systemTime, CCtrl_V2_P1, _CCtrl_V2_P2, CCtrl_V2_P3, CCtrl_V2_U1_L1_N, CCtrl_V2_U2_L2_N, '
                'CCtrl_V2_U3_L3_N, CCtrl_V2_HZ, '
                'CCtrl_V2_U1_L1_L2, CCtrl_V2_U2_L2_L3, CCtrl_V2_U3_L3_L1, CCtrl_V2_Itot, '
                'CCtrl_V2_I1, CCtrl_V2_I2, CCtrl_V2_I3,'
                'CCtrl_V2_Yield_Wh, CCtrl_V2_Yield_kWh, CCtrl_V2_Yield_MWh, '
                'CCtrl_V2_YieldDay_Wh, CCtrl_V2_YieldDay_kWh, CCtrl_V2_P']

json_unit2_preset = ['V2_P,V2_P1,V2_P2,V2_P3,V2_U1_L1_N,V2_U2_L2_N,V2_U3_L3_N,V2_U1_L1_L2,V2_U2_L2_L3,'
                     'V2_U3_L3_L1,V2_Itot,V2_I1,V2_I2,V2_I3,V2_Yield_kWh,V2_Yield_MWh,V2_YieldDay_kWh,'
                     'V2_PV,V2_HZ']

unit3_preset = ['systemTime, CCtrl_V3_P1, CCtrl_V3_P2, CCtrl_V3_P3, CCtrl_V3_U1_L1_N, '
                'CCtrl_V3_U2_L2_N, CCtrl_V3_U3_L3_N, CCtrl_V3_HZ,'
                'CCtrl_V3_U1_L1_L2, CCtrl_V3_U2_L2_L3, CCtrl_V3_U3_L3_L1, CCtrl_V3_I1, '
                'CCtrl_V3_I2, CCtrl_V3_I3, '
                'CCtrl_V3_Yield_Wh, CCtrl_V3_Yield_kWh, CCtrl_V3_Yield_MWh, '
                'CCtrl_V3_YieldDay_Wh, CCtrl_V3_YieldDay_kWh, CCtrl_V3_P, CCtrl_V3_HZ']

json_unit3_preset = ['V3_P,V3_P1,V3_P2,V3_P3,V3_U1_L1_N,V3_U2_L2_N,V3_U3_L3_N,V3_U1_L1_L2,V3_U2_L2_L3,'
                     'V3_U3_L3_L1,V3_Itot,V3_I1,V3_I2,V3_I3,V3_Yield_kWh,V3_Yield_MWh,V3_YieldDay_kWh,'
                     'V3_PV,V3_HZ']

temp_preset = ['systemTime, GT41_MV, GT42_MV']

json_temp_preset = ['GT41_MV,GT42_MV']

# The location id could be improved
location_id = "A1157_AS3"


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
        if filename.__contains__('vader'):
            folders.append(filename)

        elif filename.__contains__('schneider'):
            folders.append(filename)

        elif filename.__contains__('cluster'):
            folders.append(filename)

        elif filename.__contains__("temp"):
            folders.append(filename)

        else:
            print(filename + "You don't belong here")

    print(folders)
    folder_list = folders
    print(directory)


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
    cluster = 'cluster'
    schneider = 'schneider'
    temp = 'temp'
    weather = 'vader'

    for folder in folders:
        all_files = os.listdir(directory + folder)
        for file_name in all_files:

            if folder.__contains__(cluster):
                cluster_list.append(file_name)

            elif folder.__contains__(schneider):
                schneider_list.append(file_name)

            elif folder.__contains__(temp):
                temp_list.append(file_name)

            elif folder.__contains__(weather):
                weather_list.append(file_name)

            else:
                print(file_name)

        if folder.__contains__(schneider):
            print(schneider_list)
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

                with open(destination_filename + '/' + str(generated_filename) + '.csv', 'w', newline='') as added:
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    selected_preset = schneider_preset
                    write.writerow(selected_preset)

                    merge_4()

        elif folder.__contains__(cluster):
            print(cluster_list)
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

                with open(destination_filename + '/' + str(generated_filename) + '.csv', 'w', newline='') as added:
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

        elif folder.__contains__(weather):
            print(weather_list)
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

                with open(destination_filename + '/' + str(generated_filename) + '.csv', 'w', newline='') as added:
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    selected_preset = weather_preset
                    write.writerow(selected_preset)

                    merge_3()

        elif folder.__contains__(temp):

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

                with open(destination_filename + '/' + str(generated_filename), 'w', newline='') as added:
                    write = csv.writer(added, delimiter=',', quotechar=' ')

                    selected_preset = temp_preset
                    write.writerow(selected_preset)

                    add_header_temp()

        else:
            print("Folder name did not match our registry")


def add_header_temp():
    for row in merge1:
        row = row.replace('\n', '')
        row_list = row.split(";")
        column2 = row_list[1]
        column2 = float(column2)
        column3 = row_list[2]
        column3 = float(column3)
        column2 = column2/100
        column3 = column3/100
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

        part1list = part1.split(";")
        part2list = part2.split(";")
        part3list = part3.split(";")

        first_file_timestamp = datetime.datetime.strptime(part1list[0], '%Y-%m-%d-%H:%M:%S.%f')
        first_file_timestamp = first_file_timestamp.timestamp()

        second_file_timestamp = datetime.datetime.strptime(part2list[0], '%Y-%m-%d-%H:%M:%S.%f')
        second_file_timestamp = second_file_timestamp.timestamp()

        combine1 = float(first_file_timestamp) - float(second_file_timestamp)
        combine1 = combine1/100

        third_file_timestamp = datetime.datetime.strptime(part3list[0], '%Y-%m-%d-%H:%M:%S.%f')
        third_file_timestamp = third_file_timestamp.timestamp()

        combine2 = float(first_file_timestamp) - float(third_file_timestamp)
        combine2 = combine2/100

        # Compares the different times --!Should probably be improved!--
        if combine1 < 2.5 and combine2 < 2.5:
            # Removes the timestamps
            del part2list[0]
            del part3list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)
            complete_str = ','.join(map(str, complete))

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
        combine1 = combine1/100

        third_file_timestamp = datetime.datetime.strptime(part3list[0], '%Y-%m-%d-%H:%M:%S.%f')
        third_file_timestamp = third_file_timestamp.timestamp()

        fourth_file_timestamp = datetime.datetime.strptime(part4list[0], '%Y-%m-%d-%H:%M:%S.%f')
        fourth_file_timestamp = fourth_file_timestamp.timestamp()

        combine2 = float(third_file_timestamp) - float(fourth_file_timestamp)
        combine2 = combine2/100

        # Compares the different times --!Should probably be improved!--
        if combine1 < 2.5 and combine2 < 2.5:
            # Removes the timestamps
            del part2list[0]
            del part3list[0]
            del part4list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list + part4list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)
            complete_str = ','.join(map(str, complete))

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
    cluster = 'Unit'
    schneider = 'Schneider'
    temp = 'Temp'
    weather = 'WXT'
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
        if folder.__contains__("cluster"):
            cluster_folder = folder

        elif folder.__contains__("schneider"):
            schneider_folder = folder

        elif folder.__contains__("temp"):
            temp_folder = folder

        elif folder.__contains__("vader"):
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


def generate_zip():
    print(destination_filename)
    shutil.make_archive(destination_filename + 'Generated', 'zip', destination_filename)


def zip_file():
    global create_zip
    create_zip = 0
    is_checked = zip_checking.get()

    if is_checked != str(0):
        create_zip = 1

    return create_zip


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


def generate_audit():
    print(directory + str(folders))
    file_list = []
    size = []
    rows_in_file = []
    check_these_files = []
    i = 0
    x = 0
    print(x)

    this_header = ['Filename', 'Folder', 'Rows', 'Bytes']

    with open(destination_filename + "PreMergeDataInfo.json", 'w') as clearing:
        json.dump(' ', clearing, indent=2, ensure_ascii=False)
    # Opens the file info file and adds the header.
    with open(destination_filename + "PreMergeDataInfo.csv", 'w', newline='') as header:
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
            with open(destination_filename + "PreMergeDataInfo.csv", 'a', newline='') as csv_file:
                pre_merge = csv.writer(csv_file, delimiter=',', quotechar=' ')
                complete = [file_list[0] + ", " + folder + ", " + str(rows_in_file[0]) + ", " + str(size[0])]
                pre_merge.writerows([complete])

            # Writes a json file with the filename, folder name, number of rows and size in bytes
            with open(destination_filename + "PreMergeDataInfo.json", 'a') as json_file:
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
                    json.dump(all_data, json_file, indent=2, ensure_ascii=False)
        i += 1

        # Writes the text file for all in need of a check
    with open(destination_filename + "Potentially_Faulty.txt", 'w') as check_me:
        for i_file in check_these_files:
            check_me.write(i_file)
            check_me.write("\n")

        # Writes the CSV version for the storing of the files in need of a look
    with open(destination_filename + "Potentially_Faulty.csv", 'w') as check_me_csv:
        for i_file_csv in check_these_files:
            check_me_csv.write(i_file_csv)
            check_me_csv.write("\n")


def perform_result_audit():
    global do_result_audit
    do_result_audit = 0
    is_checked = result_audit_check.get()
    if is_checked == str(1):
        do_result_audit = 1

    return do_result_audit


def generate_result_audit():
    print(destination_filename)
    all_generated_folders = os.listdir(destination_filename)
    print(all_generated_folders)
    file_list = []
    size = []
    rows_in_file = []
    check_these_files = []
    i = 0
    x = 0
    print(x)

    this_header = ['Filename', 'Folder', 'Rows', 'Bytes']

    with open(destination_filename + "PostMergeDataInfo.json", 'w') as clearing:
        json.dump(' ', clearing, indent=2, ensure_ascii=False)
    # Opens the file info file and adds the header.
    with open(destination_filename + "PostMergeDataInfo.csv", 'w', newline='') as header:
        audit_write = csv.writer(header, delimiter=',', quotechar=' ')
        audit_write.writerows([this_header])

        # S T A R T   H E R E
        
    for folder in all_generated_folders:
        all_generated_files = os.listdir(destination_filename + '/' + folder + '/')
        for file in all_generated_files:
            if file.endswith(".csv"):

                weather_list = "".join(weather_preset)
                weather_list = weather_list.split(",")
                schneider_list = "".join(schneider_preset)
                schneider_list = schneider_list.split(",")
                unit1_list = "".join(unit1_preset)
                unit1_list = unit1_list.split(",")
                unit2_list = "".join(unit2_preset)
                unit2_list = unit2_list.split(",")
                unit3_list = "".join(unit3_preset)
                unit3_list = unit3_list.split(",")
                temp_list = "".join(temp_preset)
                temp_list = temp_list.split(",")

                faulty_list = []

                count_col = open(destination_filename + '/' + folder + '/' + file)
                row_number = 0
                for row in count_col:
                    row_number += 1
                    row = row.replace('\n', '')
                    rowlist = row.split(",")
                    del rowlist[-1]

                    # list to string and format for writing out on csv file
                    def format_list_strg(self, binary):
                        print(binary, "BIN!")

                        list_to_length = str(len(self))
                        deed = "Length:" + list_to_length
                        # binary should only be 0 or 1,
                        if binary == 1:
                            deed += "\n"

                        return deed

                    binary_selector_headlist = 0
                    binary_selector_rowlist = 1
                    location_format = "Location " + str(destination_filename) + ","

                    # Checks if lists match in length if not then adds to faulty_list
                    if file.__contains__("WXT"):
                        if len(weather_list) - 1 == len(rowlist):
                            print("WXT Weather contains:")
                            print(file)
                            print(len(weather_list))
                            print(len(rowlist))
                            faulty_list += "WXT Weather contains: "
                            faulty_list += str(file)
                            faulty_list += format_list_strg(weather_list, binary_selector_headlist)
                            faulty_list += format_list_strg(rowlist, binary_selector_rowlist)
                            faulty_list += location_format

                    elif file.__contains__("Schneider"):
                        if len(schneider_list) - 1 == len(rowlist):
                            print("Schneider contains:")
                            print(file)
                            print(len(rowlist))
                            print(len(schneider_list))
                            faulty_list += "Schneider contains: "
                            faulty_list += str(file)
                            faulty_list += format_list_strg(schneider_list, binary_selector_headlist)
                            faulty_list += format_list_strg(rowlist, binary_selector_rowlist)
                            faulty_list += location_format

                    elif file.__contains__("Unit1"):
                        if len(unit1_list) - 1 == len(rowlist):
                            print("UNIT 1 contains")
                            print(file)
                            print(len(unit1_list))
                            print(len(rowlist))
                            faulty_list += "UNIT 1 contains: "
                            faulty_list += str(file)
                            faulty_list += format_list_strg(unit1_list, binary_selector_headlist)
                            faulty_list += format_list_strg(rowlist, binary_selector_rowlist)
                            faulty_list += location_format

                    elif file.__contains__("Unit2"):
                        if len(unit2_list) - 1 == len(rowlist):
                            print("UNIT 2 contains")
                            print(file)
                            print(len(unit2_list))
                            print(len(rowlist))
                            faulty_list += "UNIT 2 contains: "
                            faulty_list += str(file)
                            faulty_list += format_list_strg(unit2_list, binary_selector_headlist)
                            faulty_list += format_list_strg(rowlist, binary_selector_rowlist)
                            faulty_list += location_format

                    elif file.__contains__("Unit3"):
                        if len(unit3_list) - 1 == len(rowlist):
                            print("UNIT 3 contains")
                            print(file)
                            print(len(unit3_list))
                            print(len(rowlist))
                            faulty_list += "UNIT 3 contains: "
                            faulty_list += str(file)
                            faulty_list += format_list_strg(unit3_list, binary_selector_headlist)
                            faulty_list += format_list_strg(rowlist, binary_selector_rowlist)
                            faulty_list += location_format

                    elif file.__contains__("Temp"):
                        if len(temp_list) - 1 == len(rowlist):
                            print("TEMP contains")
                            print(file)
                            print(len(temp_list))
                            print(len(rowlist))
                            faulty_list += "TEMP contains: "
                            faulty_list += str(file)
                            faulty_list += format_list_strg(temp_list, binary_selector_headlist)
                            faulty_list += format_list_strg(rowlist, binary_selector_rowlist)
                            faulty_list += location_format

                    else:
                        print("Nothing matched")

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
  
                # Creates new .csv file,dumps data with non matching header and lists in "LEN"
                with open(destination_filename + "NonMatchingHeader&Lists.csv", 'a', newline='') as weekly_data_output:
                    for i in faulty_list:
                        weekly_data_output.write(i)

                # Writes a CSV file with the filename, folder name, number of rows and size in bytes

                with open(destination_filename + "PostMergeDataInfo.csv", 'a', newline='') as csv_file:
                    post_merge = csv.writer(csv_file, delimiter=',', quotechar=' ')
                    complete = [file_list[0] + ", " + destination_filename + '/' + folder + ", " +
                                str(rows_in_file[0]) + ", " + str(size[0])]
                    post_merge.writerows([complete])

                # Writes a json file with the filename, folder name, number of rows and size in bytes
                with open(destination_filename + "PostMergeDataInfo.json", 'a') as pm_json_file:
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

                # Writes the text file for all in need of a check
            with open(destination_filename + "Potentially_Faulty_Generated.txt", 'w') as check_me:
                for i_file in check_these_files:
                    check_me.write(i_file)
                    check_me.write("\n")

                # Writes the CSV version for the storing of the files in need of a look
            with open(destination_filename + "Potentially_Faulty_Generated.csv", 'w') as check_me_csv:
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
    global writing
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
    json_to_be_merged = []
    json_folder_list = []
    json_type_schneider = "EnergyMeter"
    json_type_wxt = "WXT530"
    json_type_cluster = "ClusterControl"
    json_type_temp = "IO"

    # END HERE ?
    
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
        if json_folder.__contains__('schneider'):
            print("Schneider")
            while len(json_schneider_list) != 0:
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

                # Tries to make a new dir for the json files
                try:
                    os.makedirs(destination_filename + '/' + 'json' + json_folder)
                except OSError:
                    pass

                with open(destination_filename + '/' + 'json' + json_folder +
                          '/' + str(generated_filename) + '.json', 'w', newline='') \
                        as json_added:
                    print(destination_filename + '/' + 'json' + json_folder + '/' + str(generated_filename) + '.json')
                    json_merge_4()

        elif json_folder.__contains__('vader'):
            print("Weather")
            while len(json_wxt_list) != 0:
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

                # Tries to make a new dir for the files
                try:
                    os.makedirs(destination_filename + '/' + 'json' + json_folder)
                except OSError:
                    pass

                with open(destination_filename + '/' + 'json' + json_folder +
                          '/' + str(generated_filename) + '.json', 'w', newline='') \
                        as json_added:
                    print(destination_filename + '/' + 'json' + json_folder + '/' + str(generated_filename) + '.json')
                    json_merge_3()

        elif json_folder.__contains__('cluster'):
            print("Cluster")
            json_unit_list = json_unit1_list + json_unit2_list + json_unit3_list
            while len(json_unit_list) != 0:
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

                # Tries to make a new dir for the files
                try:
                    os.makedirs(destination_filename + '/' + 'json' + json_folder)
                except OSError:
                    pass

                with open(destination_filename + '/' + 'json' + json_folder +
                          '/' + str(generated_filename) + '.json', 'w', newline='') \
                        as json_added:
                    print(destination_filename + '/' + 'json' + json_folder + '/' + str(generated_filename) + '.json')
                    json_merge_3()

        elif json_folder.__contains__('temp'):
            print("temp")
            per_merge = 1
            print(len(json_temp_list))
            json_type = json_type_temp

            # Tries to make a new dir for the files
            try:
                os.makedirs(destination_filename + '/' + 'json' + json_folder)
            except OSError:
                pass

            x = 1
            while x == 1:
                json_to_be_merged = json_temp_list[:per_merge]
                # Removes the transferred Files
                del json_temp_list[:per_merge]
                if len(json_temp_list) == 0:
                    x = 0

                json_merge1 = open(directory + json_folder + '/' + json_to_be_merged[0], 'r')

                generated_filename = json_to_be_merged[0]
                print(generated_filename)
                if generated_filename.endswith('1.csv'):
                    generated_filename = generated_filename[:-5]

                json_selected_preset = json_temp_preset

                with open(destination_filename + '/' + 'json' + json_folder +
                          '/' + str(generated_filename) + '.json', 'w', newline='') \
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
        column2 = column2/100
        column3 = column3/100
        complete = [str(column2), str(column3)]
        sak = "".join(json_selected_preset)
        sak = sak.split(',')
        dictionary = dict(zip(sak, complete))

        all_data = {"ID": location_id, "timestamp": row_list[0], "DataList": {json_type: dictionary}}
        json.dump(all_data, json_added, indent=4, ensure_ascii=False)


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
            timestamp = part1list[0]
            del part1list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)
            sak = "".join(json_selected_preset)
            sak = sak.split(',')
            dictionary = dict(zip(sak, complete))

            all_data = {"ID": location_id, "timestamp": timestamp, "DataList": {json_type: dictionary}}
            json.dump(all_data, json_added, indent=4, ensure_ascii=False)
        else:
            print("Here some data did not add up")
            merge_3x += 1
            print("We have missed " + str(merge_3x) + " in total!")


# Function that merges and converts the Schneider data from CSV to JSON objects
def json_merge_4():
    print(len(json_schneider_list))
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
            timestamp = part1list[0]
            del part1list[0]

            # Combines the lists
            complete = [part1list + part2list + part3list + part4list]
            # Removes the brackets at the beginning and end
            complete = complete.pop(0)
            sak = "".join(json_selected_preset)
            sak = sak.split(',')
            dictionary = dict(zip(sak, complete))

            # Dumps the data in to JSON
            all_data = {"ID": location_id, "timestamp": timestamp, "DataList": {json_type: dictionary}}
            json.dump(all_data, json_added, indent=4, ensure_ascii=False)
        else:
            print("Here some data did not add up")
            merge_4x += 1
            print("We have missed " + str(merge_4x) + " in total!")


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


def generate():
    try:
        if do_audit == 1:
            generate_audit()
    except NameError:
        print("Do_audit Was not selected")

    try:
        if create_csv == 1:
            csv_merging()
    except NameError:
        print("Do CSV was not selected")

    generated_move()

    try:
        if create_json == 1:
            generate_json()
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


# Theme color presets which control all colors on GUI

Preset_color_white = '#ffffff'  # white theme color
Preset_color_gray = '#9d9d9c'  # gray theme color
Preset_color_orange = '#e16b02'  # Orange theme color

# GUI Code for the folders which will be used
folder_path = StringVar()
select_folder_title = Label(text=" Select the folder: ", background=Preset_color_gray)
select_folder_title.grid(row=1, column=1)
select_folder_title.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
select_folder_button = Button(text=" Select Folder ", command=browse_button)
select_folder_button.grid(row=1, column=4)
select_folder = Label(master=window, textvariable=folder_path)
select_folder.config(width=50)
select_folder.grid(row=1, column=2)

# GUI Code for the destination selection
destination_folder_path = StringVar()
select_destination_folder_title = Label(text=" Select the destination folder: ", background=Preset_color_gray)
select_destination_folder_title.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
select_destination_folder_title.grid(row=2, column=1)
select_destination_folder_button = Button(text=" Select Folder ", command=destination_browse_button)
select_destination_folder_button.grid(row=2, column=4)
select_destination_folder = Label(master=window, textvariable=destination_folder_path)
select_destination_folder.config(width=50)
select_destination_folder.grid(row=2, column=2)

# GUI Code for the ZIP creation of the generated files
zip_check = Label(text=" Do you want the results in a Zip?: ", background=Preset_color_gray)
zip_check.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
zip_check.grid(row=6, column=1)
zip_checking = Variable(value=0)
zip_checked = Checkbutton(window, text='', variable=zip_checking, command=zip_file)
zip_checked.grid(row=6, column=2)

# GUI Code for the JSON generation checkbox
json_check = Label(text=" Do you want it as JSON?: ", background=Preset_color_gray)
json_check.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
json_check.grid(row=4, column=1)
json_checkbox = Variable(value=0)
json_checked = Checkbutton(window, text='', variable=json_checkbox, command=json_file)
json_checked.grid(row=4, column=2)

# GUI Code for the CSV generation checkbox
csv_check = Label(text=" Do you want it as CSV?: ", background=Preset_color_gray)
csv_check.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
csv_check.grid(row=5, column=1)
csv_checkbox = Variable(value=0)
csv_checked = Checkbutton(window, text='', variable=csv_checkbox, command=csv_file)
csv_checked.grid(row=5, column=2)

# GUI Code for file checking
audit = Label(text=" Do you want to perform a pre process check?: ", background=Preset_color_gray)
audit.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
audit.grid(row=7, column=1)
audit_check = Variable(value=0)
audit_checked = Checkbutton(window, text='', variable=audit_check, command=perform_audit)
audit_checked.grid(row=7, column=2)

# GUI Code for the result check
result_audit = Label(text=" Do you want to perform a check on the resulting files?: ", background=Preset_color_gray)
result_audit.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_white)
result_audit.grid(row=8, column=1)
result_audit_check = Variable(value=0)
result_audit_checked = Checkbutton(window, text='', variable=result_audit_check, command=perform_result_audit)
result_audit_checked.grid(row=8, column=2)

# Creates a gap between the 2nd column and the buttons
spacing = Label(window, text="a", background=Preset_color_gray)
spacing.config(font=("Helvetica", 6, "roman italic"), fg=Preset_color_gray)
spacing.grid(row=999, column=3)

# GUI Code for the Generate button
generate_button = Button(window, text=" Generate ", command=generate)
generate_button.config(font=("Helvetica", 11, "roman italic"), fg=Preset_color_orange)
generate_button.place(relx=.5, rely=.9, anchor='c')

window.mainloop()
