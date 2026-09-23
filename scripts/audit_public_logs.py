#!/usr/bin/env python3
"""Inspect four pinned author logs; never execute agents or benchmark actions."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "5353cf7615b135cace8d07c8f12dac53a16b6db3"
BASE = "gpt-4o-2024-08-06"
PIPELINES = (BASE, BASE + "-transformers_pi_detector")
TASKS = ("user_task_0", "user_task_1")
MARKER = "Data omitted because a prompt injection was detected"


def inspect(cache: Path, fetch: bool) -> dict:
    records = []
    for task in TASKS:
        for pipeline in PIPELINES:
            relative = f"runs/{pipeline}/shopping/{task}/none/none.json"
            url = f"https://raw.githubusercontent.com/SaFo-Lab/AgentDyn/{COMMIT}/{relative}"
            path = cache / f"{pipeline}_{task}.json"
            if fetch:
                # Public Contents API avoids requiring GitHub authentication and
                # works where the raw-content host is unreachable.
                api_url = f"https://api.github.com/repos/SaFo-Lab/AgentDyn/contents/{relative}?ref={COMMIT}"
                request = urllib.request.Request(api_url, headers={"User-Agent": "public-research-log-audit"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    payload = response.read(14_000_001)
                if len(payload) > 14_000_000:
                    raise ValueError(f"Unexpectedly large API response for {task} / {pipeline}")
                metadata = json.loads(payload)
                if metadata.get("encoding") != "base64" or not isinstance(metadata.get("content"), str):
                    raise ValueError(f"Unexpected GitHub response for {task} / {pipeline}")
                raw = base64.b64decode(metadata["content"])
                if len(raw) > 10_000_000:
                    raise ValueError(f"Unexpectedly large public log for {task} / {pipeline}")
                # Validate before writing a downloaded response into the cache.
                json.loads(raw)
                cache.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            if not path.is_file():
                raise FileNotFoundError(f"Missing {path.name}; use --fetch to download public logs.")
            raw = path.read_bytes()
            log = json.loads(raw)
            for field in ("messages", "utility", "attack_type", "injection_task_id", "injections", "error"):
                if field not in log:
                    raise ValueError(f"Missing field {field} in {path.name}")
            if (log.get("suite_name"), log.get("user_task_id"), log.get("pipeline_name")) != (
                "shopping", task, pipeline
            ):
                raise ValueError(f"Unexpected identity in {path.name}")
            if not isinstance(log["utility"], bool) or not isinstance(log["messages"], list):
                raise ValueError(f"Unexpected data types in {path.name}")
            marker_messages = sum(
                MARKER in json.dumps(message, ensure_ascii=False) for message in log["messages"]
            )
            records.append({
                "task": task,
                "pipeline": pipeline,
                "source_url": url,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "author_evaluation_timestamp": log.get("evaluation_timestamp"),
                "benchmark_version": log.get("benchmark_version"),
                "agentdojo_package_version": log.get("agentdojo_package_version"),
                "utility": log["utility"],
                "attack_type": log["attack_type"],
                "injection_task_id": log["injection_task_id"],
                "injections_empty": log["injections"] == {},
                "error": log["error"],
                "message_count": len(log["messages"]),
                "messages_containing_filter_marker": marker_messages,
            })
    observations = []
    for task in TASKS:
        baseline = next(r for r in records if r["task"] == task and r["pipeline"] == BASE)
        filtered = next(r for r in records if r["task"] == task and r["pipeline"] != BASE)
        observations.append({
            "task": task,
            "baseline_succeeds_filtered_fails": baseline["utility"] and not filtered["utility"],
            "filtered_trace_has_omission_marker": filtered["messages_containing_filter_marker"] > 0,
            "both_have_no_recorded_attack_or_error": all(
                r["attack_type"] is None and r["injection_task_id"] is None
                and r["injections_empty"] and r["error"] is None
                for r in (baseline, filtered)
            ),
        })
    return {
        "audit_kind": "inspection_of_author_public_logs_not_model_reproduction",
        "source_commit": COMMIT,
        "scope": "Two benign shopping tasks; descriptive paired traces, not controlled causal replay.",
        "records": records,
        "observations": observations,
        "limitations": [
            "No agent model or tool action was executed.",
            "Task failure alone is not proof of a false positive or its causal mechanism.",
            "No attack success rate is inferred from benign runs.",
            "The sample is not an overall defense performance estimate.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Download four public logs at the pinned commit.")
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "data/raw/public-logs")
    parser.add_argument("--output", type=Path, help="Optional path for a compact JSON report.")
    args = parser.parse_args()
    try:
        result = inspect(args.cache_dir.resolve(), args.fetch)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Public-log audit failed: {exc}\n")
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Saved public-log inspection report: {args.output}")
    for item in result["observations"]:
        print(json.dumps(item, ensure_ascii=False))
    if not args.output:
        print(rendered)


if __name__ == "__main__":
    main()
