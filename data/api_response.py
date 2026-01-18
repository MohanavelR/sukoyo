class ApiResponse:
    def __init__(self, success: bool, data=None, error: str = None, message: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.message = message

    @staticmethod
    def success_response(data, message="Success"):
        return ApiResponse(True, data=data, message=message)

    @staticmethod
    def error_response(error_message):
        return ApiResponse(False, error=error_message)
