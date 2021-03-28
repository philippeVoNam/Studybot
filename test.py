 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
# * Imports
# 3rd Party Imports
from src.test.scan_dir import scan_dir, process_dirs
import pandas as pd
from pandas import DataFrame
# User Imports

# * Code

# course id
courseDataInfo = {
    "SOEN-343": 123,
    "COMP-474": 456
}
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

paths = ["data/COMP", "data/SOEN"]
coursesEventData, coursesMaterialData = process_dirs(paths, courseDataInfo)

dfEvent = DataFrame(coursesEventData, columns=["EventID" ,"CourseID", "Type", "Number"])
dfMaterial  = DataFrame(coursesMaterialData, columns=["EventID" ,"Type", "Link"])

dfEvent.to_csv("df_event.csv")
dfMaterial.to_csv("df_material.csv")
