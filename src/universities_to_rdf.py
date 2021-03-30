from graph import graph, RDF, RDFS, OWL, FOAF, VIVO, STUDYBOT
from util import to_snake_case

from rdflib import URIRef, Literal


def convert(universities):
    for i, row in universities.iterrows():
        name = row['Name']
        sameAs = row['Same As']
        uni_resource = STUDYBOT[to_snake_case(name)]
        same_as_resource = URIRef(sameAs)

        graph.add((
            uni_resource, RDF.type, VIVO.University
        ))
        graph.add((
            uni_resource, FOAF.name, Literal(name, lang='en')
        ))
        graph.add((
            uni_resource, RDFS.label, Literal(name, lang='en')
        ))
        graph.add((
            uni_resource, OWL.sameAs, same_as_resource
        ))
