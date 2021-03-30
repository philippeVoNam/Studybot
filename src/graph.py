import os

from rdflib import Namespace, Graph
from rdflib.namespace import OWL, FOAF, RDF, RDFS

from config import Config

STUDYBOT = Namespace(
    Config.base_url)
STUDY = Namespace(
    Config.schema_file)
TEACH = Namespace('http://linkedscience.org/teach/ns#')
AIISO = Namespace('http://purl.org/vocab/aiiso/schema#')
ICAL = Namespace('http://www.w3.org/2002/12/cal#')
VIVO = Namespace('http://vivoweb.org/ontology/core')

graph = Graph()
graph.base = STUDYBOT
graph.bind('study', STUDY)
graph.bind('teach', TEACH)
graph.bind('aiiso', AIISO)
graph.bind('vivo', VIVO)
graph.bind('ical', ICAL)
graph.bind('foaf', FOAF)
graph.bind('rdfs', RDFS)
graph.bind('rdf', RDF)
graph.bind('owl', OWL)
