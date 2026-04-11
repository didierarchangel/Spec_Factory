#!/usr/bin/env python3
"""Regression tests for vibe-design task detection."""

from core.graph import SpecGraphManager


def _make_manager() -> SpecGraphManager:
    # Avoid full initialization (LLM clients, graph build) for pure predicate tests.
    return object.__new__(SpecGraphManager)


def test_modelisation_mongodb_is_not_vibe_design_task() -> None:
    manager = _make_manager()
    task_name = "10_Modelisation_Donnees_MongoDB"
    checklist = """
    - [ ] Deriver les modeles depuis `Constitution/MappingComponent.md` et `design/constitution_design.yaml`
    - [ ] Generer `backend/src/models/Doctor.model.ts`
    - [ ] Generer `backend/src/models/Patient.model.ts`
    - [ ] Creer des modeles Mongoose
    """
    assert manager._is_vibe_design_task(task_name, checklist, "") is False


def test_explicit_vibe_step_is_detected() -> None:
    manager = _make_manager()
    task_name = "00_Vibe_Design_Extraction"
    checklist = """
    - [ ] Analyser `Constitution/MappingComponent.md`
    - [ ] Analyser `design/constitution_design.yaml`
    - [ ] Extraire les tokens dans `design/tokens.yaml`
    """
    assert manager._is_vibe_design_task(task_name, checklist, "") is True
