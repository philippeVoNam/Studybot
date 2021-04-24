import pandas as pd

import os

def load_courses(data_dir):
    course_catalog = pd.read_csv(os.path.join(
        data_dir, 'CU_SR_OPEN_DATA_CATALOG.csv'),
        encoding='latin1')

    course_descriptions = pd.read_csv(os.path.join(
        data_dir, 'CU_SR_OPEN_DATA_CATALOG_DESC.csv'),
        encoding='latin1')

    course_extras = pd.read_csv(os.path.join(
        data_dir, 'course_extra_info.csv'),
        encoding='latin1')

    course_topics = pd.read_csv(os.path.join(
        data_dir, 'course_topics.csv'),
        encoding='latin1')

    courses = pd.merge(course_catalog, course_descriptions, on='Course ID')
    courses = pd.merge(courses, course_extras, on="Course ID", how="left")

    return courses, course_topics


def load_universities(data_dir):
    universities = pd.read_csv(os.path.join(
        data_dir, 'universities.csv'),
        encoding='latin1')

    return universities


def load_subjects(data_dir, courses=None):
    if courses is None:
        courses, _ = load_courses(data_dir)

    subjects = courses['Subject'].unique()
    
    return subjects


def load_events(data_dir):
    lecture_data_dir = os.path.join(data_dir, 'lecture_data')

    eventCSV = pd.read_csv(os.path.join(
        lecture_data_dir, 'df_event.csv'),
        encoding='latin1')

    eventLinkCSV = pd.read_csv(os.path.join(
        lecture_data_dir, 'df_event_link.csv'),
        encoding='latin1')

    materialCSV = pd.read_csv(os.path.join(
        lecture_data_dir, 'df_material.csv'),
        encoding='latin1')

    lectureDataCSV = pd.merge(eventCSV, eventLinkCSV, on='EventID', how="left")
    lectureDataCSV = pd.merge(lectureDataCSV, materialCSV, on='EventID')

    return lectureDataCSV

def load_material_topics(data_dir):
    lecture_data_dir = os.path.join(data_dir, 'lecture_data')

    materialTopicsCSV = pd.read_csv(os.path.join(
        lecture_data_dir, 'course_material_topics.csv'),
        encoding='latin1')

    return materialTopicsCSV 

def load_data(data_dir):
    courses, course_topics = load_courses(data_dir)

    subjects = load_subjects(data_dir, courses=courses)
    universities = load_universities(data_dir)

    events = load_events(data_dir)

    material_topics = load_material_topics(data_dir)

    return universities, subjects, courses, course_topics, events, material_topics
