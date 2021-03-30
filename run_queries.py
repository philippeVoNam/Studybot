import rdflib

import os

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('GRAPH')
    parser.add_argument('QUERIES', type=str, nargs='+', default='./queries/*.txt')
    parser.add_argument('--format', default='ntriples')

    args = parser.parse_args()

    graph = rdflib.Graph()

    print('Parsing graph from', args.GRAPH)
    graph.parse(args.GRAPH, format=args.format)

    for query_file in args.QUERIES:
        file_location = os.path.dirname(query_file)
        file_name = os.path.basename(query_file)
        query_name = file_name.split('.')[0]
        out_path = os.path.join(file_location, f'{query_name}.out.csv')
        
        print('Running query: ', query_file, '...')

        with open(query_file) as fh:
            query = fh.read()
            
            results = graph.query(query)

            print('... saving results to ', out_path)
            results.serialize(out_path, format='csv')