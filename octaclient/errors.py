class OctadeskError(Exception):
    """Base exception for Octadesk client errors."""


class AuthenticationError(OctadeskError):
    pass


class NotFoundError(OctadeskError):
    pass


class RateLimitError(OctadeskError):
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None, *args):
        super().__init__(message, *args)
        self.retry_after = retry_after


class ValidationError(OctadeskError):
    pass


class ServerError(OctadeskError):
    pass


class APIError(OctadeskError):
    def __init__(self, status_code: int, message: str | None = None, body: object | None = None):
        super().__init__(message or f"API returned status {status_code}")
        self.status_code = status_code
        self.body = body
