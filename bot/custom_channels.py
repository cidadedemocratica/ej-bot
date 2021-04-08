from typing import Text
from rasa.core.channels import RocketChatInput


class RocketChatInputChannel(RocketChatInput):
    @classmethod
    def name(cls) -> Text:
        return "rocketchat"

    def get_metadata(self, request):
        metadata = request.json
        return metadata
