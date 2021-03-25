import os

import rdflib
import pandas as pd

from rdflib import Namespace, Literal, Graph
from rdflib.namespace import OWL, FOAF, RDF, RDFS


DATA_DIR = './data'
SCHEMA_DIR = os.path.abspath('./schema')

course_catalog = pd.read_csv(os.path.join(
    DATA_DIR, 'CU_SR_OPEN_DATA_CATALOG.csv'),
    encoding='latin1')

course_descriptions = pd.read_csv(os.path.join(
        DATA_DIR, 'CU_SR_OPEN_DATA_CATALOG_DESC.csv'),
        encoding='latin1')

courses = pd.merge(course_catalog, course_descriptions, on='Course ID')

subjects = courses['Subject'].unique()

STUDYBOT = Namespace('http://www.example.org')
STUDY = Namespace(os.path.join('file:///', SCHEMA_DIR, 'study.ttl'))
TEACH = Namespace('http://linkedscience.org/teach/ns#')
AIISO = Namespace('http://purl.org/vocab/aiiso/schema#')
ICAL = Namespace('http://www.w3.org/2002/12/cal#')
VIVO = Namespace('http://vivoweb.org/ontology/core')

g = Graph()

g.base = STUDYBOT
g.bind('study', STUDY)
g.bind('study', STUDY)
g.bind('teach', TEACH)
g.bind('vivo', VIVO)
g.bind('ical', ICAL)
g.bind('foaf', FOAF)
g.bind('rdfs', RDFS)
g.bind('rdf', RDF)
g.bind('owl', OWL)

for subject in subjects:
    subject_resource = STUDYBOT[subject]
    g.add(
        (subject_resource, RDF.type, STUDY.Subject)
    )

s = g.serialize(format='turtle').decode('utf-8')
print(s)
