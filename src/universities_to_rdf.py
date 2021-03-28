from graph import graph, RDF, OWL, FOAF, VIVO, STUDYBOT
from data import universities
from util import to_snake_case

from rdflib import URIRef, Literal

def convert():
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
            uni_resource, OWL.sameAs, same_as_resource
        ))

if __name__ == "__main__":
    convert()

    print(
        graph.serialize(format='turtle').decode('utf-8')
    )