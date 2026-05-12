import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("payments")

class PaymentError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        logger.error(f"Payment Error: {message}")
