from enum import Enum


class Tiebreaking(Enum):
    """ASN tiebreaking methods beyond AS Paths"""

    LOWEST_ASN_WINS = "Prefer_Lowest_ASN".lower()
    RANDOM_WINS = "Random".lower()


class TimestampComparison(Enum):
    """Unclear as to what this does"""

    NEWER_WINS = "Prefer_Newer".lower()
    OLDER_WINS = "Prefer_Older".lower()
    DISABLED = "Disabled".lower()
