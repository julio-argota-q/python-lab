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
2025-0f-10 14:33:02 WARNING High memory usage during the proccess