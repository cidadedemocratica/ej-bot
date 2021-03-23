import pytest
import unittest
import os
from unittest.mock import Mock, patch
from typing import Text, List, Any, Dict

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa.shared.core.domain import Domain
from rasa.shared.core.events import UserUttered
from rasa.shared.core.trackers import DialogueStateTracker, AnySlotDict
from actions import ActionSetupConversation, ActionAskVote, ValidateVoteForm

STATISTICS = {
    "votes": 0,
    "missing_votes": 6,
}


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with patch.dict(os.environ, {"JWT_SECRET": "testing_secret_value"}):
        yield


@pytest.fixture
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def domain():
    return dict()


@pytest.fixture
def tracker():
    return DialogueStateTracker(sender_id="1", slots=AnySlotDict())


def test_action_ask_vote(dispatcher, domain, tracker):
    with patch("actions.ej_connector.api.requests.get") as mock_get:
        statistics_mock = STATISTICS
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = statistics_mock
        action = ActionAskVote()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [SlotSet("change_comment", True)]

        assert events == expected_events
