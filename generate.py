import argparse
import sys

sys.path.append('./src')

from config import Config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('out', type=str)
    parser.add_argument('--data', default="./data", type=str, help="path to the data files")
    parser.add_argument('--schema', type=str, default="file:///./schema/study.ttl/", help="path to the STUDY schema")
    parser.add_argument('--base', type=str, default="file:///./data/", help="base to use for STUDYBOT URIs")
    parser.add_argument('--format', default='ntriples', type=str, help="serialization format for the graph")
    args = parser.parse_args()

    Config.base_url = args.base
    Config.schema_file = args.schema

    # Imports are here so that the Config changes will take effect
    from graph import graph

    import src.courses_to_rdf as courses_to_rdf
    import src.subjects_to_rdf as subjects_to_rdf
    import src.universities_to_rdf as universities_to_rdf
    import src.lecture_to_rdf as lecture_to_rdf

    from data import load_data

    universities, subjects, courses, course_topics, events = load_data(args.data)

    courses_to_rdf.convert(courses, course_topics)
    subjects_to_rdf.convert(subjects)
    universities_to_rdf.convert(universities)
    lecture_to_rdf.convert(events)

    graph.serialize(args.out, format=args.format)
