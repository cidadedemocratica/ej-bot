from actions.utils import define_vote_utter, VOTE_VALUES


def test_vote_values_list():
    values = ["Concordar", "Discordar", "Pular", "1", "-1", "0"]
    assert values == VOTE_VALUES


def test_define_vote_livechat():
    metadata = {"agent": "livechat"}
    message = "vote message"
    returned_value = define_vote_utter(metadata, message)

    assert not "buttons" in returned_value
    assert "text" in returned_value
    assert message == returned_value["text"]


def test_define_vote_channel_not_livechat():
    metadata = {"other_keys": " notlivechat"}
    message = "vote message"
    returned_value = define_vote_utter(metadata, message)

    assert "buttons" in returned_value
    assert "text" in returned_value
    assert message == returned_value["text"]
