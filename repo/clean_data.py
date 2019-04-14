import os
import shutil
import pandas as pd
import airflow

INPUT_FOLDER = '/home/ubuntu/repo/InputFolder'
OUTPUT_FOLDER = '/home/ubuntu/repo/OutputFolder'
file = 'CombinedOpt.csv'

def run(**kwargs):
    args_dict = kwargs['ti']
    col_name = args_dict.xcom_pull(task_ids='push_col_name')
    combined_file = pd.read_csv(os.path.join(OUTPUT_FOLDER, file))
    combined_file.drop([col_name], inplace=True, axis=1)
    combined_file.to_csv('/home/ubuntu/repo/OutputFolder/CleanedOpt.csv', index=False)
