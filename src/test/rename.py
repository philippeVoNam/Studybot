 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
# * Imports
# 3rd Party Imports
from pathlib import Path
import os
import pandas as pd
# User Imports

# * Code
def scan_dir(dirPath: str):
    # scan directory and extract the dirs and files
    dirPath = Path(dirPath)

    directory = os.listdir(dirPath)

    dataDirectories = []
    dataFiles = []
    for root, directories, filenames in os.walk(dirPath): 

        for filename in filenames:  
            dataFiles.append(os.path.join(root,filename))

            ogFile = os.path.join(root,filename)
            ogFile = os.path.abspath(ogFile)

            src = ogFile
            
            destFileName = filename.replace(" ", "_")

            destFile = os.path.join(root,destFileName)
            destFile = os.path.abspath(destFile)

            dest = destFile

            print("---")
            print(src)
            print(dest)
            print("---")
            

    return dataDirectories, dataFiles

if __name__ == "__main__":
    scan_dir("local_dataset/")
