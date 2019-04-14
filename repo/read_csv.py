import os
import shutil

INPUT_FOLDER = '/home/ubuntu/repo/InputFolder'
OUTPUT_FOLDER = '/home/ubuntu/repo/OutputFolder'
DOWNLOAD_FOLDER = '/home/ubuntu/repo/DownloadFolder'

def run():
    for file in os.listdir(INPUT_FOLDER):
        shutil.copy((os.path.join(INPUT_FOLDER, file)), OUTPUT_FOLDER)

    for file in os.listdir(INPUT_FOLDER):
        shutil.copy((os.path.join(DOWNLOAD_FOLDER, file)), OUTPUT_FOLDER)
