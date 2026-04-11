#!/usr/bin/env python3
"""Regression test: `module_*` tokens should not block subtask validation."""

from pathlib import Path
from tempfile import TemporaryDirectory

from core.etapes import EtapeManager


def test_module_tokens_are_ignored_in_mapping_subtasks() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Constitution").mkdir(parents=True, exist_ok=True)
        (root / "backend" / "src" / "routes").mkdir(parents=True, exist_ok=True)
        (root / "backend" / "src" / "controllers").mkdir(parents=True, exist_ok=True)

        etapes = """## [ ] 12_Backend_API_Modules : API
- [ ] Mapper le module `users` : `backend/src/routes/users.routes.ts` + `backend/src/controllers/users.controller.ts` avec la section frontend `module_users`
"""
        (root / "Constitution" / "etapes.md").write_text(etapes, encoding="utf-8")
        (root / "backend" / "src" / "routes" / "users.routes.ts").write_text("// users", encoding="utf-8")
        (root / "backend" / "src" / "controllers" / "users.controller.ts").write_text("// users", encoding="utf-8")

        manager = EtapeManager(model=None, project_root=str(root))
        ok, checked, total = manager.mark_step_as_completed("12_Backend_API_Modules")

    assert ok is True
    assert total == 1
    assert checked == 1


def test_zustand_module_list_tokens_are_ignored() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Constitution").mkdir(parents=True, exist_ok=True)
        (root / "frontend" / "src" / "store").mkdir(parents=True, exist_ok=True)
        (root / "frontend" / "src" / "store" / "index.ts").write_text("// store", encoding="utf-8")

        etapes = """## [ ] 14_Architecture_Frontend : Frontend
- [ ] Structurer Zustand par module backend (`users`, `medications`, `chat`, `archives`, `patients`, `consultations`, `prescriptions`, `billing`, `doctors`, `alerts`, `chatmessages`, `billings`, `chat_messages`) et preparer les slices/stores relies a `*_API_LAYER`
"""
        (root / "Constitution" / "etapes.md").write_text(etapes, encoding="utf-8")

        manager = EtapeManager(model=None, project_root=str(root))
        ok, checked, total = manager.mark_step_as_completed("14_Architecture_Frontend")

        assert ok is True
        assert total == 1
        assert checked == 1


def test_auth_action_tokens_are_ignored_for_api_layer() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Constitution").mkdir(parents=True, exist_ok=True)
        (root / "frontend" / "src" / "api").mkdir(parents=True, exist_ok=True)
        (root / "frontend" / "src" / "api" / "auth.api.ts").write_text("// auth", encoding="utf-8")

        etapes = """## [ ] 15_API_LAYER : API layer
- [ ] Creer `frontend/src/api/auth.api.ts` pour `login`/`register` avec Axios + JWT
"""
        (root / "Constitution" / "etapes.md").write_text(etapes, encoding="utf-8")

        manager = EtapeManager(model=None, project_root=str(root))
        ok, checked, total = manager.mark_step_as_completed("15_API_LAYER")

        assert ok is True
        assert total == 1
        assert checked == 1


if __name__ == "__main__":
    test_module_tokens_are_ignored_in_mapping_subtasks()
    test_zustand_module_list_tokens_are_ignored()
    test_auth_action_tokens_are_ignored_for_api_layer()
    print("ok")
