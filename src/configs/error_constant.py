"""Error Messages Constants"""


class ErrorMessage:
    """Error Messages"""

    MISSING_REQ_FIELD = "Missing required field!"
    RECORD_NOT_FOUND = "Record not found!"
    RECORD_ALREADY_EXISTS = "{} already exists!"
    INVALID_ID = "Invalid {} ID!"
    INVALID_ACTION = "Invalid action!"
    AUTH_HEADER_ERROR = "Authorization Token Missing!"
    UNAUTHORIZED_USER = "Unauthorized User"
    USER_ONBOARDING_ERROR = "Authentication failed, Please connect to admin for onBoarding"
    CUSTOM_MESSAGE = "{}"
    UNAUTHORIZED_REQUEST = "Unauthorized request!"
