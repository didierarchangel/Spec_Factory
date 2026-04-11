#!/usr/bin/env python3
"""Regression test: checklist validation for MongoDB modeling subtasks."""

from pathlib import Path
from tempfile import TemporaryDirectory

from core.etapes import EtapeManager


def test_modelisation_subtasks_are_checked_from_real_files() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Constitution").mkdir(parents=True, exist_ok=True)
        (root / "backend" / "src" / "models").mkdir(parents=True, exist_ok=True)

        etapes = """## [ ] 10_Modelisation_Donnees_MongoDB : Modélisation des Données MongoDB
- [ ] Vérifier les modèles existants : `Doctor.model.ts`, `Patient.model.ts`
- [ ] Deriver les modeles depuis `Constitution/CONSTITUTION.md`, `Constitution/MappingComponent.md`, `design/image_meta.json` (`DOMAIN_ADAPTATION.modules`) et `design/constitution_design.yaml`
- [ ] Generer `backend/src/models/Doctor.model.ts` pour le module metier `doctor`
- [ ] Generer `backend/src/models/Patient.model.ts` pour le module metier `patient`
"""
        (root / "Constitution" / "etapes.md").write_text(etapes, encoding="utf-8")

        # Fichiers réellement générés par le pipeline code.
        (root / "backend" / "src" / "models" / "Doctor.model.ts").write_text("// doctor", encoding="utf-8")
        (root / "backend" / "src" / "models" / "Patient.model.ts").write_text("// patient", encoding="utf-8")
        (root / "Constitution" / "CONSTITUTION.md").write_text("# constitution", encoding="utf-8")
        (root / "Constitution" / "MappingComponent.md").write_text("# mapping", encoding="utf-8")
        (root / "design").mkdir(parents=True, exist_ok=True)
        (root / "design" / "image_meta.json").write_text("{}", encoding="utf-8")
        (root / "design" / "constitution_design.yaml").write_text("{}", encoding="utf-8")

        manager = EtapeManager(model=None, project_root=str(root))
        ok, checked, total = manager.mark_step_as_completed("10_Modelisation_Donnees_MongoDB")

        assert ok is True
        assert total == 4
        assert checked == 4

        updated = (root / "Constitution" / "etapes.md").read_text(encoding="utf-8")
        assert "## [x] 10_Modelisation_Donnees_MongoDB" in updated


if __name__ == "__main__":
    test_modelisation_subtasks_are_checked_from_real_files()
    print("ok")
