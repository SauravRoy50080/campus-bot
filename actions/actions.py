from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCheckAdmissionPeriod(Action):
    def name(self) -> Text:
        return "action_check_admission_period"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="The admission period for the next semester is from June 1st to August 31st.")
        return []

class ActionGetFees(Action):
    def name(self) -> Text:
        return "action_get_fees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        program = next(tracker.get_latest_entity_values("program"), None)
        
        if program:
            # In a real implementation, you would fetch this from a database
            fees = {
                "engineering": "$10,000 per year",
                "arts": "$8,000 per year",
                "science": "$9,500 per year",
                "business": "$12,000 per year"
            }
            fee_amount = fees.get(program.lower(), "Please contact our office for fee information")
            dispatcher.utter_message(text=f"The fee for {program} is {fee_amount}.")
        else:
            dispatcher.utter_message(text="Which program are you interested in? We have Engineering, Arts, Science, and Business programs.")
        
        return []
