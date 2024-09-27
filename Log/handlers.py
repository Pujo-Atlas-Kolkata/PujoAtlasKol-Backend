import logging

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from Log.models import Log
        user_id = getattr(record, 'user_id', None)

        log_entry = Log(
            level=record.levelname,
            message=record.getMessage(),
            module=record.module,
            user_id=user_id,
        )
        log_entry.save()
