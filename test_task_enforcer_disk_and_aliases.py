#!/usr/bin/env python3
"""Regression tests for deterministic TaskEnforcer filesystem/alias handling."""

from pathlib import Path
from tempfile import TemporaryDirectory

from core.graph import SpecGraphManager


def _make_manager(root: Path) -> SpecGraphManager:
    manager = object.__new__(SpecGraphManager)
    manager.root = root
    return manager


def test_task_enforcer_uses_disk_and_aliases() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "backend" / "src" / "routes").mkdir(parents=True, exist_ok=True)
        (root / "backend" / "src" / "controllers").mkdir(parents=True, exist_ok=True)

        # Canonical files on disk (singular + chat)
        (root / "backend" / "src" / "routes" / "billing.routes.ts").write_text("// billing", encoding="utf-8")
        (root / "backend" / "src" / "controllers" / "billing.controller.ts").write_text("// billing", encoding="utf-8")
        (root / "backend" / "src" / "routes" / "chat.routes.ts").write_text("// chat", encoding="utf-8")
        (root / "backend" / "src" / "controllers" / "chat.controller.ts").write_text("// chat", encoding="utf-8")

        # Checklist asks for alternate aliases and full paths.
        checklist = """
        - [ ] Mapper billing: `backend/src/routes/billings.routes.ts` + `backend/src/controllers/billings.controller.ts`
        - [ ] Mapper chat: `backend/src/routes/chat_messages.routes.ts` + `backend/src/controllers/chatmessages.controller.ts`
        """

        state = {
            "subtask_checklist": checklist,
            # stale/empty tree must not force STRUCTURE_KO if disk has files
            "file_tree": "",
        }
        manager = _make_manager(root)
        result = manager.task_enforcer_node(state)  # type: ignore[arg-type]

        assert result["validation_status"] == "STRUCTURE_OK"
        assert result["missing_tasks"] == 0


if __name__ == "__main__":
    test_task_enforcer_uses_disk_and_aliases()
    print("ok")
