# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .sparql import (get_course_description, get_course_name,
                     get_course_outline_location, get_courses_by_event,
                     get_courses_by_subject, get_courses_by_topic,
                     get_event_topics, get_material_location, get_more_info)

logger = logging.getLogger('studybot')
logger.setLevel(logging.INFO)


def get_lastest_entity_value_or_none(tracker: Tracker, entity: Text):
    return next(tracker.get_latest_entity_values(entity), None)


class ActionAboutCourse(Action):

    def name(self) -> Text:
        return "action_about_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_subject = get_lastest_entity_value_or_none(
            tracker, 'course_subject')
        course_number = get_lastest_entity_value_or_none(
            tracker, 'course_number')

        logger.info('%s - course_subject=%s course_number=%s',
                    self.name(), course_subject, course_number)

        if not all([course_subject, course_number]):
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        description = get_course_description(course_subject, course_number)

        logger.info('%s : results - course_subject=%s course_number=%s description=%s',
                    self.name(), course_subject, course_number, description)

        if description:
            dispatcher.utter_message(text=description)
        else:
            dispatcher.utter_message(response="utter_no_results")

        return []


class ActionEventTopics(Action):

    def name(self) -> Text:
        return "action_event_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        event_number = get_lastest_entity_value_or_none(
            tracker, 'CARDINAL')
        course_subject = get_lastest_entity_value_or_none(
            tracker, 'course_subject')
        course_number = get_lastest_entity_value_or_none(
            tracker, 'course_number')
        event = get_lastest_entity_value_or_none(tracker, 'event')

        logger.info('%s - event=%s event_number=%s course_subject=%s, course_number=%s',
                    self.name(), event, event_number, course_subject, course_number)

        try:
            event_number = int(event_number)
        except ValueError:
            event_number = None

        if event is None:
            pass
        elif event.lower() == 'lab':
            event = 'Lab'
        elif event.lower() == 'lecture':
            event = 'Lecture'
        elif event.lower() == 'tutorial':
            event = 'Tutorial'
        else:
            event = None

        if not all([course_number, course_subject, event, event_number]):
            dispatcher.utter_message(response='utter_no_understand')
            return []

        topics = get_event_topics(
            course_subject, course_number, event, event_number)
        topics = ['Example Topic']

        logger.info('%s : results - course_subject=%s course_number=%s topics=%s',
                    self.name(), course_subject, course_number, topics)
        if not topics:
            dispatcher.utter_message(response="utter_no_results")
            return []

        topic_list = ', '.join(topics)
        dispatcher.utter_message(response='utter_course_topic_results',
                                 topics=topic_list,
                                 course_subject=course_subject,
                                 course_number=course_number,
                                 event=event,
                                 event_number=event_number)

        return []


class ActionSearchByTopic(Action):

    def name(self) -> Text:
        return "action_search_by_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic = get_lastest_entity_value_or_none(tracker, 'topic')

        logger.info('%s - topic=%s',
                    self.name(), topic)

        if topic is None:
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        courses = get_courses_by_topic(topic)

        logger.info('%s : results - topic=%s courses=%s',
                    self.name(), topic, courses)

        if not courses:
            dispatcher.utter_message(response="utter_no_results")
            return []

        course_list = ', '.join(courses)
        dispatcher.utter_message(response='utter_courses_with_topic_results',
                                 courses=course_list,
                                 topic=topic)

        return []


class ActionSearchBySubject(Action):

    def name(self) -> Text:
        return "action_search_by_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_subject = get_lastest_entity_value_or_none(
            tracker, 'course_subject')

        logger.info('%s - course_subject=%s',
                    self.name(), course_subject)

        if course_subject is None:
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        courses = get_courses_by_subject(course_subject)

        logger.info('%s : results - course_subject=%s courses=%s',
                    self.name(), course_subject, courses)

        if not courses:
            dispatcher.utter_message(response="utter_no_results")
            return []

        course_list = ', '.join(courses)
        dispatcher.utter_message(response='utter_courses_in_subject',
                                 courses=course_list,
                                 course_subject=course_subject)

        return []


class ActionLookupCourseName(Action):

    def name(self) -> Text:
        return "action_lookup_course_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_subject = get_lastest_entity_value_or_none(
            tracker, 'course_subject')

        course_number = get_lastest_entity_value_or_none(
            tracker, 'course_number')

        logger.info('%s - course_subject=%s course_number=%s',
                    self.name(), course_subject, course_number)

        if not all([course_subject, course_number]):
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        name = get_course_name(course_subject, course_number)

        logger.info('%s : results - course_subject=%s course_number=%s name=%s',
                    self.name(), course_subject, course_number, name)

        if not name:
            dispatcher.utter_message(response="utter_no_results")
            return []

        dispatcher.utter_message(response='utter_course_name',
                                 name=name,
                                 course_subject=course_subject,
                                 course_number=course_number)

        return []


class ActionSearchByEvent(Action):

    def name(self) -> Text:
        return "action_search_by_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        event = get_lastest_entity_value_or_none(
            tracker, 'event')

        logger.info('%s - event=%s',
                    self.name(), event)

        if event is None:
            pass
        elif event.lower() == 'lab':
            event = 'Lab'
        elif event.lower() == 'lecture':
            event = 'Lecture'
        elif event.lower() == 'tutorial':
            event = 'Tutorial'
        else:
            event = None

        if not all([event]):
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        courses = get_courses_by_event(event)

        logger.info('%s : results - event=%s courses=%s',
                    self.name(), event, courses)

        if not courses:
            dispatcher.utter_message(response="utter_no_results")
            return []

        course_list = ', '.join(courses)
        dispatcher.utter_message(response='utter_courses_with_event',
                                 courses=course_list,
                                 event=event)

        return []


class ActionFindOutline(Action):

    def name(self) -> Text:
        return "action_find_outline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_subject = get_lastest_entity_value_or_none(
            tracker, 'course_subject')

        course_number = get_lastest_entity_value_or_none(
            tracker, 'course_number')

        logger.info('%s - course_subject=%s course_number=%s',
                    self.name(), course_subject, course_number)

        if not all([course_subject, course_number]):
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        location = get_course_outline_location(course_subject, course_number)

        logger.info('%s : results - course_subject=%s course_number=%s courses=%s',
                    self.name(), course_subject, course_number, location)

        if not location:
            dispatcher.utter_message(response="utter_no_results")
            return []

        dispatcher.utter_message(response='utter_where_to_find',
                                 url=location)

        return []


class ActionFindMaterial(Action):

    def name(self) -> Text:
        return "action_find_material"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        event_number = get_lastest_entity_value_or_none(
            tracker, 'CARDINAL')
        course_subject = get_lastest_entity_value_or_none(
            tracker, 'course_subject')
        course_number = get_lastest_entity_value_or_none(
            tracker, 'course_number')
        event = get_lastest_entity_value_or_none(tracker, 'event')
        material = get_lastest_entity_value_or_none(tracker, 'material')

        logger.info('%s - event=%s event_number=%s course_subject=%s, course_number=%s material=%s',
                    self.name(), event, event_number, course_subject, course_number, material)

        try:
            event_number = int(event_number)
        except ValueError:
            event_number = None

        if event is None:
            pass
        elif event.lower() == 'lab':
            event = 'Lab'
        elif event.lower() == 'lecture':
            event = 'Lecture'
        elif event.lower() == 'tutorial':
            event = 'Tutorial'
        else:
            event = None

        if material is None:
            pass
        elif material.lower() == 'slides':
            material = 'Slides'
        elif material.lower() == 'worksheet':
            material = 'Worksheet'
        elif material.lower() == 'reading':
            material = 'Reading'
        else:
            material = None

        if not all([course_number, course_subject, event, event_number, material]):
            dispatcher.utter_message(response='utter_no_understand')
            return []

        locations = get_material_location(
            course_subject, course_number, event, event_number, material)

        logger.info('%s : results - course_subject=%s course_number=%s material=%s locations=%s',
                    self.name(), course_subject, course_number, material, locations)

        if not locations:
            dispatcher.utter_message(response="utter_no_results")
            return []

        location_list = ', '.join(locations)
        dispatcher.utter_message(response='utter_where_to_find',
                                 url=location_list)

        return []


class ActionMoreInfo(Action):

    def name(self) -> Text:
        return "action_more_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic = get_lastest_entity_value_or_none(
            tracker, 'topic')

        logger.info('%s - topic=%s',
                    self.name(), topic)

        if not all([topic]):
            dispatcher.utter_message(
                response='utter_no_understand')
            return []

        locations = get_more_info(topic)

        logger.info('%s : results - topic=%s locations=%s',
                    self.name(), topic, locations)

        if not locations:
            dispatcher.utter_message(response="utter_no_results")
            return []

        location_list = ', '.join(locations)
        dispatcher.utter_message(response='utter_where_to_find',
                                 url=location_list)

        return []
