# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Text, List, Any, Dict

#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

#
#
class ActionSetupConversation(Action):
    def name(self):
        return "action_setup_conversation"

    def run(self, dispatcher, tracker, domain):
        # TODO: get values from EJ server
        conversation_id = 1
        number_comments = 10
        number_voted_comments = 1
        first_comment = "Comment text here"
        comment_id = 53
        return [
            SlotSet("number_voted_comments", number_voted_comments),
            SlotSet("conversation_id", conversation_id),
            SlotSet("number_comments", number_comments),
            SlotSet("comment_text", first_comment),
            SlotSet("current_comment_id", comment_id),
        ]


class ActionSendVote(Action):
    def name(self):
        return "action_send_vote"

    def run(self, dispatcher, tracker, domain):
        # TODO: Add code to send request to EJ with vote value
        vote = tracker.latest_message["intent"].get("name")
        dispatcher.utter_message(vote)
        voted_comments = tracker.get_slot("number_voted_comments")
        dispatcher.utter_message(template="utter_vote_received")
        return [SlotSet("number_voted_comments", voted_comments + 1)]


class ValidateVoteForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_vote_form"

    def validate_vote(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate vote value."""
        vote_value = dispatcher.utter_message(slot_value)
        if vote_value in ["agree", "disagree", "pass"]:
            # TODO: Send vote value to EJ server
            voted_comments = tracker.get_slot("number_voted_comments") + 1
            total_comments = tracker.get_slot("number_comments")

            # TODO: Get next random comment
            # was_sent = send_vote(vote_value)
            # next_comment = get_random_comment()
            if voted_comments == total_comments:
                # user voted in all comments, can exit loop
                return {"vote": slot_value}

        # user still has comments to vote, remain in loop OR did not send expected vote value
        return {"vote": None}
