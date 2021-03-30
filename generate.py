import argparse
import sys

sys.path.append('./src')

import src.courses_to_rdf as courses_to_rdf
import src.subjects_to_rdf as subjects_to_rdf
import src.universities_to_rdf as universities_to_rdf
import src.lecture_to_rdf as lecture_to_rdf

from graph import graph

from data import load_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('out', type=str)
    parser.add_argument('--data', type=str, help="path to the data files")
    parser.add_argument('--schema', type=str, default="./schema/study.ttl", help="path to the STUDY schema")
    parser.add_argument('--base', type=str, default="http://example.org", help="base to use for STUDYBOT URIs")
    parser.add_argument('--format', default='ntriples', type=str, help="serialization format for the graph")
    args = parser.parse_args()


    universities, subjects, courses, course_topics, events = load_data(args.data)

    courses_to_rdf.convert(courses, course_topics)
    subjects_to_rdf.convert(subjects)
    universities_to_rdf.convert(universities)
    lecture_to_rdf.convert(events, courses)

    graph.serialize(args.out, format=args.format)
