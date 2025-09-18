from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from googletrans import Translator

# Initialize translator
translator = Translator()

class ActionSetLanguage(Action):
    def name(self) -> Text:
        return "action_set_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        language = tracker.get_slot("language")
        if language:
            dispatcher.utter_message(text=f"Language set to {language}")
        return [SlotSet("language", language)]

class ActionProvideAdmissionInfo(Action):
    def name(self) -> Text:
        return "action_provide_admission_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get detected language from message or slot
        detected_lang = tracker.get_slot("language") or "en"
        
        # Get original message if available
        original_text = None
        for event in tracker.events:
            if event.get("event") == "user":
                original_text = event.get("metadata", {}).get("original_text")
                if original_text:
                    break
        
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
