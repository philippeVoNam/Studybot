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

def get_all_topics(material_topics):
    topics_labels = material_topics[["Topic", "Label"]]
    distinct_topics_label = list(dict.fromkeys(topics_labels))
    return distinct_topics_label

def convert(events, courses, course_topics, material_topics):

    lectureEventDict = {}
    tutorial_lab_events = []
    for i, event in events.iterrows():
        event_ref = get_event_resource(event)
        eventType = event["Type_x"]
        eventCourseID = event["CourseID"]
        eventNumber = int(event["Number"])
        eventTitle = event["Title"]
        materialType = event["Type_y"]
        materialLink = event["Link"]
        materialID = event["MaterialID"]

        # FIXME : not sure here
        lectureEventIDLink = event["LectureEventID"]
        eventID = event["EventID"]

        if not materialLink.startswith('http'):
            materialLink = os.path.join('file:///', materialLink)

        if eventType == "Lectures":
            graph.add((
                event_ref, RDF.type, STUDY.Lecture
            ))

            lectureEventDict[eventID] = event_ref

        elif eventType == "tutorial":
            graph.add((
                event_ref, RDF.type, STUDY.Tutorial
            ))

            tutorial_lab_events.append(event)


        elif eventType == "lab":
            graph.add((
                event_ref, RDF.type, STUDY.Lab
            ))

            tutorial_lab_events.append(event)

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

    # make link from tutorial/lab to lecture event
    for event in tutorial_lab_events:
        event_ref = get_event_resource(event)
        lectureEventIDLink = event["LectureEventID"]

        graph.add((
            event_ref, STUDY.hasCourseEvent, lectureEventDict[lectureEventIDLink]
        ))

    # make topic node with label
    all_topics_labels = get_all_topics(material_topics)
    for topic_label in all_topics_labels:
        topic = topic_label[0]
        label = topic_label[1]
        graph.add((
            URIRef(topic), RDFS.label, Literal(label, lang='en')
        ))

    return graph
