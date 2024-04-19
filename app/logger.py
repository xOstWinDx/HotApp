import datetime
from datetime import datetime as dt
import logging
from pythonjsonlogger import jsonlogger
from app.config import settings

logging.basicConfig(encoding='utf-8')
logger = logging.getLogger()
logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = dt.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


formatter = CustomJsonFormatter(U'%(timestamp)s %(level)s %(name)s %(message)s', json_ensure_ascii=False)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)

