import pytest
import unittest
from unittest.mock import Mock, patch
from typing import Text, List, Any, Dict

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa.shared.core.trackers import DialogueStateTracker, AnySlotDict
from actions import ActionSetupConversation, ActionAskVote


@pytest.fixture
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def domain():
    return dict()


@pytest.fixture
def tracker():
    return DialogueStateTracker(sender_id="1", slots=AnySlotDict())


@patch("actions.ej_connector.api.requests.get")
@patch("actions.ej_connector.api.requests.post")
def test_action_setup_conversation(dispatcher, domain, tracker):
    with patch("actions.ej_connector.api.requests.get") as mock_get:
        with patch("actions.ej_connector.api.requests.post") as mock_post:
            user_response = {"key": "key_value"}
            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = user_response

            comment_response = {
                "content": "This is the comment text",
                "links": {"self": "http://localhost:8000/api/v1/comments/1/"},
            }
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = comment_response

            action = ActionSetupConversation()
            events = action.run(dispatcher, tracker, domain)
            expected_events = [
                SlotSet("number_voted_comments", 1),
                SlotSet("conversation_id", 1),
                SlotSet("number_comments", 2),
                SlotSet("comment_text", comment_response["content"]),
                SlotSet("current_comment_id", "1"),
                SlotSet("change_comment", False),
                SlotSet("ej_user_token", user_response["key"]),
                FollowupAction("vote_form"),
            ]
            assert events == expected_events


def test_action_ask_vote(dispatcher, domain, tracker):
    action = ActionAskVote()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [SlotSet("change_comment", True)]

    assert events == expected_events
