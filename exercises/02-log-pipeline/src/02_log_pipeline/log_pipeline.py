
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from collections.abc import Iterator, Iterable
from collections import Counter
from itertools import groupby

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    log_level: LogLevel
    message: str


def parse_log_entry(log_entries:Iterable[str]) -> Iterator[LogRecord]:
    for entry in log_entries:
        parsed_entry = entry.split(maxsplit=3)
        try:
            timestamp = datetime.strptime(f'{parsed_entry[0]} {parsed_entry[1]}', DATETIME_FORMAT)
            severity = LogLevel(parsed_entry[2])
            message = parsed_entry[3]
            yield LogRecord(timestamp, severity, message)
        except ValueError as e:
            print(f'Error: {e} produced by log entry:{entry}')


def fileter_by_log_level(log_records:Iterable[LogRecord], log_levels:set[LogLevel]) -> Iterator[LogRecord]:
    for log_record in log_records:
        if log_record.log_level in log_levels:
            yield log_record


def group_by_minute(log_records:Iterable[LogRecord]) -> Iterator[tuple[datetime, Iterator[LogRecord]]]:
    for min, log_group in groupby(log_records, key=lambda log_record: log_record.timestamp.replace(second=0, microsecond=0)):
        yield (min, log_group)


def top_k_messages(log_groups:Iterable[tuple[datetime, Iterable]], n:int) -> Iterator[tuple[datetime, dict[str,int]]]:
    for timestamp, log_group in log_groups:
        yield (timestamp, Counter( log_record.message for log_record in log_group) )
