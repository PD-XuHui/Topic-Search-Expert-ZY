#!/usr/bin/env python3
"""Deterministically rank vibe-topic-radar candidates from model-assigned scores."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


POSITIVE_WEIGHTS = {
    "account_fit": 0.20,
    "audience_demand": 0.20,
    "evidence_strength": 0.15,
    "pain_specificity": 0.10,
    "execution_value": 0.10,
    "click_potential": 0.10,
    "save_share": 0.10,
    "series_value": 0.05,
}

PENALTY_POINTS = {
    "overlap_penalty": 1.2,
    "saturation_penalty": 0.8,
    "risk_penalty": 1.0,
}


def bounded_score(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a number from 0 to 10") from exc
    if not 0 <= number <= 10:
        raise ValueError(f"{field} must be between 0 and 10, got {number}")
    return number


def rank_topic(topic: dict[str, Any]) -> dict[str, Any]:
    scores = topic.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("each topic must contain a scores object")

    base = 0.0
    for field, weight in POSITIVE_WEIGHTS.items():
        base += bounded_score(scores.get(field), field) * weight * 10

    penalty = 0.0
    for field, points_per_unit in PENALTY_POINTS.items():
        penalty += bounded_score(scores.get(field, 0), field) * points_per_unit

    final = round(max(0.0, min(100.0, base - penalty)), 1)
    evidence = bounded_score(scores.get("evidence_strength"), "evidence_strength")

    if final >= 80:
        tier = "S"
    elif final >= 70:
        tier = "A"
    elif final >= 60:
        tier = "B"
    else:
        tier = "C"

    if evidence >= 8:
        confidence = "high"
    elif evidence >= 5:
        confidence = "medium"
    else:
        confidence = "low"

    result = dict(topic)
    result["score"] = final
    result["tier"] = tier
    result["confidence"] = confidence
    return result


def load_topics(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    topics = payload.get("topics") if isinstance(payload, dict) else payload
    if not isinstance(topics, list) or not topics:
        raise ValueError("input must be a non-empty list or an object with a topics list")
    if not all(isinstance(item, dict) for item in topics):
        raise ValueError("every topic must be a JSON object")
    return topics


def self_test() -> None:
    sample = {
        "title": "第一次见客户，男生提前检查这5处",
        "scores": {
            "account_fit": 9,
            "audience_demand": 8,
            "evidence_strength": 7,
            "pain_specificity": 9,
            "execution_value": 9,
            "click_potential": 8,
            "save_share": 8,
            "series_value": 8,
            "overlap_penalty": 1,
            "saturation_penalty": 2,
            "risk_penalty": 0,
        },
    }
    result = rank_topic(sample)
    assert result["tier"] in {"S", "A", "B", "C"}
    assert 0 <= result["score"] <= 100
    assert result["confidence"] == "medium"
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank Xiaohongshu topic candidates for vibe-topic-radar."
    )
    parser.add_argument("input", nargs="?", type=Path, help="JSON candidate file")
    parser.add_argument("-o", "--output", type=Path, help="write ranked JSON here")
    parser.add_argument("--self-test", action="store_true", help="run a built-in test")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if args.input is None:
        parser.error("input is required unless --self-test is used")

    try:
        ranked = sorted(
            (rank_topic(topic) for topic in load_topics(args.input)),
            key=lambda item: item["score"],
            reverse=True,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    output = json.dumps({"topics": ranked}, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
