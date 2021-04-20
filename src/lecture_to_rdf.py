 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
from pathlib import Path
from rdflib import Literal, URIRef, BNode

import os

from graph import graph, STUDYBOT, STUDY, RDF, FOAF

from courses_to_rdf import get_course_resource


def get_event_resource(event):
    courseTitle = event['CourseTitle']
    type_x = event['Type_x']
    number = event['Number']
    return STUDYBOT[f'{courseTitle}_{type_x}_{number}']

def get_material_topics(material_topics, materialID):
    topics = list(material_topics[material_topics['MaterialID'] == materialID]['Topic'])
    return topics

def convert(events, courses, course_topics, material_topics):
    for i, event in events.iterrows():
        event_ref = get_event_resource(event)
        eventType = event["Type_x"]
        eventCourseID = event["CourseID"]
        eventNumber = int(event["Number"])
        eventTitle = event["Title"]
        materialType = event["Type_y"]
        materialLink = event["Link"]
        materialID = event["MaterialID"]

        if not materialLink.startswith('http'):
            materialLink = os.path.join('file:///', materialLink)

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
        
        # add the topics to the material node
        topics = get_material_topics(material_topics, materialID)
        for topic in topics:
            graph.add((
                material_node, FOAF.topic, URIRef(topic)
            ))

        graph.add((
            event_ref, STUDY.hasMaterial, material_node
        ))

        # FIXME : should we get rid of this ? (since we already link the topics to the materials itself)
        # topics = list(course_topics[course_topics['Course ID'] == eventCourseID]['Topic'])
        # for topic in topics:
            # graph.add((
                # event_ref, FOAF.topic, URIRef(topic)
            # ))

        course = courses[courses['Course ID'] == eventCourseID].iloc[0]
        course_ref = get_course_resource(course)

        graph.add((
            course_ref, STUDY.courseEvent, event_ref
        ))


    return graph
