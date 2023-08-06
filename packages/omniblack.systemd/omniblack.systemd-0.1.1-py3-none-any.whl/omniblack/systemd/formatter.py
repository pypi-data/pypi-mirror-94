from logging import Formatter
from public import public


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


@public
class SystemdFormatter(Formatter):
    """
        A logging formatter that prepends the syslog priority.
            This can be used when running as a new style daemon.

        Attributes:
            vital: Is the program vital to the system.
                Increases the priorities.
    """
    vital = False

    def format(self, record):
        level = record.levelname
        levels = (vital_logging_levels
                  if self.vital
                  else logging_levels)
        syslog_priority = f'<{levels[level]}>'
        record.syslog_priority = syslog_priority
        return super().format(record)
