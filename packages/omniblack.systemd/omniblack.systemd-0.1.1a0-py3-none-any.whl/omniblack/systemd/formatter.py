from logging import Formatter


vital_logging_levels = {
    'CRITICAL': 1,
    'ERROR': 3,
    'WARNING': 4,
    'INFO': 6,
    'DEBUG': 7,
}

logging_levels = {
    'CRITICAL': 2,
    'ERROR': 3,
    'WARNING': 4,
    'INFO': 6,
    'DEBUG': 7,
}


class SystemdFormatter(Formatter):
    vital = False

    def format(self, record):
        level = record.levelname
        levels = (vital_logging_levels
                  if self.vital
                  else logging_levels)
        syslog_priority = f'<{levels[level]}>'
        record.syslog_priority = syslog_priority
        return super().format(record)
