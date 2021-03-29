 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
# * Imports
# 3rd Party Imports
from src.test.scan_dir import scan_dir, process_dirs, connect_tutorial_lecture_event
import pandas as pd
from pandas import DataFrame
# User Imports

# * Code

# course id
courseDataInfo = {
    "SOEN-343": "SOEN343",
    "COMP-474": "COMP474"
}
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

paths = ["local_dataset/COMP", "local_dataset/SOEN"]
coursesEventData, coursesMaterialData = process_dirs(paths, courseDataInfo)

dfEvent = DataFrame(coursesEventData, columns=["EventID" ,"CourseID", "Type", "Number"])
dfMaterial  = DataFrame(coursesMaterialData, columns=["EventID" ,"Type", "Link"])

dfEvent.to_csv("df_event.csv", index = False)
dfMaterial.to_csv("df_material.csv", index = False)

# link events
eventLinkData = connect_tutorial_lecture_event("df_event.csv")

dfEventLink  = DataFrame(eventLinkData, columns=["EventID" ,"ExtraEventID"])

dfEventLink.to_csv("df_event_link.csv", index = False)
