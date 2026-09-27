import enum


class EVENT_TYPE(enum.StrEnum):
    MESSAGE_RECEIVED = "MESSAGE_RECEIVED"


class MESSAGE_IDENTIFIER(enum.StrEnum):
    QUERY = "/QUERY"
    SAVE = "/SAVE"