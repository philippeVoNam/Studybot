import logging
import os

from SPARQLWrapper import JSON, SPARQLWrapper

SPARQL_SERVER = os.environ.get(
    'SPARQL_SERVER', "http://192.168.2.19:3030/studybot/sparql")
sparql = SPARQLWrapper(SPARQL_SERVER)
sparql.setReturnFormat(JSON)

logger = logging.getLogger('studybot')


def setQuery(query):
    sparql.setQuery(f"""
        PREFIX study: <file:///schema/study.ttl/>
        PREFIX studybot: <file:///data/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX teach: <http://linkedscience.org/teach/ns#>
        PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#>
        PREFIX ical: <http://www.w3.org/2002/12/cal#>

        {query}""")
    logger.info(sparql.queryString)
    return sparql.queryString

def get_course_description(course_subject, course_number):
    setQuery(f"""
        SELECT ?description WHERE {{
            studybot:{course_subject}-{course_number} teach:courseDescription ?description .
        }} LIMIT 1
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return bindings[0]['description']['value']
    else:
        return None


def get_event_topics(course_subject, course_number, event, number):
    setQuery(f"""
        SELECT ?topic ?topicLabel WHERE {{
            studybot:{course_subject}-{course_number} study:hasCourseEvent ?event .
            ?event a study:{event} .
            ?event study:eventNumber {number} .
            ?event study:hasMaterial ?material .
            ?material foaf:topic ?topic .
            ?topic rdfs:label ?topicLabel .
            FILTER (lang(?topicLabel) = 'en')
        }} GROUP BY ?topic ?topicLabel
        ORDER BY DESC(count(1))
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return list(map(lambda b: f"{b['topicLabel']['value']} ({b['topic']['value']})", bindings))
    else:
        return None


def get_courses_by_topic(topic):
    setQuery(f"""
        SELECT ?courseName WHERE {{
            ?course a teach:Course .
            ?course foaf:name ?courseName .
            ?course study:hasCourseEvent ?event .
            ?event study:hasMaterial ?material .
            ?material foaf:topic ?topic .
            ?topic rdfs:label ?topicLabel .
            FILTER (lang(?topicLabel) = 'en')
            FILTER (contains(lcase(?topicLabel), '{topic.lower()}') || contains('{topic.lower()}', lcase(?topicLabel)))
        }} GROUP BY ?courseName
        ORDER BY DESC(count(1))
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return list(map(lambda b: f"{b['courseName']['value']}", bindings))
    else:
        return None


def get_courses_by_subject(subject):
    setQuery(f"""
        SELECT ?courseName WHERE {{
            ?course a teach:Course .
            ?course study:courseSubject ?subject .
            ?subject foaf:name '{subject.upper()}'@en .
            ?course teach:courseTitle ?courseName .
        }}
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return list(map(lambda b: f"{b['courseName']['value']}", bindings))
    else:
        return None


def get_course_name(course_subject, course_number):
    setQuery(f"""
        SELECT ?name WHERE {{
            studybot:{course_subject}-{course_number} teach:courseTitle ?name .
        }} LIMIT 1
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return bindings[0]['name']['value']
    else:
        return None


def get_courses_by_event(event):
    setQuery(f"""
        SELECT DISTINCT ?courseName WHERE {{
            ?course a teach:Course .
            ?course teach:courseTitle ?courseName .
            ?course study:hasCourseEvent ?event .
            ?event a study:{event} .
        }}
    """)
    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return list(map(lambda b: f"{b['courseName']['value']}", bindings))
    else:
        return None


def get_course_outline_location(course_subject, course_number):
    setQuery(f"""
        SELECT ?outline WHERE {{
            studybot:{course_subject}-{course_number} teach:hasCourseMaterial ?material .
            ?material rdf:type study:CourseOutline .
            ?material rdf:resource ?outline .
        }} LIMIT 1
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return bindings[0]['outline']['value']
    else:
        return None


def get_material_location(course_subject, course_number, event, event_number, material):
    setQuery(f"""
        SELECT ?resource WHERE {{
            studybot:{course_subject}-{course_number} study:hasCourseEvent ?event .
            ?event a study:{event} .
            ?event study:eventNumber {event_number} .
            ?event study:hasMaterial ?material .
            ?material a study:{material} .
            ?material rdf:resource ?resource .
        }}
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return list(map(lambda b: f"{b['resource']['value']}", bindings))
    else:
        return None


def get_more_info(topic):
    setQuery(f"""
        SELECT ?seeAlso WHERE {{
            ?topic rdfs:seeAlso ?seeAlso .
            ?topic rdfs:label ?topicLabel .
            FILTER (lang(?topicLabel) = 'en')
            FILTER (contains(lcase(?topicLabel), '{topic.lower()}') || contains('{topic.lower()}', lcase(?topicLabel)))
        }}
    """)

    results = sparql.queryAndConvert()['results']
    bindings = results['bindings']
    if bindings:
        return list(map(lambda b: f"{b['seeAlso']['value']}", bindings))
    else:
        return None
