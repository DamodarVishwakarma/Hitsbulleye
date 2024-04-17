"""Global Constants"""

from src.configs.env import get_settings

config = get_settings()

APP_CONTEXT_PATH = "/hitbullseye/api"


class MasterConstants:
    """master constant"""
    DEFAULT_TIME_ZONE = "UTC"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    ADMIN_ROLE_ID = 1
    ADMIN_LIMIT_ROLE_ID = 1
    DEFAULT_USER = "lalit@gmail.com"


class UserConstant:
    """constant for user"""

    class Role:
        """role id constant"""
        VIEWER = 0
        ADMIN = 1


class QuestionConstant:
    """question constanta"""

    class QuestionStyle:
        """question st"""
        SINGLE_SCREEN = 1
        SPLIT_SCREEN = 2

    class NumberOfOptions:
        """constant for number of options"""
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6

    class QuestionType:
        """question type constant"""
        OBJECTIVE = 1
        SUBJECTIVE = 2

    class AnswerType:
        """answer type constant"""
        SINGLE_SELECT = 1
        MULTI_SELECT = 2
        TYPABLE = 3

    class Lod:
        """Lod constant"""
        EASY = 1
        MEDIUM = 2
        HARD = 3
