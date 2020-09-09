from tkinter import *
from tkinter import filedialog, messagebox
import csv
import pandas as pd
import os

app = Tk()

app.title('CSV Merger')
app.geometry('650x400')
# app.iconbitmap('csvicon.ico')

file1 = None
file2 = None
file3 = None
file4 = None
output_file_location = None


def add_file1():
    global file1
    global file3
    merge_completed.config(text='')
    file1 = filedialog.askopenfilename(filetypes=(('CSV files', '*.csv'),))
    file1_name.config(text=file1)


def add_file2():
    global file2
    global file4
    file2 = filedialog.askopenfilename(filetypes=(('CSV files', '*.csv'),))
    file2_name.config(text=file2)


def perform_merge():
    if file1 is None or file2 is None or column_name.get() == '' or merger_values.get() == '' or output_file_location is None:
        messagebox.showerror('Required Fields', 'Please include all fields')
        return

    value_list = merger_values.get().split(',')

    with open(f'{file1}', 'r') as csv1:
        csv1_reader = csv.reader(csv1)
        header1 = next(csv1_reader)
        i1 = header1.index(column_name.get())

        with open('file3.csv', 'w') as csv3:
            csv3_writer = csv.writer(csv3, lineterminator='\r')
            csv3_writer.writerow(header1)
            for line in csv1_reader:
                if line[i1] in value_list:
                    csv3_writer.writerow(line)

    with open(f'{file2}', 'r') as csv2:
        csv2_reader = csv.reader(csv2)
        header2 = next(csv2_reader)
        i2 = header2.index(column_name.get())

        with open('file4.csv', 'w') as csv4:
            csv4_writer = csv.writer(csv4, lineterminator='\r')
            csv4_writer.writerow(header2)
            for line in csv2_reader:
                if line[i2] in value_list:
                    csv4_writer.writerow(line)

    a = pd.read_csv("file3.csv")
    b = pd.read_csv("file4.csv")
    b = b.dropna(axis=1)
    merged = a.merge(b, on=column_name.get())
    merged.to_csv(f"{output_file_location}/output.csv", index=False)
    os.remove('file3.csv')
    os.remove('file4.csv')
    merge_completed.config(text='Merge completed! output.csv created at selected folder location')
    clear_inputs()


def select_output_folder():
    global output_file_location
    output_file_location = filedialog.askdirectory()
    folder_location.config(text=output_file_location)


def clear_inputs():
    global file1, file2, output_file_location
    file1 = None
    file2 = None
    output_file_location = None
    merge_on_column_entry.delete(0, END)
    merger_values_entry.delete(0, END)
    file1_name.config(text='')
    file2_name.config(text='')
    folder_location.config(text='')


csv_file1 = Label(app, text='CSV File 1', font=('Times', 10, 'bold'), pady=20, padx=20)
csv_file1.grid(row=0, column=0, sticky=W)
add_file1_button = Button(app, text='Add CSV File 1', command=add_file1)
add_file1_button.grid(row=0, column=1, sticky=W)
file1_name = Label(app, text='', padx=20)
file1_name.grid(row=0, column=2, sticky=W)

csv_file2 = Label(app, text='CSV File 2', font=('Times', 10, 'bold'), pady=20, padx=20)
csv_file2.grid(row=1, column=0, sticky=W)
add_file2_button = Button(app, text='Add CSV File 2', command=add_file2)
add_file2_button.grid(row=1, column=1, sticky=W)
file2_name = Label(app, text='', padx=20)
file2_name.grid(row=1, column=2, sticky=W)

merge_on_column = Label(app, text='Column Name', font=('Times', 10, 'bold'), pady=20, padx=20)
merge_on_column.grid(row=2, column=0, sticky=W)
column_name = StringVar()
merge_on_column_entry = Entry(app, textvariable=column_name)
merge_on_column_entry.grid(row=2, column=1, sticky=W)

values = Label(app, text='Enter Values(comma separated)', font=('Times', 10, 'bold'), pady=20, padx=20)
values.grid(row=3, column=0, sticky=W)
merger_values = StringVar()
merger_values_entry = Entry(app, textvariable=merger_values)
merger_values_entry.grid(row=3, column=1, sticky=W)

output_file = Label(app, text='Output File location', font=('Times', 10, 'bold'), pady=20, padx=20)
output_file.grid(row=4, column=0, sticky=W)
select_folder_location_button = Button(app, text='Select Folder', command=select_output_folder)
select_folder_location_button.grid(row=4, column=1, sticky=W)
folder_location = Label(app, text='', padx=20)
folder_location.grid(row=4, column=2, sticky=W)

Buttons_frame = Frame(app)
Buttons_frame.grid(row=5, column=0, padx=20, pady=20, sticky=W)
perform_merge_button = Button(Buttons_frame, text='Merge', command=perform_merge)
perform_merge_button.grid(row=0, column=0, sticky=W)
clear_button = Button(Buttons_frame, text='Clear inputs', command=clear_inputs)
clear_button.grid(row=0, column=1, sticky=W, padx=20)

merge_completed = Label(app, text='')
merge_completed.grid(row=6, column=0, columnspan=3, sticky=W, padx=20)

app.mainloop()
