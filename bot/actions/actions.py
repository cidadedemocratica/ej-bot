# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import requests

#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#
#
class ActionRandomComment(Action):
    def name(self):
        return 'action_random_comment'

    def run(self, dispatcher, tracker, domain):
        # TODO: Add code to get comment from EJ server
        comment = 'Comment text here'
        dispatcher.utter_message(comment)
        dispatcher.utter_message(template="utter_vote")
        return []

class ActionSendVote(Action):
    def name(self):
        return 'action_send_vote'

    def run(self, dispatcher, tracker, domain):
        # TODO: Add code to send request to EJ with vote value
        vote = tracker.latest_message['intent'].get('name')
        dispatcher.utter_message(vote)
        dispatcher.utter_message(template="utter_vote_received")
        return []