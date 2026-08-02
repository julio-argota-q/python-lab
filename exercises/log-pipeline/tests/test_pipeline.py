from collections import Counter
from collections.abc import Iterable
from datetime import datetime

from log_pipeline import (
    LogLevel,
    filter_by_log_level,
    group_by_minute,
    parse_log_entry,
    top_k_messages,
)


def get_log_entries() -> Iterable[str]:
    return [
        '2025-01-10 14:32:01 INFO Server started',
        '2025-01-10 14:32:15 ERROR Database connection failed',
        '2025-01-10 14:32:20 ERROR Database connection failed',
        '2025-01-10 14:33:02 WARNING High memory usage',
        '2025-01-10 14:34:01 INFO Server started',
        '2025-01-10 14:35:15 ERROR Database connection failed',
        '2025-01-10 14:35:17 WRNING High memory usage',
        '2025-01-10 14:35:20 ERROR Database connection failed',
        '2025-01-10 14:35:20 Database connection failed',
        '2025-01-10 14:35:22 WARNING High memory usage',
        '2025-01-10 14:36:02 WARNING High memory usage'
    ]


def test_parse_log_entry() -> None:
    log_entries = get_log_entries()
    log_records = list(parse_log_entry(log_entries))
    assert 9 == len(log_records)
    assert log_records[0].message == 'Server started'
    assert log_records[2].log_level == LogLevel.ERROR
    
    log_timestamp = datetime(2025,1,10,14,35,15)
    assert log_records[5].timestamp == log_timestamp

    counter = Counter( log_record.log_level for log_record in log_records )
    assert counter == {LogLevel.WARNING:3, LogLevel.ERROR:4, LogLevel.INFO:2}


def test_fileter_by_level() -> None:
    log_entries = get_log_entries()
    log_records = filter_by_log_level(parse_log_entry(log_entries),{LogLevel.WARNING, LogLevel.INFO})
    counter = Counter(log_record.log_level for log_record in log_records)
    assert counter == {LogLevel.WARNING:3, LogLevel.INFO:2}


def test_group_by_minute() -> None:
    log_entries = get_log_entries()
    grouped_log_records = group_by_minute(parse_log_entry(log_entries))
    groups = [(timestamp, list(group)) for timestamp, group in grouped_log_records]

    assert 5 == len(groups)

    assert datetime(2025,1,10,14,32,0) == groups[0][0]
    assert datetime(2025,1,10,14,33,0) == groups[1][0]
    assert datetime(2025,1,10,14,34,0) == groups[2][0]
    assert datetime(2025,1,10,14,35,0) == groups[3][0]
    assert datetime(2025,1,10,14,36,0) == groups[4][0]

    assert 3 == len(groups[0][1])
    assert 1 == len(groups[1][1])
    assert 1 == len(groups[2][1])
    assert 3 == len(groups[3][1])
    assert 1 == len(groups[4][1])

def test_top_k_messages():
    log_entries = get_log_entries()
    grouped_log_records = group_by_minute(parse_log_entry(log_entries))
    top_messages = list(top_k_messages(grouped_log_records, 2))

    assert 5 == len(top_messages)

    assert [('Database connection failed',2), ('Server started',1)] == top_messages[0][1]
    assert [('Database connection failed',2), ('High memory usage',1)] == top_messages[3][1]
    assert [('High memory usage',1)] == top_messages[4][1]
