"""Offline structure checker for the IT0123 Module 4 request plan.

This script does not call the API or the internet. It verifies that the
student's JSON plan contains the required endpoint design and AI-use record.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED = {
    "R1": ("GET", "/api/v1/books", "none", 200),
    "R2": ("GET", "/api/v1/books", "none", 200),
    "R3": ("POST", "/api/v1/loginViaBasic", "basic-auth", 200),
    "R4": ("POST", "/api/v1/books", "x-api-key", 200),
    "R5": ("GET", "/api/v1/books/{id}", "none", 200),
    "R6": ("DELETE", "/api/v1/books/{id}", "x-api-key", 200),
    "R7": ("POST", "/api/v1/books", "missing-or-invalid-key", 401),
}


def normalized(value: object) -> str:
    return str(value).strip().lower()


def contains_sensitive_key(value: object) -> bool:
    forbidden = {"password", "token", "secret", "credential", "api_key_value"}
    if isinstance(value, dict):
        return any(normalized(key) in forbidden or contains_sensitive_key(item)
                   for key, item in value.items())
    if isinstance(value, list):
        return any(contains_sensitive_key(item) for item in value)
    return False


def main() -> int:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "request_plan.json")
    checks: list[tuple[str, bool]] = []
    try:
        plan = json.loads(source.read_text(encoding="utf-8"))
        checks.append(("JSON file loads", True))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL  JSON file loads: {exc}")
        return 1

    checks.append(("Student and AI-tool disclosure completed",
                   bool(str(plan.get("student_name", "")).strip()) and
                   bool(str(plan.get("ai_tool", "")).strip())))
    checks.append(("Credentials are declared redacted",
                   plan.get("credentials_redacted") is True))

    requests = {item.get("id"): item for item in plan.get("requests", [])
                if isinstance(item, dict)}
    checks.append(("All seven request scenarios are present",
                   set(EXPECTED).issubset(requests)))

    designs_ok = True
    status_ok = True
    decisions_ok = True
    evidence_ok = True
    for request_id, (method, path, auth, status) in EXPECTED.items():
        item = requests.get(request_id, {})
        designs_ok &= (
            normalized(item.get("method")) == normalized(method)
            and normalized(item.get("path")) == normalized(path)
            and normalized(item.get("authentication")) == normalized(auth)
        )
        status_ok &= item.get("expected_status") == status
        decisions_ok &= normalized(item.get("ai_decision")) in {
            "accepted", "modified", "rejected"
        }
        evidence_ok &= bool(str(item.get("validation_evidence", "")).strip())

    checks.append(("Methods, paths, and authentication labels are correct",
                   bool(designs_ok)))
    checks.append(("Expected status codes are correct", bool(status_ok)))

    r2_params = requests.get("R2", {}).get("query_parameters", {})
    checks.append(("R2 includes includeISBN=true and sortBy=author",
                   str(r2_params.get("includeISBN", "")).lower() == "true"
                   and normalized(r2_params.get("sortBy")) == "author"))

    r4 = requests.get("R4", {})
    r4_headers = {normalized(k): normalized(v)
                  for k, v in r4.get("headers", {}).items()}
    r4_payload = r4.get("payload", {})
    checks.append(("R4 declares JSON and includes book fields",
                   r4_headers.get("content-type") == "application/json"
                   and isinstance(r4_payload, dict)
                   and {"id", "title", "author"}.issubset(r4_payload)))

    checks.append(("Every scenario records an AI decision", bool(decisions_ok)))
    checks.append(("Every scenario records validation evidence", bool(evidence_ok)))
    checks.append(("No sensitive-value field names are stored",
                   not contains_sensitive_key(plan)))

    for label, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}  {label}")
    passed_count = sum(passed for _, passed in checks)
    print(f"\nResult: {passed_count}/{len(checks)} checks passed")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
