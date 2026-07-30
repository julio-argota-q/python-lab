Exercise 2 — Log Processing Pipeline

Goal: Build a reusable library for processing application log files.

Core components: - LogRecord dataclass - parse_lines() -
filter_by_level() - group_by_minute() - top_k_messages()

Requirements: - Parse timestamped log entries. - Skip or report
malformed lines. - Filter by log level. - Group records by minute. -
Count most frequent messages. - Use iterators where appropriate. -
Produce clear exceptions for invalid timestamps.

Suggested tests: - Valid parsing. - Malformed lines. - Invalid dates. -
Filtering. - Grouping. - Top-K frequency.


logentry example 
    log_entries = [
        '2025-01-10 14:32:01 INFO Server started',
        '2025-01-10 14:32:15 ERROR Database connection failed',
        '2025-01-10 14:32:20 ERROR Database connection failed',
        '2025-01-10 14:33:02 WARNING High memory usage',
        '2025-01-10 14:34:01 INFO Server started',
        '2025-01-10 14:35:15 ERROR Database connection failed',
        '2025-01-10 14:35:17 WARNING High memory usage',
        '2025-01-10 14:35:20 ERROR Database connection failed',
        '2025-01-10 14:35:22 WARNING High memory usage',
        '2025-01-10 14:36:02 WARNING High memory usage'
    ]