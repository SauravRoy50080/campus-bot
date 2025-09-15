from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ActionGetFee(Action):
    def name(self) -> str:
        return "action_get_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        course = tracker.get_slot("course")

        conn = sqlite3.connect("campus.db")
        cur = conn.cursor()
        cur.execute("SELECT fee FROM courses WHERE name=?", (course,))
        result = cur.fetchone()
        conn.close()

        if result:
            dispatcher.utter_message(text=f"The fee for {course} is {result[0]}")
        else:
            dispatcher.utter_message(text="Sorry, I don’t know that course.")
        return []

class ActionHandoff(Action):
    def name(self) -> str:
        return "action_handoff"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Transferring you to a human agent...")
        return []

