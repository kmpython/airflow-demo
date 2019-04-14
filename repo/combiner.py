import os
import shutil
import pandas as pd

INPUT_FOLDER = '/home/ubuntu/repo/InputFolder'
OUTPUT_FOLDER = '/home/ubuntu/repo/OutputFolder'

def run():
    base_file = pd.DataFrame(columns=['Fname', 'Lname', 'Dept'])
    print("Combining files from output directory")

    for file in os.listdir(OUTPUT_FOLDER):
        base_file = basefile.append(pd.read_csv(os.path.join(OUTPUT_FOLDER, file)))

    base_file.to_csv('/home/ubuntu/repo/OutputFolder.CombinedOpt.csv', index=False)