import logging
import requests

class CustomHTTPHandler(logging.Handler):
    # Initialize the handler with the host, url, and method
    def __init__(self, host, url, method="POST"):
        super().__init__()
        self.host = host
        self.url = url
        self.method = method

    # Emit the log record to the specified HTTP endpoint
    def emit(self, record):
        try:
            # Format the log record
            log_entry = self.format(record)

            # Prepare the HTTP request
            headers = {'Content-Type': 'application/json'}
            url = f"http://{self.host}{self.url}"

            # POST request to the logging endpoint
            response = requests.post(url, data=log_entry, headers=headers)
            response.raise_for_status()
        except Exception as e:
            self.handleError(record)