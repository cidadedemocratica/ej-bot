from rasa.core.channels import TelegramInput
from typing import Text


class TelegramInputChannel(TelegramInput):
    @classmethod
    def name(cls) -> Text:
        return "telegram"

    def get_metadata(self, request):
        metadata = request.json
        return metadata
