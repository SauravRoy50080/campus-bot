from typing import Any, Text, Dict, List, Optional

from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from googletrans import Translator, LANGUAGES

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)
class GoogleTranslateComponent(GraphComponent):
    """Custom component to translate user messages to English"""

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, model_storage, resource, execution_context)

    def __init__(
        self,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> None:
        super().__init__(config, model_storage, resource, execution_context)
        self.translator = Translator()
        self._base_language = config.get("base_language", "en")
        self._supported_languages = config.get("supported_languages", ["en", "es", "fr"])

    def process(self, messages: List[Message]) -> List[Message]:
        """Process incoming messages by translating them to base language."""
        for message in messages:
            self._process_message(message)
        return messages

    def _process_message(self, message: Message) -> None:
        """Translate a single message to base language."""
        text = message.get("text")
        
        if not text:
            return
            
        # Detect language
        detected_lang = self._detect_language(text)
        
        # Store detected language in message
        message.set("detected_language", detected_lang)
        
        # If not base language, translate
        if detected_lang != self._base_language:
            translated_text = self._translate(text, detected_lang, self._base_language)
            message.set("original_text", text)
            message.set("text", translated_text)
    
    def _detect_language(self, text: Text) -> Text:
        """Detect the language of the input text."""
        try:
            detected = self.translator.detect(text)
            return detected.lang
        except Exception as e:
            print(f"Error detecting language: {e}")
            return self._base_language
    
    def _translate(self, text: Text, src_lang: Text, target_lang: Text) -> Text:
        """Translate text from source language to target language."""
        try:
            result = self.translator.translate(text, src=src_lang, dest=target_lang)
            return result.text
        except Exception as e:
            print(f"Error translating text: {e}")
            return text
    
    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Process training data by translating examples to base language."""
        self.process(training_data.training_examples)
        return training_data
    
    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
        **kwargs: Any,
    ) -> GraphComponent:
        return cls(config, model_storage, resource, execution_context)
