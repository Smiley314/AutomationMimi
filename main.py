import pandas as pd
import os

predefined_values = [  "ACT3086G" ]  # Replace with your desired value
column_indices_to_compare = [0]  # Replace with the column indices you want to compare

def compare_and_save_matches(file_path, output_file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        matching_rows_list = []  # To store matched rows from all sheets
        
        for predefined_value in predefined_values:
            for sheet_name in sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Filter the DataFrame to only include the specified columns by index
                filtered_df = df.iloc[:, column_indices_to_compare]
                print(filtered_df)
                
                # Find rows where any value in the specified columns matches the current predefined value
                matching_rows = df[(filtered_df == predefined_value).any(axis=1)]
                
                if not matching_rows.empty:
                    pd.options.mode.chained_assignment = None  # Suppress the SettingWithCopyWarning
                    matching_rows['PredefinedValue'] = predefined_value  # Add a column for predefined value
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

directory_path = '/Users/smiley/Desktop/Mimi'
output_file_path = '/Users/smiley/Desktop/Mimi/matched_rows.xlsx'

for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)
        compare_and_save_matches(file_path, output_file_path)