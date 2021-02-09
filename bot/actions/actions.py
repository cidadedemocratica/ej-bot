# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Text, List, Any, Dict

#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, EventType
from rasa_sdk.types import DomainDict

#
#
class ActionSetupConversation(Action):
    def name(self):
        return "action_setup_conversation"

    def run(self, dispatcher, tracker, domain):
        # TODO: get values from EJ server
        conversation_id = 1
        number_comments = 3
        number_voted_comments = 1
        first_comment = "Comment text here"
        comment_id = 53
        return [
            SlotSet("number_voted_comments", number_voted_comments),
            SlotSet("conversation_id", conversation_id),
            SlotSet("number_comments", number_comments),
            SlotSet("comment_text", first_comment),
            SlotSet("current_comment_id", comment_id),
            SlotSet("change_comment", False),
            FollowupAction("vote_form"),
        ]


class ActionAskVote(Action):
    def name(self) -> Text:
        return "action_ask_vote"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        buttons = [
            {"title": "Concordar", "payload": "agree"},
            {"title": "Discordar", "payload": "disagree"},
            {"title": "Pular", "payload": "pass"},
        ]

        if tracker.get_slot("change_comment"):
            # TODO: get values from EJ server
            # next_comment = get_random_comment()
            new_comment = "novo comentário com outro id"
            dispatcher.utter_message(text=new_comment, buttons=buttons)
            number_voted_comments = tracker.get_slot("number_comments") + 1
            comment_id = 22
            return [
                SlotSet("number_voted_comments", number_voted_comments),
                SlotSet("comment_text", new_comment),
                SlotSet("current_comment_id", comment_id),
            ]
        else:
            dispatcher.utter_message(
                text=tracker.get_slot("comment_text"), buttons=buttons
            )
            return [SlotSet("change_comment", True)]


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
        if str(slot_value) in ["agree", "disagree", "pass"]:
            # TODO: Send vote value to EJ server
            voted_comments = tracker.get_slot("number_voted_comments")
            total_comments = tracker.get_slot("number_comments")
            dispatcher.utter_message(template="utter_vote_received")
            # TODO: Get next random comment
            # was_sent = send_vote(vote_value)
            if voted_comments == total_comments:
                # user voted in all comments, can exit loop
                return [{"vote": slot_value}]
            else:
                # user still has comments to vote, remain in loop
                return {"vote": None}
        else:
            dispatcher.utter_message(template="utter_out_of_context")
            # did not send expected vote value
        return {"vote": None}
