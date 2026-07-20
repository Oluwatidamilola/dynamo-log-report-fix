import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_report_exists():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"


def test_report_is_valid_json():
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    json.loads(REPORT_PATH.read_text())


def test_report_has_required_keys():
    data = json.loads(REPORT_PATH.read_text())
    for key in ("total_requests", "unique_ips", "top_path"):
        assert key in data, f"missing required key: {key}"


def test_report_values_are_correct():
    data = json.loads(REPORT_PATH.read_text())
    expected = _expected()
    assert data["total_requests"] == expected["total_requests"]
    assert data["unique_ips"] == expected["unique_ips"]
    assert data["top_path"] == expected["top_path"]
