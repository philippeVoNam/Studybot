from graph import graph, STUDYBOT, TEACH, STUDY, RDF, RDFS

from rdflib import Literal, URIRef, BNode


def get_course_resource(course):
    subj = course['Subject']
    cat = course['Catalog']
    return STUDYBOT[f'{subj}-{cat}']


def get_course_subject(course):
    subj = course['Subject']
    return STUDYBOT[subj]


def convert():
    from data import courses

    courses['See Also'] = courses['See Also'].fillna('missing')
    courses['Outline'] = courses['Outline'].fillna('missing')

    for i, course in courses.iterrows():
        res = get_course_resource(course)
        subj = get_course_subject(course)
        title = course['Long Title']
        courseNumber = course['Catalog']
        desc = course['Descr']

        graph.add((
            res, RDF.type, TEACH.Course
        ))
        graph.add((
            res, TEACH.courseTitle, Literal(title, lang='en')
        ))
        graph.add((
            res, TEACH.courseDescription, Literal(desc, lang='en')
        ))
        graph.add((
            res, STUDY.courseSubject, subj
        ))
        graph.add((
            res, STUDY.courseNumber, Literal(courseNumber)
        ))

        see_also = course['See Also']
        outline = course['Outline']
        
        if see_also != 'missing':
            graph.add((
                res, RDFS.seeAlso, URIRef(see_also)
            ))
        if outline != 'missing':
            outline_node = BNode()
            graph.add((
                outline_node, RDF.type, STUDY.CourseOutline
            ))
            graph.add((
                outline_node, RDF.resource, URIRef(outline)
            ))
            graph.add((
                res, TEACH.hasCourseMaterial, outline_node
            ))


if __name__ == "__main__":
    convert()
    
    print(graph.serialize(format='turtle').decode('utf-8'))
