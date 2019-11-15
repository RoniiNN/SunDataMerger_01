import os.path
from tkinter import filedialog
from tkinter import *
import shutil
import json

# The Tkinter init
window = Tk()
window.title('CSV Merged to JSON')
window.geometry('815x400')
window.configure(background='#9d9d9c')
window.resizable(width=False, height=False)


# Sets the enter dt entry as variable
def define_data_type():
    global data_list_type
    dt_received = enter_dt_entry.get()
    print(dt_received)
    if len(dt_received) != 0:
        data_list_type = dt_received
    else:
        data_list_type = "Undefined"


# Sets the id written in the field
def set_id():
    global location_id
    run_sec = 1
    try:
        received = enter_id_entry.get()
        if len(received) != 0:
            location_id = received
        else:
            run_sec = 0
    except (ValueError, TypeError):
        location_id = "Undefined"

    if run_sec == 0:
        try:
            location = file
            # location = location.replace('-', ';', 1)
            # print(location)
            location = location.split(';')
            location_id = location[0]
            print(location_id)
        except (OSError, ValueError, TypeError):
            location_id = "Undefined"


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    global filename
    global directory
    global file_list
    global files
    global json_filename
    files = []
    directory = filedialog.askdirectory()
    display_directory = directory
    while len(display_directory) > 50:
        display_directory = display_directory[1:]
    if len(display_directory) >= 50:
        display_directory = '...' + display_directory
    folder_path.set(display_directory)
    directory = directory + '/'
    print(directory)

    print(os.listdir(directory))
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            files.append(filename)
            json_filename = filename[:-3]
        else:
            print(filename + " This doesn't belong here")

    print(files)
    file_list = files
    print(directory)


def zip_file():
    global create_zip
    create_zip = 0
    is_checked = zip_checking.get()

    if is_checked != str(0):
        create_zip = 1

    return create_zip


def generate_zip():
    print(destination_filename)

    json_destination = destination_filename[:-9]
    print(json_destination)
    try:
        shutil.make_archive(json_destination + '/JSONGenerated', 'zip', json_destination + '/JSONGenerated')
    except OSError:
        print("JSONGenerated did not exist")


def destination_browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global destination_filename
    global destination_folder_name
    global destination_folders

    destination_folders = []
    destination_folder_name = '/JSONGenerated'
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


def generating_json():
    global file
    compare_name = ''
    for file in file_list:
        x = 0
        set_id()
        with open(directory + file, 'r') as csv_reader:
            define_data_type()
            for row in csv_reader:
                if x == 0:
                    the_header = row
                    the_header = the_header.replace('\n', '')
                    the_header = the_header.split(',')
                    x += 1
                    del the_header[0]
                else:
                    row = row.replace('\n', '')
                    row = row.replace(' ', '')
                    row_list = row.split(',')
                    timestamp = row_list[0]
                    del row_list[0]
                    cell_list = []
                    for cell in row_list:
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
                        cell_list.append(cell)

                    file_timestamp = timestamp[:-10]
                    file_name = location_id + '-' + file_timestamp + ".json"
                    folder_month_timestamp = file_timestamp[:-6]
                    folder_month = folder_month_timestamp
                    folder_day_timestamp = file_timestamp[:-3]
                    folder_day = folder_day_timestamp

                    combine = dict(zip(the_header, cell_list))
                    all_data = {"ID": location_id, "timestamp": timestamp, "DataList": {data_list_type: combine}}

                    if file_name != compare_name:
                        try:
                            os.makedirs(destination_filename + '/')
                        except OSError:
                            pass

                        try:
                            os.mkdir(destination_filename + '/' + folder_month + '/')
                        except OSError:
                            pass
                        try:
                            os.mkdir(destination_filename + '/' + folder_month + '/' + folder_day + '/')
                        except OSError:
                            pass
                        complete_json = open(destination_filename + '/' + folder_month + '/' +
                                             folder_day + '/' + file_name, 'a')
                        json.dump(all_data, complete_json, indent=4, ensure_ascii=False)
                        complete_json.write('\n')
                        compare_name = file_name

                        # Opens and writes the Json
                    else:
                        json.dump(all_data, complete_json, indent=4, ensure_ascii=False)
                        complete_json.write('\n')


def generate():
    generating_json()
    try:
        if create_zip == 1:
            generate_zip()
    except NameError:
        print("Generate_Zip Was not selected")


folder_path = StringVar()
select_folder_title = Label(text=" Select the folder: ", background='#9d9d9c')
select_folder_title.grid(row=1, column=1)
select_folder_title.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
select_folder_button = Button(text=" Select Folder ", command=browse_button)
select_folder_button.grid(row=1, column=3)
select_folder = Label(master=window, textvariable=folder_path)
select_folder.config(width=50)
select_folder.grid(row=1, column=2)

destination_folder_path = StringVar()
select_destination_folder_title = Label(text=" Select the destination folder: ", background='#9d9d9c')
select_destination_folder_title.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
select_destination_folder_title.grid(row=9, column=1)
select_destination_folder_button = Button(text=" Select Folder ", command=destination_browse_button)
select_destination_folder_button.grid(row=9, column=3)
select_destination_folder = Label(master=window, textvariable=destination_folder_path)
select_destination_folder.config(width=50)
select_destination_folder.grid(row=9, column=2)

enter_id_label = Label(window, text="Enter Site ID:", background='#9d9d9c')
enter_id_label.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
enter_id_label.grid(row=10, column=1)
enter_id_entry = Entry()
enter_id_entry.grid(row=10, column=2)
enter_id_confirm = Button(text="Confirm", command=set_id)
enter_id_confirm.grid(row=10, column=3)

enter_dt_label = Label(window, text="Enter The Data Type Name:", background='#9d9d9c')
enter_dt_label.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
enter_dt_label.grid(row=11, column=1)
enter_dt_entry = Entry()
enter_dt_entry.grid(row=11, column=2)
enter_dt_confirm = Button(text="Confirm", command=define_data_type)
enter_dt_confirm.grid(row=11, column=3)

zip_check = Label(text=" Do you want the results in a Zip?: ", background='#9d9d9c')
zip_check.config(font=("Helvetica", 11, "roman italic"), fg='#ffffff')
zip_check.grid(row=12, column=1)
zip_checking = Variable(value=0)
zip_checked = Checkbutton(window, text='', variable=zip_checking, command=zip_file)
zip_checked.grid(row=12, column=2)

generate_button = Button(window, text=" Generate ", command=generate)
generate_button.config(font=("Helvetica", 11, "roman italic"), fg='#e16b02')
generate_button.place(relx=.5, rely=.9, anchor='c')

window.mainloop()
