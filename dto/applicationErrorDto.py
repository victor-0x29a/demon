class ApplicationError:
    def __init__(self, reason, http_status_code=422):
        self.reason = reason
        self.http_status_code = http_status_code
