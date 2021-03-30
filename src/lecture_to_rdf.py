 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
# * Imports
# 3rd Party Imports
from pathlib import Path
import os
import pandas as pd
from rdflib import Literal, URIRef, BNode
# User Imports
from graph import graph, STUDYBOT, TEACH, STUDY, RDF, RDFS, FOAF
from constants import DATA_DIR, LECTURE_DATA_DIR

# * Code
def read_csv_files():
    eventCSV = pd.read_csv(os.path.join(
        LECTURE_DATA_DIR, 'df_event.csv'),
        encoding='latin1')

    eventLinkCSV = pd.read_csv(os.path.join(
        LECTURE_DATA_DIR, 'df_event_link.csv'),
        encoding='latin1')

    materialCSV = pd.read_csv(os.path.join(
        LECTURE_DATA_DIR, 'df_material.csv'),
        encoding='latin1')

    lectureDataCSV = pd.merge(eventCSV, eventLinkCSV, on='EventID', how="left")
    lectureDataCSV = pd.merge(lectureDataCSV, materialCSV, on='EventID')

    return lectureDataCSV

def get_event_resource(event):
    courseTitle = event['CourseTitle']
    type_x = event['Type_x']
    number = event['Number']
    return STUDYBOT[f'{courseTitle}_{type_x}_{number}']

def convert():
    events = read_csv_files()
    # events.to_csv("info.csv", index = False)
    # print(events)

    for i, event in events.iterrows():
        event_ref = get_event_resource(event)
        eventType = event["Type_x"]
        eventNumber = event["Number"]
        eventTitle = event["Title"]
        materialType = event["Type_y"]
        materialLink = event["Link"]



        if eventType == "Lectures":
            graph.add((
                event_ref, RDF.type, STUDY.Lecture
            ))

        elif eventType == "tutorial":
            graph.add((
                event_ref, RDF.type, STUDY.Tutorial
            ))

        elif eventType == "lab":
            graph.add((
                event_ref, RDF.type, STUDY.Lab
            ))

        graph.add((
            event_ref, FOAF.name, Literal(eventTitle, lang='en')
        ))

        graph.add((
            event_ref, STUDY.eventNumber, Literal(eventNumber, lang='en')
        ))

        material_node = BNode()
        if materialType == "slides":
            graph.add((
                material_node, RDF.type, STUDY.Slides
            ))
        elif materialType == "worksheets":
            graph.add((
                material_node, RDF.type, STUDY.Worksheet
            ))
        else:
            graph.add((
                material_node, RDF.type, STUDY.Reading
            ))

        graph.add((
            material_node, RDF.resource, URIRef(materialLink)
        ))
        graph.add((
            event_ref, STUDY.hasMaterial, material_node
        ))

    return graph

if __name__ == "__main__":
    graph = convert()
    graph.serialize(destination='lecture_data.ttl', format='turtle')
