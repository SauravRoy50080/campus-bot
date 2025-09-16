from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pymongo
from datetime import datetime

class ActionLogToMongo(Action):
    def name(self):
        return "action_log_to_mongo"

    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient("mongodb://mongo:27017/")
        db = client["campus_bot"]
        logs = db["conversations"]

        log_entry = {
            "user_message": tracker.latest_message.get('text'),
            "intent": tracker.latest_message['intent'].get('name'),
            "response": tracker.latest_message['text'],
            "timestamp": datetime.now()
        }
        logs.insert_one(log_entry)
        return []
