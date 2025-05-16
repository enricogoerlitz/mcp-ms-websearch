from requests import Response


class GeneralError(Exception):
    """
    Custom ValueError implementation
    """

    def __init__(self, err_msg: str) -> None:
        super().__init__(err_msg)


class GeneralValueError(GeneralError):
    pass


class NotFoundError(GeneralError):
    pass


class DuplicateRecordError(GeneralError):
    pass


class AIClientRateLimitError(Exception):
    def __init__(self, resp: Response):
        err = f"Code: {resp.status_code}, Response: {resp.text}"
        super().__init__(err)


class RequestsException(Exception):
    def __init__(self, resp: Response):
        err = f"Code: {resp.status_code}, Response: {resp.text}"
        super().__init__(err)


class VectorSearchRequestException(RequestsException):
    pass
