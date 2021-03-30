from graph import graph, STUDYBOT, RDF, RDFS, AIISO, FOAF

from rdflib import Literal


def convert(subjects):    
    concordia = STUDYBOT['concordia_university']

    for subject in subjects:
        subject_resource = STUDYBOT[subject]
        graph.add(
            (subject_resource, RDF.type, AIISO.Subject))
        graph.add(
            (subject_resource, FOAF.name, Literal(subject, lang='en')))
        graph.add(
            (subject_resource, RDFS.label, Literal(subject, lang='en')))
        graph.add(
            (concordia, AIISO.teaches, subject_resource))
