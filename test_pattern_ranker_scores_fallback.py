#!/usr/bin/env python3
"""Regression test: PatternRanker should tolerate missing `scores`."""

from core.pattern_ranker import PatternRanker


def test_pattern_ranker_handles_missing_scores() -> None:
    ranker = PatternRanker()
    pattern = {"id": "no-scores"}  # no `scores` key
    score = ranker.score(pattern, constitution_score=0.8)
    assert isinstance(score, float)
    assert score > 0.0


if __name__ == "__main__":
    test_pattern_ranker_handles_missing_scores()
    print("ok")
