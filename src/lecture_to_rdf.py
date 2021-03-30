 # * author : Philippe Vo 
 # * date : Mar-25-2021 13:57:57
 
from pathlib import Path
from rdflib import Literal, URIRef, BNode

from graph import graph, STUDYBOT, STUDY, RDF, FOAF


def get_event_resource(event):
    courseTitle = event['CourseTitle']
    type_x = event['Type_x']
    number = event['Number']
    return STUDYBOT[f'{courseTitle}_{type_x}_{number}']

def get_course_resource(course):
    subj = course['Subject']
    cat = course['Catalog']
    return STUDYBOT[f'{subj}-{cat}']

def convert(events, courses):
    for i, event in events.iterrows():
        event_ref = get_event_resource(event)
        eventType = event["Type_x"]
        eventCourseID = event["CourseID"]
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

        # adding the course events to the course nodes
        # FIXME : for sure it can be done more efficiently
        # FIXME : instead of doing from the event side, it would be more efficient to do it on the course side
        for i, course in courses.iterrows():

            if course["Course ID"] == eventCourseID:
                targetCourse = course

                course_ref = get_course_resource(targetCourse)

                graph.add((
                    course_ref, STUDY.hasCourseEvent, event_ref
                ))

    return graph
