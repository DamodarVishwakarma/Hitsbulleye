"""Redis constants"""


class RedisKey:
    """Redis key constant"""
    USER_EMAIL          = "user_#{email}"
    QUESTION_ID         = "question_id_#{id}"


class RedisExp:
    """Redis Exp constant"""
    USER_EMAIL           = 60 * 60 * 24 * 3  # 3 days
    QUESTION_ID          = 60 * 60 * 24 * 30  # 30 days
