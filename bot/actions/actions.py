# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"
import requests
from typing import Any, Text, Dict, List

#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#
#
class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        post_url = "http://localhost:8000/"

        headers = {"content-type": "application/json"}

        params = {"message": "constante"}

        r = requests.post(post_url, data=json.dumps(params), headers=headers)
        dispatcher.utter_message(text="Hello World!")

        return []
