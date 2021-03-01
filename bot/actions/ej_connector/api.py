import os
import requests
import json
from .user import User

HEADERS = {
    "Content-Type": "application/json",
}
VOTE_CHOICES = {"Pular": 0, "Concordar": 1, "Discordar": -1}
HOST = os.getenv("EJ_HOST")
API_URL = f"{HOST}/api/v1"
REGISTRATION_URL = f"{HOST}/rest-auth/registration/"
VOTES_URL = f"{API_URL}/votes/"
COMMENTS_URL = f"{API_URL}/comments/"


def conversation_url(conversation_id):
    return f"{API_URL}/conversations/{conversation_id}/"


def conversation_random_comment_url(conversation_id):
    return f"{conversation_url(conversation_id)}random-comment/"


def user_statistics_url(conversation_id):
    return f"{conversation_url(conversation_id)}user-statistics/"


def user_comments_route(conversation_id):
    return f"{conversation_url(conversation_id)}user-comments/"


def user_pending_comments_route(conversation_id):
    return f"{conversation_url(conversation_id)}user-pending-comments/"


def auth_headers(token):
    headers = HEADERS
    headers["Authorization"] = f"Token {token}"
    return headers


class API:
    def create_user(sender_id, name="Participante anônimo", email=""):
        user = User(sender_id, name, email)
        response = requests.post(
            REGISTRATION_URL,
            data=user.serialize(),
            headers=HEADERS,
        )
        user.token = response.json()["key"]
        return user

    def get_next_comment(conversation_id, token):
        url = conversation_random_comment_url(conversation_id)
        response = requests.get(url, headers=auth_headers(token))
        comment = response.json()
        comment_url_as_list = comment["links"]["self"].split("/")
        comment["id"] = comment_url_as_list[len(comment_url_as_list) - 2]
        return comment

    def get_user_conversation_statistics(conversation_id, token):
        url = user_statistics_url(conversation_id)
        response = requests.get(url, headers=auth_headers(token))
        return response.json()

    def send_comment_vote(comment_id, choice, token):
        body = json.dumps(
            {
                "comment": comment_id,
                "choice": VOTE_CHOICES[choice],
            }
        )
        response = requests.post(
            VOTES_URL,
            data=body,
            headers=auth_headers(token),
        )
        return response.json()

    def send_new_comment(conversation_id, content, token):
        body = json.dumps(
            {"content": content, "conversation": conversation_id, "status": "pending"}
        )
        response = requests.post(
            COMMENTS_URL,
            data=body,
            headers=auth_headers(token),
        )
        return response.json()
