from graph import graph, STUDYBOT, RDF, AIISO


def convert():
    from data import subjects
    
    concordia = STUDYBOT['concordia_university']

    for subject in subjects:
        subject_resource = STUDYBOT[subject]
        graph.add(
            (subject_resource, RDF.type, AIISO.Subject)
        )
        graph.add(
            (concordia, AIISO.teaches, subject_resource)
        )

if __name__ == "__main__":
    convert()
    
    print(graph.serialize(format='turtle').decode('utf-8'))
