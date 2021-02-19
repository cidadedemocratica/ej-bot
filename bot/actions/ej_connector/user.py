import os
import json
import jwt


class User(object):
    def __init__(self, rasa_id, name="", email=""):
        self.name = name
        self.display_name = ""
        self.stats = {}
        if email:
            self.email = email
            self.password = self.email
            self.password_confirm = self.email
        else:
            secret = os.getenv("JWT_SECRET")
            encoded_id = jwt.encode({"rasa_id": rasa_id}, secret, algorithm="HS256")
            self.email = f"{encoded_id}-rasa@mail.com"
            self.password = f"{encoded_id}-rasa"
            self.password_confirm = f"{encoded_id}-rasa"

    def serialize(self):
        return json.dumps(self.__dict__)
