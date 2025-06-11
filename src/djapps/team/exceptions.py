import strawberry




class ErrorException(Exception):
    def __init__(self, message: str, code: str = "BAD_REQUEST"):
        
        """
        Custom exception class for handling errors in the application.
        Args:
            message (str): The error message to be displayed.
            code (str): The error code, default is "BAD_REQUEST".
        """
        self.code = code
        self.message = message
        super().__init__(message)
        
@strawberry.type
class ErrorByIdResponse:
    ok: bool
    error: ErrorException | None = None
