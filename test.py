 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
# * Imports
# 3rd Party Imports
from src.test.scan_dir import scan_dir, process_dirs
from pandas import DataFrame
# User Imports

# * Code

# course id
courseDataInfo = {
    "SOEN-343": 123,
    "COMP-474": 456
}

paths = ["data/COMP", "data/SOEN"]
coursesEventData, coursesMaterialData = process_dirs(paths, courseDataInfo)

dfEvent = DataFrame(coursesEventData, columns=["EventID" ,"CourseID", "Type", "Number"])
dfMaterial  = DataFrame(coursesMaterialData, columns=["EventID" ,"Type", "Link"])

print(dfEvent)
print(dfMaterial)
