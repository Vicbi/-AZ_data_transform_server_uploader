import os
import zipfile
import pandas as pd
from datetime import datetime
import numpy as np

# Function to get the date in the required format
def get_date():
    return datetime.now().strftime("%Y%m%d")

# Function to unzip all .zip files in the current directory        
def unzip_all(folder_path):
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a zip file
        if filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all contents to the folder_path
                zip_ref.extractall(folder_path)
                # print(f"Unzipped: {filename}")

def create_csv_with_all_data(eid,user_folder_path,data_type):

    # List all folders in user_folder 
    folders = [f for f in os.listdir(user_folder_path) if os.path.isdir(os.path.join(user_folder_path, f)) and f != '.ipynb_checkpoints']
    dfs = []
    check_size = []
    
    # Iterate over each folder
    for folder in folders:
        # print("Folder:", folder)
        folder_pathname = user_folder_path+'/'+folder
        # print('Folder pathname:', folder_pathname)
                
        # Create an empty dataframe for the current folder
        df_folder = pd.DataFrame()

        for file_name in os.listdir(folder_pathname):
            if file_name.lower().endswith('.csv') and data_type in file_name.lower():
                file_path = os.path.join(folder_pathname, file_name)
                data_df = pd.read_csv(file_path)
                
                # Add filename and eid columns
                data_df['filename'] = folder
                data_df['eid'] = eid

                # Append data to the dataframe for the current folder
                df_folder = pd.concat([df_folder, data_df], ignore_index=True)
                check_size.append(df_folder.shape[0])
                # print(check_size)
                # print(np.sum(check_size))
    
                # Append the dataframe for the current folder to the list
                dfs.append(df_folder)
                 
    
    # Concatenate dataframes from all folders
    result_df = pd.concat(dfs, ignore_index=True)
        
    # Write the combined dataframe to a single CSV file
    output_csv_filename = f"D9150M00002_{eid}_{data_type}_{get_date()}.csv"

    # Change directory for saving the output file
    parent_directory = 'results/'

    # Combine the parent directory and filename to create the full path
    full_path = os.path.join(parent_directory, output_csv_filename)

    # Save the DataFrame to the CSV file in the parent directory
    result_df.to_csv(full_path, index=False)
    print(f"Data written to {output_csv_filename}")