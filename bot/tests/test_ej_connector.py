import pytest
import unittest
from unittest.mock import Mock, patch
import json

from actions.ej_connector import API, User
from actions.ej_connector.api import (
    conversation_url,
    API_URL,
    conversation_random_comment_url,
    user_statistics_url,
    user_comments_route,
    user_pending_comments_route,
)

CONVERSATION_ID = 1
TOKEN = "mock_token_value"
EMAIL = "email@email.com"
SENDER_ID = "mock_rasa_sender_id"


class APIClassTest(unittest.TestCase):
    """tests actions.ej_connector.api API class"""

    @patch("actions.ej_connector.api.requests.post")
    def test_create_user_in_ej_with_rasa_id(self, mock_post):
        response_value = {"key": "key_value"}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = response_value
        response = API.create_user(SENDER_ID)
        assert response.token == response_value["key"]

    @patch("actions.ej_connector.api.requests.post")
    def test_create_user_in_ej_with_email(self, mock_post):
        response_value = {"key": "key_value"}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = response_value
        response = API.create_user(SENDER_ID, EMAIL, EMAIL)
        assert response.token == response_value["key"]

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
        return f"{API_URL}/conversations/{CONVERSATION_ID}/user-comments/"

    def test_user_pending_comments_route_generator(self):
        url = user_pending_comments_route(CONVERSATION_ID)
        return f"{API_URL}/conversations/{CONVERSATION_ID}/user-pending-comments/"
