# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Text, List, Any, Dict
import json

#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, EventType
from rasa_sdk.types import DomainDict

from .ej_connector import API

#
#


class ActionSetupConversation(Action):
    def name(self):
        return "action_setup_conversation"

    def run(self, dispatcher, tracker, domain):
        conversation_id = 1
        user_email = tracker.get_slot("email")

        if user_email:
            user = API.create_user(tracker.sender_id, user_email, user_email)
        else:
            user = API.create_user(tracker.sender_id)

        statistics = API.get_user_conversation_statistics(conversation_id, user.token)
        first_comment = API.get_next_comment(conversation_id, user.token)
        return [
            SlotSet("number_voted_comments", statistics["votes"]),
            SlotSet("conversation_id", conversation_id),
            SlotSet(
                "number_comments", statistics["missing_votes"] + statistics["votes"]
            ),
            SlotSet("comment_text", first_comment["content"]),
            SlotSet("current_comment_id", first_comment["id"]),
            SlotSet("change_comment", False),
            SlotSet("ej_user_token", user.token),
            FollowupAction("vote_form"),
        ]


class ActionAskVote(Action):
    def name(self) -> Text:
        return "action_ask_vote"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        buttons = [
            {"title": "Concordar", "payload": "Concordar"},
            {"title": "Discordar", "payload": "Discordar"},
            {"title": "Pular", "payload": "Pular"},
        ]
        conversation_id = tracker.get_slot("conversation_id")
        token = tracker.get_slot("ej_user_token")
        statistics = API.get_user_conversation_statistics(conversation_id, token)
        total_comments = statistics["missing_votes"] + statistics["votes"]
        number_voted_comments = statistics["votes"]

        if tracker.get_slot("change_comment"):
            new_comment = API.get_next_comment(conversation_id, token)
            comment_content = new_comment["content"]
            message = f"{comment_content} \n O que você acha disso ({number_voted_comments}/{total_comments})?"

            dispatcher.utter_message(text=message, buttons=buttons)

            conversation_id = tracker.get_slot("conversation_id")
            token = tracker.get_slot("ej_user_token")
            new_comment = API.get_next_comment(conversation_id, token)
            return [
                SlotSet("number_voted_comments", number_voted_comments),
                SlotSet("comment_text", new_comment["content"]),
                SlotSet("number_comments", total_comments),
                SlotSet("current_comment_id", new_comment["id"]),
            ]
        else:
            comment_content = tracker.get_slot("comment_text")
            message = f"{comment_content} \n O que você acha disso ({number_voted_comments}/{total_comments})?"
            dispatcher.utter_message(text=message, buttons=buttons)
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
        token = tracker.get_slot("ej_user_token")
        conversation_id = tracker.get_slot("conversation_id")
        if str(slot_value) in ["Concordar", "Discordar", "Pular"]:
            comment_id = tracker.get_slot("current_comment_id")
            sent_vote = API.send_comment_vote(comment_id, slot_value, token)

            if sent_vote["created"]:
                dispatcher.utter_message(template="utter_vote_received")
            statistics = API.get_user_conversation_statistics(conversation_id, token)
            if statistics["missing_votes"] > 0:
                # user still has comments to vote, remain in loop
                return {"vote": None}
            else:
                # user voted in all comments, can exit loop
                dispatcher.utter_message(template="utter_voted_all_comments")
                return [{"vote": slot_value}]
        elif str(slot_value) == "PARAR":
            dispatcher.utter_message(template="utter_stopped")
            return {"vote": "None"}
        else:
            # register a new comment instead of a vote
            response = API.send_new_comment(conversation_id, slot_value, token)
            if response["created"]:
                dispatcher.utter_message(template="utter_sent_comment")
            else:
                dispatcher.utter_message(template="utter_send_comment_error")
        return {"vote": None}
