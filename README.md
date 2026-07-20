# Dynamo - Fixed Terminal-Bench Task: log-report

Fixes applied to the originally broken task:

1. **`artifacts` schema violation** - was a bare string, Harbor's `TaskConfig` requires `list[str]`. Fixed to `["/app/report.json"]`.
2. **Unpinned base image** - `FROM python:latest` replaced with digest-pinned `python:3.12-slim@sha256:57cd7c3a...`.
3. **Leaked solution** - `environment/solution_hint.py` (a copy of the reference solution) was baked into the agent's image via a Dockerfile `COPY`. Removed both the file and the line.
4. **Dishonest verifier** - original `tests/test_outputs.py` only checked that `report.json` existed and was non-empty, so a no-op agent could trivially pass. Rewritten to independently recompute `total_requests`, `unique_ips`, and `top_path` from `access.log` and assert exact equality against the agent's output.
5. **Wrong verifier output paths** - `tests/test.sh` wrote `reward.txt` to `/app/` and never produced a CTRF report. Fixed to write `/logs/verifier/reward.txt` and `/logs/verifier/ctrf.json` via `pytest --ctrf`.
6. **`instruction.md` lacked success criteria** - rewritten with numbered steps consistent with what the verifier actually checks.

## Verification

```
harbor run -p log-report -a oracle --force-build   # Reward: 1.0
harbor run -p log-report --agent nop                # Reward: 0.0
```
