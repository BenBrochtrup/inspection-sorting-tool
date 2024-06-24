import pandas as pd
import os
from report import *

# Function to read a CSV file and print its headers
def read_csv_with_headers(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        print(f"The file at path {file_path} does not exist.")
    except pd.errors.EmptyDataError:
        print("No data in the file.")
    except pd.errors.ParserError:
        print("Error parsing the data.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_employee_id_columns(df):
    # Create a new column with the first four digits of the 'Equipment Item Identifier'
    df['ID'] = df['Equipment Item Identifier'].str[:4]
    df['Assignee Name'] = df['Assignee First Name'] + ' ' + df['Assignee Last Name']
    return df

def group_by_column(df, group_by_column):
    # Check if the specified column exists
    if group_by_column not in df.columns:
        raise ValueError(f"The column '{group_by_column}' does not exist in the CSV file.")
    
    return df.groupby(group_by_column)

def save_dataframes(dfs, title_column):
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    for value, group in dfs:
        output_file = os.path.join("output", f"{group[title_column].iloc[0]}.csv")
        group.to_csv(output_file, index=False)
        print(f"DataFrame for '{group[title_column].iloc[0]}' saved to {output_file}")

# Define codes for equipment type
code_map = {
    'HE': 'Helmet',
    'BT': 'Boots',
    'HD1': 'Hood (1)',
    'HD2': 'Hood (2)',
    'GL1': 'Gloves (1)',
    'GL2': 'Gloves (2)',
    'CT1': 'Coat (1)',
    'CT2': 'Coat (2)',
    'PT1': 'Pants (1)',
    'PT2': 'Pants (2)'
}

def assign_equipment_type(df):
    def determine_type(equipment_id):
        code = equipment_id[4:]
        return code_map.get(code, 'Unknown')
    
    df['Type'] = df['Equipment Item Identifier'].apply(determine_type)
    return df

def format_blank_strings(df):
    def replace_nan(text):
        return '' if pd.isna(text) else text
    return df.map(replace_nan)

def format_years(df):
    def convert(value):
        if pd.isna(value):
            return ''
        else:
            return int(value)
    df['Year of Equipment Item'] = df['Year of Equipment Item'].apply(convert)
    return df

def generate_reports(csv_path, output_folder):
    csv = read_csv_with_headers(csv_path)
    df = create_employee_id_columns(csv)
    df = assign_equipment_type(df)
    df = format_years(df)
    df = format_blank_strings(df)
    dfs = group_by_column(df, "ID")
    for value, group in dfs:
        assignee_first = group['Assignee First Name'].iloc[0]
        assignee_last = group['Assignee Last Name'].iloc[0]
        employee_id = group['ID'].iloc[0]
        assignee = group['Assignee Name'].iloc[0]
        report_path = os.path.join(output_folder, f"{assignee}.pdf")
        dataframe_to_pdf(group, report_path, assignee_first, assignee_last, employee_id)
