import pandas as pd

import os

from constants import DATA_DIR


course_catalog = pd.read_csv(os.path.join(
    DATA_DIR, 'CU_SR_OPEN_DATA_CATALOG.csv'),
    encoding='latin1')

course_descriptions = pd.read_csv(os.path.join(
        DATA_DIR, 'CU_SR_OPEN_DATA_CATALOG_DESC.csv'),
        encoding='latin1')

courses = pd.merge(course_catalog, course_descriptions, on='Course ID')

subjects = courses['Subject'].unique()

