import os.path
import json
from tkinter import filedialog
from tkinter import *
import shutil
import itertools
the_files = []
timestamp = "timeStamp"
location_id = "undefined"
data_1 = "Data Type 1"
data_2 = "ClusterControl"

# The Tkinter init
window = Tk()
window.title('STUNS Energi')
window.geometry('695x400')
window.configure(background='#9d9d9c')
window.resizable(width=False, height=False)


# Takes the rows to header
def amount_of_rows():
    global rows_to_header
    rows_to_header = enter_rows_to_header_entry.get()
    rows_to_header = int(rows_to_header)
    rows_to_header -= 1
    if rows_to_header == 'null':
        rows_to_header = 0

    # header at row 8
    # header at row 9 if the additional pre change row


def set_id():
    # Sets the id written in the field
    global location_id
    location_id = enter_id_entry.get()
    # If nothing was entered and the user pressed confirmed the ID will change from '' to 'undefined'
    if len(location_id) == 0:
        location_id = 'undefined'


def destination_browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global destination_filename
    global destination_folder_name
    global destination_folders

    destination_folders = []
    destination_folder_name = '/JSON'
    destination_filename = filedialog.askdirectory()
    display_directory = destination_filename
    while len(display_directory) > 50:
        display_directory = display_directory[1:]
    if len(display_directory) >= 50:
        display_directory = '...' + display_directory
    destination_folder_path.set(display_directory)
    print(destination_filename)
    destination_filename = destination_filename + destination_folder_name
    # Makes the directory for the destination files
    try:
        os.makedirs(destination_filename)
    except OSError:
        pass
    print(destination_filename)


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    global filename
    global directory
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
        if filename.endswith('.csv'):
            print(filename)
            folders.append(filename)
        else:
            print(filename + " Does not end with .CSV so i wont use it")


# This is the main function for the JSON generation
def generate_json():
    the_folder = os.listdir(directory)
    for file in the_folder:
        if file.endswith(".csv"):
            the_files.append(file)

    for file in the_files:
        json_file = file
        json_file = json_file[:6]
        json_file = json_file + '.json'
        with open(directory + '/' + file) as current_file:
            x = 0
            with open(destination_filename + '/' + json_file, 'w') as json_write:
                the_header = ''
                for row in current_file:
                    if x < rows_to_header:
                        x += 1
                    elif x == rows_to_header:
                        the_header = row
                        the_header = the_header.replace('\n', '')
                        the_header = the_header.split(';')

                        # Splits the list in to smaller lists to make it easier to remove unnecessary values
                        del the_header[0]
                        unit_1_header = the_header[32:]
                        unit_2_header = unit_1_header[26:]
                        del unit_1_header[26:]
                        unit_3_header = unit_2_header[26:]
                        del unit_2_header[26:]

                        # Removes unnecessary values
                        del the_header[32:]
                        del the_header[0]
                        del the_header[4]

                        del the_header[25]
                        del the_header[25]
                        del the_header[25]

                        del the_header[21]
                        del the_header[21]
                        del the_header[21]
                        del the_header[21]
                        del the_header[-1]

                        del unit_1_header[-4:]
                        del unit_2_header[-4:]
                        del unit_3_header[-4:]

                        del unit_1_header[8]
                        del unit_2_header[8]
                        del unit_3_header[8]

                        del unit_1_header[1]
                        del unit_2_header[1]
                        del unit_3_header[1]

                        del unit_1_header[3]
                        del unit_2_header[3]
                        del unit_3_header[3]

                        # Chains the Unit header parts together
                        cluster_control = itertools.chain(unit_1_header, unit_2_header, unit_3_header)
                        cluster_control = tuple(cluster_control)
                        print(cluster_control)

                        x += 1
                    else:
                        row_str = row
                        row_str = row_str.replace('\n', '')
                        row_list = row_str.split(';')

                        # Splits the list in to smaller lists to make it easier to remove unnecessary values
                        del row_list[0]
                        unit_1 = row_list[32:]
                        del row_list[32:]
                        unit_2 = unit_1[26:]
                        del unit_1[26:]
                        unit_3 = unit_2[26:]
                        del unit_2[26:]
                        ts = row_list[0]

                        # Removes unnecessary values
                        del row_list[0]
                        del row_list[4]

                        del row_list[25]
                        del row_list[25]
                        del row_list[25]

                        del row_list[21]
                        del row_list[21]
                        del row_list[21]
                        del row_list[21]
                        del row_list[-1]

                        del unit_1[-4:]
                        del unit_2[-4:]
                        del unit_3[-4:]

                        del unit_1[8]
                        del unit_2[8]
                        del unit_3[8]

                        del unit_1[1]
                        del unit_2[1]
                        del unit_3[1]

                        del unit_1[3]
                        del unit_2[3]
                        del unit_3[3]

                        cell_list = []
                        # Goes through each row and replace every empty value with null and converts
                        # all possible values to ints and floats
                        for cell in row_list:
                            if len(cell) == 0:
                                cell = cell.replace(cell, 'null')
                                cell_list.append(cell)
                            else:
                                if cell.__contains__(','):
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

                                cell_list.append(cell)

                        unit_1_list = []
                        for cell in unit_1:
                            if len(cell) == 0:
                                cell = cell.replace(cell, 'null')
                                unit_1_list.append(cell)
                            else:
                                if cell.__contains__(','):
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

                                unit_1_list.append(cell)

                        unit_2_list = []
                        for cell in unit_2:
                            if len(cell) == 0:
                                cell = cell.replace(cell, 'null')
                                unit_2_list.append(cell)
                            else:
                                if cell.__contains__(','):
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

                                unit_2_list.append(cell)

                        unit_3_list = []
                        for cell in unit_3:
                            if len(cell) == 0:
                                cell = cell.replace(cell, 'null')
                                unit_3_list.append(cell)
                            else:
                                if cell.__contains__(','):
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

                                unit_3_list.append(cell)
                        # Chains the Unit list parts together
                        cluster_list = itertools.chain(unit_1_list, unit_2_list, unit_3_list)
                        cluster_list = tuple(cluster_list)

                        data_type_1 = dict(zip(the_header, cell_list))
                        data_type_2 = dict(zip(cluster_control, cluster_list))

                        all_data = {"ID": location_id, timestamp: ts,
                                    "DataList": {data_1: data_type_1, data_2: data_type_2}}
                        json.dump(all_data, json_write, indent=4, ensure_ascii=False)
                        json_write.write('\n')


def zip_file():
    # Checks if the Zip checkbox is checked
    global create_zip
    create_zip = 0
    is_checked = zip_checking.get()

    if is_checked != str(0):
        create_zip = 1


def generate_zip():
    # Creates a Zip from the destination
    try:
        shutil.make_archive(destination_filename, 'zip', destination_filename)
    except OSError:
        print("The folder did not exist")


def generate():
    amount_of_rows()
    generate_json()

    try:
        if create_zip == 1:
            generate_zip()
    except NameError:
        print("Generate_Zip Was not selected")


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

# GUI Code for the ZIP creation of the generated files
zip_check = Label(text=" Do you want an additional ZIP? ", background='#9d9d9c')
zip_check.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
zip_check.grid(row=3, column=1)
zip_checking = Variable(value=0)
zip_checked = Checkbutton(window, text='', variable=zip_checking, command=zip_file)
zip_checked.grid(row=3, column=2)

# GUI Code for the site id
enter_id_label = Label(window, text="Enter Site ID:", background='#9d9d9c')
enter_id_label.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
enter_id_label.grid(row=4, column=1)
enter_id_entry = Entry()
enter_id_entry.grid(row=4, column=2)
enter_id_confirm = Button(text="Confirm", command=set_id)
enter_id_confirm.grid(row=4, column=4)

# GUI Code for the amount of rows to header
enter_rows_to_header_label = Label(window, text="Enter the amount of rows to header:", background='#9d9d9c')
enter_rows_to_header_label.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
enter_rows_to_header_label.grid(row=5, column=1)
enter_rows_to_header_entry = Entry()
enter_rows_to_header_entry.grid(row=5, column=2)
enter_rows_to_header_confirm = Button(text="Confirm", command=amount_of_rows)
enter_rows_to_header_confirm.grid(row=5, column=4)

# Creates a gap between the 2nd column and the buttons
spacing = Label(window, text="a", background='#9d9d9c')
spacing.config(font=("Helvetica", 6, "roman italic"), fg='#9d9d9c')
spacing.grid(row=999, column=3)

# GUI Code for the generate function
generate_button = Button(window, text=" Generate ", command=generate)
generate_button.config(font=("Helvetica", 11, "roman italic"), fg='#e16b02')
generate_button.place(relx=.5, rely=.9, anchor='c')

window.mainloop()
