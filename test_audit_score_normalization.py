#!/usr/bin/env python3
"""Regression tests for audit/checklist score normalization."""

from core.graph import SpecGraphManager


def _make_manager() -> SpecGraphManager:
    return object.__new__(SpecGraphManager)


def test_checklist_score_when_no_subtasks_and_no_missing() -> None:
    manager = _make_manager()
    assert manager._compute_checklist_score(0, 0) == 100


def test_checklist_score_with_missing_subtasks() -> None:
    manager = _make_manager()
    assert manager._compute_checklist_score(5, 1) == 80


def test_approved_status_normalizes_to_100_on_full_checklist() -> None:
    manager = _make_manager()
    assert manager._normalize_audit_score("APPROUVE", 95, 100) == 100
    assert manager._normalize_audit_score("APPROUVE", 0, 100) == 100


def test_rejected_status_keeps_score_value() -> None:
    manager = _make_manager()
    assert manager._normalize_audit_score("REJETE", 95, 100) == 95


if __name__ == "__main__":
    test_checklist_score_when_no_subtasks_and_no_missing()
    test_checklist_score_with_missing_subtasks()
    test_approved_status_normalizes_to_100_on_full_checklist()
    test_rejected_status_keeps_score_value()
    print("ok")
