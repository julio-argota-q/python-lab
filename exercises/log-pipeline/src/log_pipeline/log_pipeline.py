
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from itertools import groupby

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

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
        if len(parsed_entry) < 4:
            print(f'The log entry has a wrong format:{entry}')
            continue
        try:
            timestamp = datetime.strptime(f'{parsed_entry[0]} {parsed_entry[1]}', DATETIME_FORMAT)
            severity = LogLevel(parsed_entry[2])
            message = parsed_entry[3]
            yield LogRecord(timestamp, severity, message)
        except ValueError as e:
            print(f'Error: {e} produced by log entry:{entry}')


def filter_by_log_level(log_records:Iterable[LogRecord], log_levels:set[LogLevel]) -> Iterator[LogRecord]:
    yield from filter(lambda record: record.log_level in log_levels,  log_records)


def group_by_minute(log_records:Iterable[LogRecord]) -> Iterator[tuple[datetime, Iterator[LogRecord]]]:
    yield from groupby(log_records, key=lambda log_record: log_record.timestamp.replace(second=0, microsecond=0))


def top_k_messages(log_groups:Iterable[tuple[datetime, Iterable[LogRecord]]], k:int = 1) -> Iterator[tuple[datetime, list[tuple[str,int]]]]:
    for timestamp, log_group in log_groups:
        yield (timestamp, Counter( log_record.message for log_record in log_group).most_common(k) )
