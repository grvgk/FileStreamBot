class HTTPError(Exception):
    def __init__(self, status_code: int, description: str = None):
        self.status_code = status_code
        self.description = description
        super().__init__(f"{status_code}: {description or 'HTTP Error'}")

error_messages = {
    400: "Invalid request.",
    401: "File code is required to download the file.",
    403: "Invalid file code.",
    404: "File not found.",
    405: "Invalid request method.",
    500: "Internal server error."
}

async def invalid_request(_):
    return error_messages[400], 400

async def not_found(_):
    return error_messages[404], 404

async def invalid_method(_):
    return error_messages[405], 405

async def http_error(error: HTTPError):
    description = error.description or error_messages.get(error.status_code, "Unknown error")
    return description, error.status_code

def abort(status_code: int = 500, description: str = None):
    raise HTTPError(status_code, description)
