from enum import Enum


class Tiebreaking(Enum):
    """ASN tiebreaking methods beyond AS Paths"""

    LOWEST_ASN_WINS = "Prefer_Lowest_ASN"
    RANDOM_WINS = "Random"


class TimestampComparison(Enum):
    """Unclear as to what this does"""

    NEWER_WINS = "Prefer_Newer"
    OLDER_WINS = "Prefer_Older"
    DISABLED = "Disabled"
