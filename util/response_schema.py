def response_schema(isSuccess: bool, message: str, data: dict = None):
    return {
        "success": isSuccess,
        "message": message,
        "data": data
    }

def success_response(message: str, data: dict = None):
    return response_schema(True, message, data)

def error_response(message: str, data: dict = None):
    return response_schema(False, message, data)