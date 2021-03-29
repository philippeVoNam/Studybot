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
        for directory in directories: 
            dataDirectories.append(os.path.join(root, directory))

        for filename in filenames:  
            dataFiles.append(os.path.join(root,filename))

    return dataDirectories, dataFiles

def connect_tutorial_lecture_event(csvPath: str):
    # link the lecture event ID to it corresponding tutorial event id
    eventLinkData = []
    df = pd.read_csv(csvPath)
    for index, row in df.iterrows():
        courseID = row["CourseID"]
        type_ = row["Type"]
        number = row["Number"]
        eventID = row["EventID"]

        for index, row in df.iterrows():
            compare_courseID = row["CourseID"]
            compare_type_ = row["Type"]
            compare_number = row["Number"]
            compare_eventID = row["EventID"]

            if courseID == compare_courseID:
                if number == compare_number:
                    if type_ != compare_type_:

                        # [lecture event id, tutorial event id]

                        if type_ == "Lectures":
                            if [eventID, compare_eventID] not in eventLinkData:
                                eventLinkData.append([eventID, compare_eventID])

                        else: # type == tutorial
                            if [compare_eventID, eventID] not in eventLinkData:
                                eventLinkData.append([compare_eventID, eventID])

    return eventLinkData

def process_dirs(dirPaths: str, courseDataInfo: {}):
    # process the dirs and return the data about the courses in a format of a list of list

    coursesEventData = []
    coursesMaterialData = []
    eventNum = 0

    eventData = {}
    for dirPath in dirPaths:
        # process the dir and return list of list
        dataDir, dataFiles = scan_dir(dirPath)

        # get event
        lectureNumberExisting = []
        tutorialNumberExisting = []
        for file in dataFiles:
            data = file.split("/")

            if data[5] == "tutorial" or data[5] == "lab":
                courseType = data[1]
                courseNum = data[2]
                type_ = data[3]
                number = int(data[4])
                lectureMaterialType = data[5]
                typeMaterial = data[6]
                fileMaterial = data[7]

                courseID = courseDataInfo[courseType + "-" + courseNum]

                # add to event csv
                if number not in tutorialNumberExisting:
                    
                    # add to event dict, we use to see, given the path, which event it is
                    keyStr = "/".join(data[0:5])
                    eventData[keyStr] = eventNum

                    tutorialNumberExisting.append(number)
                    coursesEventData.append([eventNum, courseID, lectureMaterialType, number])
                    eventNum += 1

                # add to material csv
                keyStr = "/".join(data[0:5])
                eventNumData = eventData[keyStr]
                coursesMaterialData.append([eventNumData, typeMaterial, file])

            else:
                courseType = data[1]
                courseNum = data[2]
                type_ = data[3]
                number = int(data[4])
                typeMaterial = data[5]
                fileMaterial = data[6]

                courseID = courseDataInfo[courseType + "-" + courseNum]

                # add to event csv
                if number not in lectureNumberExisting:
                    
                    # add to event dict, we use to see, given the path, which event it is
                    keyStr = "/".join(data[0:5])
                    eventData[keyStr] = eventNum

                    lectureNumberExisting.append(number)
                    coursesEventData.append([eventNum, courseID, type_, number])
                    eventNum += 1

                # add to material csv
                keyStr = "/".join(data[0:5])
                eventNumData = eventData[keyStr]
                coursesMaterialData.append([eventNumData, typeMaterial, file])

    return coursesEventData, coursesMaterialData
