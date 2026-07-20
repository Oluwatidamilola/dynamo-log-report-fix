import json
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _non_empty_log_lines():
    return [line.strip() for line in LOG_PATH.read_text().splitlines() if line.strip()]


def _load_report():
    return json.loads(REPORT_PATH.read_text())


def test_success_criterion_1_report_file_exists():
    """Success criterion 1: Create the file /app/report.json."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"


def test_success_criterion_2_report_is_valid_json_object():
    """Success criterion 2: /app/report.json must contain a valid JSON object."""
    data = _load_report()
    assert isinstance(data, dict), "report.json must contain a JSON object"


def test_success_criterion_3_total_requests_is_correct():
    """Success criterion 3: total_requests equals the number of non-empty lines in /app/access.log."""
    data = _load_report()
    expected_total_requests = len(_non_empty_log_lines())
    assert data.get("total_requests") == expected_total_requests


def test_success_criterion_4_unique_ips_is_correct():
    """Success criterion 4: unique_ips equals the number of distinct first whitespace-separated fields."""
    data = _load_report()
    lines = _non_empty_log_lines()
    expected_unique_ips = len({line.split()[0] for line in lines})
    assert data.get("unique_ips") == expected_unique_ips


def test_success_criterion_5_top_path_is_correct():
    """Success criterion 5: top_path equals the most frequent seventh whitespace-separated field."""
    data = _load_report()
    lines = _non_empty_log_lines()
    path_counts = Counter(line.split()[6] for line in lines)
    expected_top_path = path_counts.most_common(1)[0][0]
    assert data.get("top_path") == expected_top_path
