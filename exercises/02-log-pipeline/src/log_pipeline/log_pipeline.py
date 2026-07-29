
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
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

def main():
    entries = [
        '2025-01-10 14:33:02 WARNING Medium memory usage during the proccess',
        '2025-01-10 14:33:06 ERROR High memory usage during the proccess',
        '2025-01-10 14:34:06 ERROR High memory usage during the proccess',
        '2025-01-10 14:34:02 DEBUG High memory usage during the proccess',
        "2025-01-10 14:35:01 INFO Server started",
        "2025-01-10 14:35:15 ERROR Database connection failed",
        "2025-01-10 14:35:20 ERROR Database connection failed",
        "2025-01-10 14:36:02 WARNING Medium memory usage"
    ]

    pipeline = fileter_by_log_level(parse_log_entry(entries), {LogLevel.DEBUG, LogLevel.ERROR})

#    for log_record in pipeline:
#        print(log_record)

#    for min, group in group_by_minute(pipeline):
#        print(min)
#        for log in group:
#            print(log)

    for min, group in top_k_messages(group_by_minute(pipeline),4):
        print(min, group)





if __name__ == '__main__':    
    main()