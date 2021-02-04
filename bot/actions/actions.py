# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import requests

#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

#
#
class ActionSetConversationId(Action):
    def name(self):
        return 'action_set_conversation_id'

    def run(self, dispatcher, tracker, domain):
        # TODO: get values from EJ server
        conversation_id = 1
        number_comments = 10
        number_voted_comments = 1
        SlotSet("conversation_id", conversation_id)
        SlotSet("number_comments", number_comments)
        SlotSet("number_voted_comments", number_voted_comments)

class ActionRandomComment(Action):
    def name(self):
        return 'action_random_comment'

    def run(self, dispatcher, tracker, domain):
        # TODO: Add code to get comment from EJ server
        # current_conversation = tracker.get_slot("conversation_id")
        comment = 'Comment text here'
        comment_id = 53
        SlotSet("current_comment_id", comment_id)
        SlotSet("loop_comment", True)
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
        voted_comments = tracker.get_slot("number_voted_comments")
        SlotSet("number_voted_comments", voted_comments + 1 )
        dispatcher.utter_message(template="utter_vote_received")
        return []

class ValidateVoteForm(FormValidationAction):
    def name(self):
        return "validate_vote_form"

    def validate_vote(self, slot_value, dispatcher, tracker, domain):
        """Validate vote value."""
        dispatcher.utter_message(slot_value)
        if False:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"vote": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"vote": None}