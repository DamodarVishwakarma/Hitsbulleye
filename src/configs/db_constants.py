"""Database constants module"""


class DBTables:
    """Database tables class"""
    USER_AUTH                       = "user_auth"
    QUESTION                        = "question"
    AREA                            = "area"
    COURSE                          = "course"
    AREA_DIRECTION                  = "area_direction"
    QUESTION_COMMENT                = "question_comment"
    TEST_SECTION                    = "test_section"
    TEST_DIRECTION                  = "test_direction"
    TEST_EXPLANATION                = "test_explanation"
    QUESTION_LOG                    = "question_logs"

class DBConfig:
    """Database configuration class"""
    SCHEMA_NAME = "hitsbulleye"
    BASE_ARGS = {"schema": SCHEMA_NAME}
