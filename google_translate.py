from rasa.nlu.components import Component
from googletrans import Translator

class GoogleTranslateComponent(Component):
    name = "google_translate"
    provides = ["translated_text"]

    def __init__(self, component_config=None):
        super().__init__(component_config)
        self.translator = Translator()

    def process(self, message, **kwargs):
        text = message.get("text")
        if text:
            translated = self.translator.translate(text, dest="en")
            message.set("text", translated.text)
