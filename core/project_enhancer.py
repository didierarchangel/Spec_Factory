from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

DEFAULT_STACK = {
    "backend": "express",
    "frontend": "react-vite",
    "database": "mongodb",
    "design": "premium",
    "devops": "docker + github-actions",
}


class ProjectEnhancer:
    """Module Project Enhancer : enrichit la vision de haut niveau du projet."""

    def __init__(self, model: Any = None, project_root: str | Path = "."):
        self.model = model
        self.root = Path(project_root)

    def enhance(
        self,
        description: str,
        stack_preferences: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        stack = {**DEFAULT_STACK}
        if stack_preferences:
            stack.update(stack_preferences)
        stack.update(self._load_spec_stack())

        enriched = {
            "summary": self._summarize_description(description),
            "objective": self._extract_objective(description),
            "stack_recommendations": stack,
            "workflow": self._build_workflow(description),
            "modules": self._suggest_modules(description),
        }

        return enriched

    def _summarize_description(self, text: str) -> str:
        if not text:
            return "Speckit.Factory project requiring premium UI/UX intelligence."
        snippet = text.strip().split("\n")[0]
        return f"Auto-enriched brief: {snippet}"

    def _extract_objective(self, text: str) -> str:
        keywords = ["objectif", "goal", "purpose", "target"]
        lower = text.lower()
        for kw in keywords:
            if kw in lower:
                start = lower.index(kw)
                return text[start : start + 80].strip()
        return "Deliver an actionable Speckit UI/UX Maker pipeline."

    def _build_workflow(self, text: str) -> Iterable[str]:
        steps = [
            "Collect user brief + goals",
            "Auto-suggest stack + architecture",
            "Generate UI Design System + UX flows",
            "Produce Constitution + operational plan",
        ]
        if "dashboard" in text.lower():
            steps.insert(2, "Prioritize analytics dashboards & stats widgets")
        return steps

    def _suggest_modules(self, text: str) -> Iterable[str]:
        base = [
            "Project Enhancer",
            "Component Improver",
            "Pattern Detector",
            "Design System Generator",
            "UX Flow Designer",
            "Constitution Generator",
        ]
        if "image" in text.lower():
            base.append("Vision Pattern Detector (image-aware)")
        return base

    def _load_spec_stack(self) -> Dict[str, str]:
        lock_file = self.root / ".spec-lock.json"
        if not lock_file.exists():
            return {}
        try:
            data = json.loads(lock_file.read_text(encoding="utf-8"))
            return {k: v for k, v in (data.get("stack_preferences") or {}).items() if isinstance(v, str)}
        except Exception:
            return {}
