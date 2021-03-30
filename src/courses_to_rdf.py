import os
from graph import graph, STUDYBOT, TEACH, AIISO, STUDY, RDF, RDFS, FOAF

from rdflib import Literal, URIRef, BNode


def get_course_resource(course):
    subj = course['Subject']
    cat = course['Catalog']
    return STUDYBOT[f'{subj}-{cat}']


def get_course_subject(course):
    subj = course['Subject']
    return STUDYBOT[subj] # <http://www.example.org/SUBJ>


def convert(courses, course_topics):
    courses['See Also'] = courses['See Also'].fillna('missing')
    courses['Outline'] = courses['Outline'].fillna('missing')

    concordia = STUDYBOT.concordia_university

    for i, course in courses.iterrows():
        course_ref = get_course_resource(course)
        subj = get_course_subject(course)
        title = course['Long Title']
        courseNumber = course['Catalog']
        desc = course['Descr']

        graph.add((
            course_ref, RDF.type, TEACH.Course
        ))
        graph.add((
            concordia, AIISO.teaches, course_ref
        ))
        graph.add((
            course_ref, TEACH.courseTitle, Literal(title, lang='en')
        ))
        graph.add((
            course_ref, RDFS.label, Literal(title, lang='en')
        ))
        graph.add((
            course_ref, TEACH.courseDescription, Literal(desc, lang='en')
        ))
        graph.add((
            course_ref, RDFS.comment, Literal(desc, lang='en')
        ))
        graph.add((
            course_ref, STUDY.courseSubject, subj
        ))
        graph.add((
            course_ref, STUDY.courseNumber, Literal(courseNumber)
        ))

        see_also = course['See Also']
        outline = course['Outline']
        topics = list(course_topics[course_topics['Course ID'] == course['Course ID']]['Topic'])

        for topic in topics:
            graph.add((
                course_ref, FOAF.topic, URIRef(topic)
            ))

        if see_also != 'missing':
            graph.add((
                course_ref, RDFS.seeAlso, URIRef(see_also)
            ))
        if outline != 'missing':
            if not outline.startswith('http'):
                outline = os.path.join('file:///', outline)

            outline_node = BNode()
            graph.add((
                outline_node, RDF.type, STUDY.CourseOutline
            ))
            graph.add((
                outline_node, RDF.resource, URIRef(outline)
            ))
            graph.add((
                course_ref, TEACH.hasCourseMaterial, outline_node
            ))
