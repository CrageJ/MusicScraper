from enum import Enum


class Website(str, Enum):
    UNDEF = 'undef'
    AOTY = 'aoty' # album of the year
    RYM = "rym" # rate your music
    BEA = "bea" # best ever albums
    META = "meta" # metacritic
