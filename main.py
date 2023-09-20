import pandas as pd
import os

preDef = []
predefined_values = ["ASM7121G"]  # Replace with your desired value "675-639-00" 0,1 for search 2 for return
column_indices_to_compare = [0,1]  # Replace with the column indices you want to compare
columns_to_keep = [0,2]
matching_rows_list = []  # To store matched rows from all sheets


#Not yet working
def data_proccesing(file_path):
    df = pd.read_excel(file_path)
    
    for col in df.columns:
      # Find index of first non-NaN value in column
      first_notna = df[col].first_valid_index()
      print(first_notna)
      # Slice column from that index and overwrite
      df[col] = df[col].iloc[first_notna:]
      
      df.to_excel(output_file_path1, index=False)
      
def getting_values(search_path):
    df = pd.read_excel(search_path)

    preDef = df.iloc[:,0]
    return preDef
      

def compare_and_save_matches(file_path, output_file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        
        for predefined_value in preDef:
            for sheet_name in sheet_names:
                #df = pd.read_excel(file_path, sheet_name=sheet_name)
                df = pd.read_excel(file_path, sheet_name, usecols=columns_to_keep)
                print(sheet_name)
                # Filter the DataFrame to only include the specified columns by index
                filtered_df = df.iloc[:, column_indices_to_compare]
               
                
                # Find rows where any value in the specified columns matches the current predefined value
                matching_rows = df[(filtered_df == predefined_value).any(axis=1)]
                
                if not matching_rows.empty:
                    pd.options.mode.chained_assignment = None  # Suppress the SettingWithCopyWarning
                    #matching_rows['PredefinedValue'] = predefined_value  # Add a column for predefined value
                    
                    matching_rows_list.append(matching_rows)
                    
        
        # Concatenate all matching rows into a single DataFrame
        if matching_rows_list:
            result_df = pd.concat(matching_rows_list, ignore_index=True)  # Use ignore_index to reset row indices
        
            # Save the matching rows to an Excel file
            result_df.to_excel(output_file_path, index=False)
            print(f"Matched rows saved to '{output_file_path}'")
        else:
            print(f"No matches found in '{file_path}'")
    except Exception as e:
        print(f"Error processing '{file_path}': {str(e)}")

directory_path = 'C:/Users/muhammad.matloob/Desktop/Mimi/Files' 
search_path = "C:/Users/muhammad.matloob/Desktop/Mimi/Files/Search/Search.xlsx"
output_file_path = 'C:/Users/muhammad.matloob/Desktop/Mimi/Files/Results/matched_rows.xlsx'
# output_file_path1 = 'C:/Users/muhammad.matloob/Desktop/Mimi/Files/Results/matched_rows1.xlsx'


preDef = getting_values(search_path)

for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)
        compare_and_save_matches(file_path, output_file_path)
