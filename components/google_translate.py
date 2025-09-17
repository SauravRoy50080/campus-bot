# components/google_translate.py

from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from googletrans import Translator

class GoogleTranslateComponent(Component):
    """Custom component to translate user messages to English"""

    name = "GoogleTranslateComponent"
    provides = ["translated_text"]

    def __init__(self, component_config=None):
        super(GoogleTranslateComponent, self).__init__(component_config)
        self.translator = Translator()

    def train(self, training_data, cfg, **kwargs):
        """No training required for translation."""
        pass

    def process(self, message, **kwargs):
        text = message.get("text")
        if text:
            translated = self.translator.translate(text, dest="en").text
            message.set("translated_text", translated, add_to_output=True)

    def persist(self, file_name, model_dir):
        """No persistence needed."""
        pass
