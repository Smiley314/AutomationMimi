import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw() 


directory_path = 'C:/Users/muhammad.matloob/Desktop/New/Results'
directory_path2 = 'C:/Users/muhammad.matloob/Desktop/New/Files'
dataSelect = "OC"
userInput_replacevalues = ""
response = None
file_names = []
file_paths = []
# Create an empty list to store the appended data frames
appended_data = []
col_names = ["VBCITStart","VBCITEnd", "VBCITDelta", "1096_4", "FilterPrime", "DirectPathClear" ,
             "FastTog", "1097_4", "Lubrication", "1098_2", "1098_3", "1098_4", "Polybead/BackPressure",
             "1099_2", "1099_3", "1099_4"]


def userInput(prompt):
    Input = simpledialog.askstring("var", prompt)
    return Input


def getDirectory():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory() 
    return folder_path

def openCSV_file(filename):
    data = pd.read_csv(filename, skiprows=7)
    return data

def split_data(data):
    data = data.iloc[:,28].str.split("[,|:]",expand=True)
    return data

def cleaned_data(data):
    extracted_data = data.iloc[:,[2,3,4,5,8,9,10,11,14,15,16,17,20,21,22,23]].copy()
    for col in extracted_data.columns:
        extracted_data[col] = pd.to_numeric(extracted_data[col], errors='coerce')
    return extracted_data / 10

def join_datas(data,datatoJoin):
    datatoJoin.columns = col_names
    data = data.dropna(how='all')
    data = data.join(datatoJoin)
    return data

def replace_column_values(data, replacement_value):
    # If Open Cart IPT data OC/2 otherwise VBA IPT data 
    if dataSelect == "1" or dataSelect == "OC":
        extracted_data = data.iloc[:,[2,11,56,57,58,59,60,61,62,63,72,74,75]].copy()
    else:
        extracted_data = data.iloc[:,[2,26,27,34,35,36,38,39,40,42,46]].copy()
        
    # Replace a column with a specific value
    # extracted_data[column_to_replace] = replacement_value
    if replacement_value != None:
        extracted_data.iloc[:,[0]] = replacement_value

    return extracted_data


def main(directory_path):
    global file_names, file_paths, response, userInput_replacevalues, dataSelect, appended_data

    for filename in os.listdir(directory_path):
        file_names.append(filename)
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            file_paths.append(file_path)

           


    while response == None: 
        dataSelect = userInput("OC or VBA:(1 or 2): ") 
        if dataSelect == "OC" or dataSelect == "VBA" or dataSelect == "1" or dataSelect =="2":
            response = "Good"

    userInput_replacevalues = userInput("Do you need to replcae sample ID values? (y/n):")


    for filename in file_names:
    # Prompt the user for the replacement value
        if userInput_replacevalues == "y" or userInput_replacevalues == "Y":
            replacement_value = userInput(f"Enter the replacement value for {filename}: ")
        else:
            replacement_value = None

        for file_path in file_paths:
            # Read the CSV file into a DataFrame
            data = pd.read_csv(file_path)

            # Call the function to replace column values
            modified_data = replace_column_values(data, replacement_value)

            # Append the modified data to the appended_data list
            appended_data.append(modified_data)
            # Concatenate the data frames in the list
    merged_data = pd.concat(appended_data)

    # Reset the index of the merged data
    merged_data.reset_index(drop=True, inplace=True)

    # Prompt the user for the output filename
    output_filename = userInput("Enter the output filename: ")

    # Write the merged data to a CSV file
    merged_data.to_csv(output_filename, index=False)

    print(f"The merged data has been written to {output_filename}.")


def raw_data(directory_path2, directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for filename in os.listdir(directory_path2):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path2, filename)
            data = openCSV_file(file_path)

            working_Data = split_data(data)

            working_Data = cleaned_data(working_Data)

            final_data = join_datas(data,working_Data)
            # file_savename = f'data_{filename}'
            file_path2 = os.path.join(directory_path, filename)
            final_data.to_csv(file_path2)


path = getDirectory()
directory_path = directory_path + "/Results"
raw_data(path,directory_path)
main(directory_path)


