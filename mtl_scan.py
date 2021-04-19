# import parser object from tike
from tika import parser  
import spacy
import pandas as pd
from pathlib import Path
import os
from progress.bar import Bar

"""
FIXME :
eventID that did not work : [23,25,34]
"""

def read_df_material(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    return lines

def output_2_file(data):
    # cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    cities = pd.DataFrame(data, columns=['EventID', 'Topic'])
    cities.to_csv('course_material_topics_error.csv', index=False)

def extract_entities(data_str, eventID):
    nlp = spacy.blank('en')
    nlp.add_pipe('dbpedia_spotlight')

    doc = nlp(data_str)

    data = []
    for ent in doc.ents:
        if [eventID, ent.kb_id_] not in data:
            data.append([eventID, ent.kb_id_])
    
    return data

if __name__ == "__main__":

    df_materials = read_df_material("data/lecture_data/df_material.csv")

    bar = Bar('Processing', max=len(df_materials))

    topic_data = []
    error_files = []
    target_list = ["23","25","34"]
    for df_material in df_materials:
        bar.next()

        file_ = df_material.split(",")
        filep = "local_dataset/" + file_[2]
        filep = os.path.abspath(filep)

        eventID = file_[0]

        my_file = Path(filep.strip())
        filepath = filep.strip()

        if eventID in target_list:
            if my_file.is_file():
                # opening pdf file
                parsed= parser.from_file(filepath)
                  
                # saving content of pdf
                # you can also bring text only, by parsed_pdf['text'] 
                # parsed_pdf['content'] returns string 
                data = parsed['content'] 
                  
            try:
                data_ents = extract_entities(data, eventID)

                topic_data = topic_data + data_ents

            except Exception as e:
                print(e)
                error_files.append(file_)

    output_2_file(topic_data)

    print("--- ERROR FILES ---")
    for error_file in error_files:
        print(error_file)

    bar.finish()
