# import parser object from tike
from tika import parser  
import spacy
import pandas as pd
from pathlib import Path
import os
from progress.bar import Bar

"""
FIXME :
materialID that did not work : [23,25,34]
"""

def read_df_material(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    return lines

def output_2_file(data):
    # cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
    cities = pd.DataFrame(data, columns=['MaterialID', 'Topic'])
    cities.to_csv('course_material_topics_error.csv', index=False)

def extract_entities(data_str, materialID):
    nlp = spacy.blank('en')
    nlp.add_pipe('dbpedia_spotlight')

    doc = nlp(data_str)

    data = []
    for ent in doc.ents:
        if [materialID, ent.kb_id_] not in data:
            data.append([materialID, ent.kb_id_])
    
    return data

if __name__ == "__main__":

    df_materials = read_df_material("data/lecture_data/df_material.csv")

    bar = Bar('Processing', max=len(df_materials))

    topic_data = []
    error_files = []
    target_list = ["11", "35", "36", "38", "53"] # NOTE : here is the materialIDs that did not work, the scanner now tries to get them (ie. if eventID in target_list)
    for df_material in df_materials:
        bar.next()

        file_ = df_material.split(",")
        filep = "local_dataset/" + file_[3]
        filep = os.path.abspath(filep)

        materialID = file_[2]

        my_file = Path(filep.strip())
        filepath = filep.strip()

        if materialID in target_list:
            if my_file.is_file():
                # opening pdf file
                parsed= parser.from_file(filepath)
                  
                # saving content of pdf
                # you can also bring text only, by parsed_pdf['text'] 
                # parsed_pdf['content'] returns string 
                data = parsed['content'] 
                  
            try:
                data_ents = extract_entities(data, materialID)

                topic_data = topic_data + data_ents

            except Exception as e:
                print(e)
                error_files.append(file_)

    output_2_file(topic_data)

    print("--- ERROR FILES ---")
    for error_file in error_files:
        print(error_file)

    bar.finish()
