import courses_to_rdf
import subjects_to_rdf
import universities_to_rdf
import lecture_to_rdf

from graph import graph

if __name__ == "__main__":
    courses_to_rdf.convert()
    subjects_to_rdf.convert()
    universities_to_rdf.convert()
    lecture_to_rdf.convert()

    graph.serialize('example.n3', format='ntriples')
