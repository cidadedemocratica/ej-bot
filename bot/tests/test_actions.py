import pytest

from typing import Text, List, Any, Dict

from actions import ActionSetupConversation, ActionAskVote
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa.shared.core.trackers import DialogueStateTracker, AnySlotDict


EMPTY_TRACKER = None


@pytest.fixture
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def domain():
    return dict()


def test_action_setup_conversation(dispatcher, domain):
    tracker = EMPTY_TRACKER
    action = ActionSetupConversation()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("number_voted_comments", 1),
        SlotSet("conversation_id", 1),
        SlotSet("number_comments", 2),
        SlotSet("comment_text", "Comment text here"),
        SlotSet("current_comment_id", 53),
        SlotSet("change_comment", False),
        FollowupAction("vote_form"),
    ]
    assert events == expected_events


def test_action_ask_vote(dispatcher, domain):
    tracker = DialogueStateTracker(sender_id="1", slots=AnySlotDict())
    action = ActionAskVote()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [SlotSet("change_comment", True)]

    assert events == expected_events
