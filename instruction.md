There is an access log at `/app/access.log`. Parse it and produce a JSON summary report.

## Task
1. Read every line of `/app/access.log`.
2. Compute:
   - `total_requests`: total number of log lines.
   - `unique_ips`: number of distinct client IPs (first field of each line).
   - `top_path`: the most frequently requested path.
3. Write the result to `/app/report.json` as:
   `{"total_requests": <int>, "unique_ips": <int>, "top_path": "<string>"}`

## Success criteria
1. `/app/report.json` exists and is valid, non-empty JSON.
2. It contains the keys `total_requests`, `unique_ips`, `top_path`.
3. All three values exactly match values computed independently from `/app/access.log`.
