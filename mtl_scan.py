from tika import parser  
import spacy
import pandas as pd
from pathlib import Path
import os
from progress.bar import Bar
from SPARQLWrapper import SPARQLWrapper, JSON

def read_CSV(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    return lines

def output_2_file(data):
    cities = pd.DataFrame(data, columns=['MaterialID', 'Topic'])
    cities.to_csv('course_material_topics.csv', index=False)

def output_2_file_w_label(data):
    cities = pd.DataFrame(data, columns=['MaterialID', 'Topic', 'Label'])
    cities.to_csv('course_material_topics_w_label.csv', index=False)

def get_label(topic_uri, sparql):

    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {{ <{}> rdfs:label ?label .
        filter(langMatches(lang(?label),"EN"))
        }}
        
    """.format(topic_uri))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result["label"]["value"]

def extract_entities(data_str, materialID):
    nlp = spacy.blank('en')
    nlp.add_pipe('dbpedia_spotlight')

    doc = nlp(data_str)

    data = []
    for ent in doc.ents:
        if [materialID, ent.kb_id_] not in data:
            data.append([materialID, ent.kb_id_])
    
    return data, ent.kb_id_

def scan():
    df_materials = read_CSV("data/lecture_data/df_material.csv")


    bar = Bar('Processing', max=len(df_materials))

    topic_data = []
    error_files = []
    target_list = ["36"] # NOTE : here is the materialIDs that did not work, the scanner now tries to get them (ie. if eventID in target_list)
    targetFlag = True
    for df_material in df_materials:
        bar.next()

        file_ = df_material.split(",")
        filep = "local_dataset/" + file_[3]
        filep = os.path.abspath(filep)

        materialID = file_[2]

        my_file = Path(filep.strip())
        filepath = filep.strip()

        if targetFlag:
            if materialID in target_list:
                if my_file.is_file():
                    # opening pdf file
                    parsed= parser.from_file(filepath)
                      
                    # saving content of pdf
                    # you can also bring text only, by parsed_pdf['text'] 
                    # parsed_pdf['content'] returns string 
                    data = parsed['content'] 
                      
                try:
                    data_ents, ent_topic = extract_entities(data, materialID)

                    topic_data = topic_data + data_ents

                except Exception as e:
                    print(e)
                    error_files.append(file_)

        else:
            if my_file.is_file():
                # opening pdf file
                parsed= parser.from_file(filepath)
                  
                # saving content of pdf
                # you can also bring text only, by parsed_pdf['text'] 
                # parsed_pdf['content'] returns string 
                data = parsed['content'] 
                  
            try:
                data_ents, ent_topic = extract_entities(data, materialID)

                topic_data = topic_data + data_ents

            except Exception as e:
                print(e)
                error_files.append(file_)

    output_2_file(topic_data)

    print("--- ERROR FILES ---")
    for error_file in error_files:
        print(error_file)

    bar.finish()

def stats():
    topics = read_CSV("data/lecture_data/course_material_topics.csv")

    topics.pop(0)
    
    distinct_topics_uri = []
    comp_topics = []
    soen_topics = []

    bar = Bar('Processing', max=len(topics))

    for topic in topics:
        bar.next()

        topic = topic.split(",")
        materialID = int(topic[0])
        topic_uri = topic[1]

        distinct_topics_uri.append(topic_uri)

        if materialID <= 26:
            comp_topics.append(topic)
        else:
            soen_topics.append(topic)

    bar.finish()

    print("Total number triples for topics = {}".format(len(topics)))

    distinct_topics_uri = list(dict.fromkeys(distinct_topics_uri))
    print("Total number of distinct topics = {}".format(len(distinct_topics_uri)))

    print("Total number of topics in COMP-474 = {}".format(len(comp_topics)))
    print("Total number of topics in SOEN-343 = {}".format(len(soen_topics)))

def gen_labels():
    topics = read_CSV("data/lecture_data/course_material_topics.csv")

    topics.pop(0)
    
    distinct_topics_uri = []
    comp_topics = []
    soen_topics = []

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    bar = Bar('Processing', max=len(topics))

    data = []
    count = 0
    maxC = 10
    for topic in topics:
        bar.next()

        try:
            topic = topic.split(",")
            materialID = int(topic[0])
            topic_uri = topic[1].strip()
            label = get_label(topic_uri, sparql)

        except Exception as e:
            topic_uri = topic[1].strip()
            label = "NA"

        data.append([materialID, topic_uri, label])

        distinct_topics_uri.append(topic_uri)

        if materialID <= 26:
            comp_topics.append(topic)
        else:
            soen_topics.append(topic)

        # count += 1
        # if count > maxC:
            # break
            
    bar.finish()

    output_2_file_w_label(data)

if __name__ == "__main__":
    scan()
