import rdflib
import glob

import os

graph = rdflib.Graph()
graph.parse('studybot.n3', format="ntriples")

query_files = glob.glob('./queries/*.txt')

for query_file in query_files:
    file_location = os.path.dirname(query_file)
    file_name = os.path.basename(query_file)
    query_name = file_name.split('.')[0]
    
    print('running', query_name)

    with open(query_file) as fh:
        query = fh.read()
        
        results = graph.query(query)
        results.serialize(os.path.join(file_location, f'{query_name}.out.csv'), format='csv')