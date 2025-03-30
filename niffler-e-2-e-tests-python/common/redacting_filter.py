import logging


class RedactingFilter(logging.Filter):

    def __init__(self, patterns: list):
        super().__init__()
        self._patterns = patterns

    def filter(self, record):
        record.msg = self.redact(record.msg)
        record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg: str):
        msg = isinstance(msg, str) and msg or str(msg)
        for pattern in self._patterns:
            msg = msg.replace(pattern, "******")
        return msg
