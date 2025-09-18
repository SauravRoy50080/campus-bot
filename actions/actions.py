from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime
import re

# ✅ Custom Action: Check Admission Period
class ActionCheckAdmissionPeriod(Action):

    def name(self) -> Text:
        return "action_check_admission_period"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Example: admission is open from June to August
        current_month = datetime.now().month
        if 6 <= current_month <= 8:
            dispatcher.utter_message(
                text="✅ Admissions are currently open! You can apply online through our portal."
            )
        else:
            dispatcher.utter_message(
                text="🚫 Admissions are currently closed. They usually open from June to August each year."
            )
        return []


# ✅ Custom Action: Get Fees
class ActionGetFees(Action):

    def name(self) -> Text:
        return "action_get_fees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract entity if available
        course = next(tracker.get_latest_entity_values("course_name"), None)

        # Example fee structure
        fees = {
            "engineering": "₹1,20,000 per year",
            "arts": "₹50,000 per year",
            "science": "₹80,000 per year",
            "business": "₹1,00,000 per year"
        }

        if course and course.lower() in fees:
            dispatcher.utter_message(
                text=f"💰 The fee for {course.title()} is {fees[course.lower()]}."
            )
        else:
            dispatcher.utter_message(
                text="💰 Here is the general fee structure:\n"
                     "- Engineering: ₹1,20,000/year\n"
                     "- Arts: ₹50,000/year\n"
                     "- Science: ₹80,000/year\n"
                     "- Business: ₹1,00,000/year\n"
                     "👉 Please specify a course for detailed fees."
            )
        return []


# ✅ Admission Form Validation
class ValidateAdmissionForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_admission_form"

    # Validate Name
    def validate_name(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        if len(slot_value.strip().split()) >= 2:  # At least first + last name
            return {"name": slot_value}
        else:
            dispatcher.utter_message(text="⚠️ Please provide your full name (first and last).")
            return {"name": None}

    # Validate Email
    def validate_email(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, slot_value):
            return {"email": slot_value}
        else:
            dispatcher.utter_message(text="⚠️ That doesn’t look like a valid email. Please try again.")
            return {"email": None}

    # Validate Program
    def validate_program(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        valid_programs = ["engineering", "arts", "science", "business"]
        if slot_value.lower() in valid_programs:
            return {"program": slot_value}
        else:
            dispatcher.utter_message(
                text="⚠️ Please choose a valid program: Engineering, Arts, Science, or Business."
            )
            return {"program": None}
