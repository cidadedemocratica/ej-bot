import pytest
import unittest
from unittest.mock import Mock, patch
import os
import json

from actions.ej_connector import API, User
from actions.ej_connector.api import (
    conversation_url,
    API_URL,
    conversation_random_comment_url,
    user_statistics_url,
    user_comments_route,
    user_pending_comments_route,
    EJCommunicationError,
)

CONVERSATION_ID = "1"
TOKEN = "mock_token_value"
EMAIL = "email@email.com"
SENDER_ID = "mock_rasa_sender_id"


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with patch.dict(os.environ, {"JWT_SECRET": "testing_secret_value"}):
        yield


class APIClassTest(unittest.TestCase):
    """tests actions.ej_connector.api API class"""

    @patch("actions.ej_connector.api.requests.post")
    def test_create_user_in_ej_with_rasa_id(self, mock_post):
        response_value = {"key": "key_value"}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = response_value
        response = API.get_or_create_user(SENDER_ID)
        assert response.token == response_value["key"]

    @patch("actions.ej_connector.api.requests.post")
    def test_create_user_in_ej_with_email(self, mock_post):
        response_value = {"key": "key_value"}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = response_value
        response = API.get_or_create_user(SENDER_ID, EMAIL, EMAIL)
        assert response.token == response_value["key"]

    @patch("actions.ej_connector.api.requests.post")
    def test_create_user_returns_invalid_response(self, mock_post):
        response_value = {"error": "key_value"}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = response_value
        with pytest.raises(EJCommunicationError):
            API.get_or_create_user(SENDER_ID, EMAIL, EMAIL)

    @patch("actions.ej_connector.api.requests.post")
    def test_create_user_returns_forbidden_response(self, mock_post):
        mock_post.return_value = Mock(status=401), "forbidden"
        with pytest.raises(EJCommunicationError):
            API.get_or_create_user(SENDER_ID, EMAIL, EMAIL)

    @patch("actions.ej_connector.api.requests.get")
    def test_get_conversation_title_in_ej(self, mock_get):
        response_value = {
            "title": "This is the conversation title",
            "links": {"self": "http://localhost:8000/api/v1/conversations/1/"},
        }
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response_value
        response = API.get_conversation_title(CONVERSATION_ID)
        assert response == response_value["title"]

    @patch("actions.ej_connector.api.requests.get")
    def test_get_conversation_title_in_ej_invalid_response(self, mock_get):
        response_value = {
            "invalid": "This is not the conversation title text",
        }
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response_value
        with pytest.raises(EJCommunicationError):
            API.get_conversation_title(CONVERSATION_ID)

    @patch("actions.ej_connector.api.requests.get")
    def test_get_conversation_title_in_ej_forbidden_response(self, mock_get):
        mock_get.return_value = Mock(status=401), "forbidden"
        with pytest.raises(EJCommunicationError):
            API.get_conversation_title(CONVERSATION_ID)

    @patch("actions.ej_connector.api.requests.get")
    def test_get_random_comment_in_ej(self, mock_get):
        response_value = {
            "content": "This is the comment text",
            "links": {"self": "http://localhost:8000/api/v1/comments/1/"},
        }
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response_value
        response = API.get_next_comment(CONVERSATION_ID, TOKEN)
        assert response["content"] == response_value["content"]
        assert response["id"] == "1"

    @patch("actions.ej_connector.api.requests.get")
    def test_get_random_comment_in_ej_invalid_response(self, mock_get):
        response_value = {
            "invalid": "This is not the comment text",
        }
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response_value
        with pytest.raises(EJCommunicationError):
            API.get_next_comment(CONVERSATION_ID, TOKEN)

    @patch("actions.ej_connector.api.requests.get")
    def test_get_random_comment_in_ej_forbidden_response(self, mock_get):
        mock_get.return_value = Mock(status=401), "forbidden"
        with pytest.raises(EJCommunicationError):
            API.get_next_comment(CONVERSATION_ID, TOKEN)

    @patch("actions.ej_connector.api.requests.get")
    def test_get_user_conversation_statistics(self, mock_get):
        statistics_mock = {
            "votes": 3,
            "missing_votes": 6,
        }
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = statistics_mock
        response = API.get_user_conversation_statistics(CONVERSATION_ID, TOKEN)

        assert response["votes"] == statistics_mock["votes"]
        assert response["missing_votes"] == statistics_mock["missing_votes"]

    @patch("actions.ej_connector.api.requests.get")
    def test_get_user_conversation_statistics_error_status(self, mock_get):
        mock_get.return_value = Mock(status=404), "not found"
        with pytest.raises(EJCommunicationError):
            API.get_user_conversation_statistics(CONVERSATION_ID, TOKEN)

    @patch("actions.ej_connector.api.requests.post")
    def test_send_user_vote(self, mock_post):
        vote_response_mock = {"created": True}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = vote_response_mock

        response = API.send_comment_vote(CONVERSATION_ID, "Pular", TOKEN)
        assert response["created"]

    @patch("actions.ej_connector.api.requests.post")
    def test_send_user_vote_error_status(self, mock_post):
        mock_post.return_value = Mock(status=401), "forbidden"
        with pytest.raises(EJCommunicationError):
            API.send_comment_vote(CONVERSATION_ID, "Pular", TOKEN)

    @patch("actions.ej_connector.api.requests.post")
    def test_send_user_comment(self, mock_post):
        vote_response_mock = {"created": True, "content": "content"}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = vote_response_mock

        response = API.send_new_comment(CONVERSATION_ID, "content", TOKEN)
        assert response["created"]
        assert response["content"] == "content"

    @patch("actions.ej_connector.api.requests.post")
    def test_send_user_comment_error_status(self, mock_post):
        mock_post.return_value = Mock(status=404), "conversation not found"
        with pytest.raises(EJCommunicationError):
            API.send_new_comment(CONVERSATION_ID, "content", TOKEN)

    @patch("actions.ej_connector.api.requests.get")
    def test_get_webchat_connection_to_conversation(self, mock_get):
        response_value = [
            {
                "conversation": "This is the conversation title",
                "links": {
                    "conversation": "http://localhost:8000/api/v1/conversations/1/"
                },
            }
        ]
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response_value
        response = API.get_conversation_info_by_url(CONVERSATION_ID)
        assert response[0]["conversation"] == response_value[0]["conversation"]
        assert response[0]["links"]["conversation"][-2] == "1"

    @patch("actions.ej_connector.api.requests.get")
    def test_get_webchat_connection_not_existing(self, mock_get):
        response_value = []
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response_value
        response = API.get_conversation_info_by_url(CONVERSATION_ID)
        assert response == []

    @patch("actions.ej_connector.api.requests.get")
    def test_get_webchat_connection_not_existing(self, mock_get):
        mock_get.return_value = Mock(status=404), "conversation not found"
        with pytest.raises(EJCommunicationError):
            API.get_conversation_info_by_url(CONVERSATION_ID)


class UserClassTest(unittest.TestCase):
    """tests actions.ej_connector.user file"""

    def test_user_init_with_rasa(self):
        user = User(SENDER_ID)
        assert "-rasa@mail.com" in user.email
        assert "-rasa" in user.password
        assert "-rasa" in user.password_confirm
        assert user.stats == {}
        assert user.name == ""
        assert user.display_name == ""

    def test_user_init_with_mail(self):
        user = User(SENDER_ID, email=EMAIL)
        assert user.email == EMAIL
        assert user.password == EMAIL
        assert user.password_confirm == EMAIL
        assert user.stats == {}
        assert user.name == ""
        assert user.display_name == ""

    def test_user_serializer_with_rasa(self):
        user = User(SENDER_ID)
        serialized_user = user.serialize()
        assert type(serialized_user) == str
        dict_user = json.loads(serialized_user)
        assert "-rasa@mail.com" in dict_user["email"]

    def test_user_serializer_with_mail(self):
        user = User(SENDER_ID, email=EMAIL)
        serialized_user = user.serialize()
        assert type(serialized_user) == str
        dict_user = json.loads(serialized_user)
        assert dict_user["email"] == EMAIL


class EjUrlsGenerationClassTest(unittest.TestCase):
    """tests actions.ej_connector.api ej urls generation"""

    def test_conversation_url_generator(self):
        url = conversation_url(CONVERSATION_ID)
        assert url == f"{API_URL}/conversations/{CONVERSATION_ID}/"

    def test_conversation_random_comment_url_generator(self):
        url = conversation_random_comment_url(CONVERSATION_ID)
        assert url == f"{API_URL}/conversations/{CONVERSATION_ID}/random-comment/"

    def test_user_statistics_url_generator(self):
        url = user_statistics_url(CONVERSATION_ID)
        assert url == f"{API_URL}/conversations/{CONVERSATION_ID}/user-statistics/"

    def test_user_comments_route_generator(self):
        url = user_comments_route(CONVERSATION_ID)
        assert url == f"{API_URL}/conversations/{CONVERSATION_ID}/user-comments/"

    def test_user_pending_comments_route_generator(self):
        url = user_pending_comments_route(CONVERSATION_ID)
        assert (
            url == f"{API_URL}/conversations/{CONVERSATION_ID}/user-pending-comments/"
        )
