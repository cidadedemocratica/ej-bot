VOTE_VALUES = ["Concordar", "Discordar", "Pular", "1", "-1", "0"]


def define_vote_utter(metadata, message):
    if "agent" in metadata:
        # channel is livechat, can't render buttons
        message = {"text": message}
    else:
        buttons = [
            {"title": "Concordar", "payload": "Concordar"},
            {"title": "Discordar", "payload": "Discordar"},
            {"title": "Pular", "payload": "Pular"},
        ]
        message = {"text": message, "buttons": buttons}
    return message
