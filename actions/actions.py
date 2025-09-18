from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from googletrans import Translator

# Initialize translator
translator = Translator()

class ActionCheckAdmissionPeriod(Action):
    def name(self) -> Text:
        return "action_check_admission_period"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        detected_lang = tracker.get_slot("language") or "en"
        
        # Base response in English
        response = "The admission period for the next semester is from June 1st to August 31st."
        
        # Translate response to detected language if not English
        if detected_lang != "en":
            try:
                translated_response = translator.translate(response, src='en', dest=detected_lang)
                response = translated_response.text
            except Exception as e:
                print(f"Translation error: {e}")
        
        dispatcher.utter_message(text=response)
        return []

class ActionGetFees(Action):
    def name(self) -> Text:
        return "action_get_fees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        detected_lang = tracker.get_slot("language") or "en"
        program = next(tracker.get_latest_entity_values("program"), None)
        
        # Base response in English
        if program:
            fees = {
                "engineering": "$10,000 per year",
                "arts": "$8,000 per year",
                "science": "$9,500 per year",
                "business": "$12,000 per year"
            }
            response = f"The fee for {program} is {fees.get(program.lower(), 'Please contact our office for fee information')}."
        else:
            response = "Which program are you interested in? We have Engineering, Arts, Science, and Business programs."
        
        # Translate response to detected language if not English
        if detected_lang != "en":
            try:
                translated_response = translator.translate(response, src='en', dest=detected_lang)
                response = translated_response.text
            except Exception as e:
                print(f"Translation error: {e}")
        
        dispatcher.utter_message(text=response)
        return []

class ActionProvideAdmissionInfo(Action):
    def name(self) -> Text:
        return "action_provide_admission_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        detected_lang = tracker.get_slot("language") or "en"
        
        # Base response in English
        response = "To apply for admission:\n1. Complete online application\n2. Submit transcripts\n3. Pay application fee\n4. Attend interview"
        
        # Translate response to detected language if not English
        if detected_lang != "en":
            try:
                translated_response = translator.translate(response, src='en', dest=detected_lang)
                response = translated_response.text
            except Exception as e:
                print(f"Translation error: {e}")
        
        dispatcher.utter_message(text=response)
        return []

class ActionProvideCourseInfo(Action):
    def name(self) -> Text:
        return "action_provide_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        detected_lang = tracker.get_slot("language") or "en"
        
        # Base response in English
        response = "Available courses:\n- Computer Science\n- Engineering\n- Business Administration\n- Psychology"
        
        # Translate response to detected language if not English
        if detected_lang != "en":
            try:
                translated_response = translator.translate(response, src='en', dest=detected_lang)
                response = translated_response.text
            except Exception as e:
                print(f"Translation error: {e}")
        
        dispatcher.utter_message(text=response)
        return []

class ActionProvideFacilityInfo(Action):
    def name(self) -> Text:
        return "action_provide_facility_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        detected_lang = tracker.get_slot("language") or "en"
        facility = next(tracker.get_latest_entity_values("facility_type"), None)
        
        # Base response in English
        if facility:
            facilities = {
                "library": "Library is open 8AM-10PM. Located at Building A, 1st Floor",
                "cafeteria": "Cafeteria is open 7AM-8PM. Located at Building B, Ground Floor",
                "gym": "Gym is open 6AM-11PM. Located at Building C, Ground Floor",
                "labs": "Computer Labs are open 24/7. Located in Building D, 2nd Floor"
            }
            response = facilities.get(facility, "Facility information not available")
        else:
            response = "Available facilities: Library, Cafeteria, Gym, Computer Labs"
        
        # Translate response to detected language if not English
        if detected_lang != "en":
            try:
                translated_response = translator.translate(response, src='en', dest=detected_lang)
                response = translated_response.text
            except Exception as e:
                print(f"Translation error: {e}")
        
        dispatcher.utter_message(text=response)
        return []

class ActionProvideEventInfo(Action):
    def name(self) -> Text:
        return "action_provide_event_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        detected_lang = tracker.get_slot("language") or "en"
        
        # Base response in English
        response = "Upcoming events:\n- Tech Fair: Oct 15, Main Hall\n- Cultural Festival: Oct 20, Auditorium"
        
        # Translate response to detected language if not English
        if detected_lang != "en":
            try:
                translated_response = translator.translate(response, src='en', dest=detected_lang)
                response = translated_response.text
            except Exception as e:
                print(f"Translation error: {e}")
        
        dispatcher.utter_message(text=response)
        return []
