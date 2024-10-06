import logging

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from systemLogs.models import SystemLogs
        user_id = getattr(record, 'user_id', None)

        log_entry = SystemLogs(
            level=record.levelname,
            message=record.getMessage(),
            module=record.module,
            user_id=user_id,
        )
        log_entry.save()
