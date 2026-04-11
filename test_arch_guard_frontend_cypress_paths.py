#!/usr/bin/env python3
"""Regression test: frontend ArchitectureGuard accepts Cypress artifacts."""

from utils.architecture_guard import ArchitectureGuard


def test_frontend_accepts_cypress_paths() -> None:
    guard = ArchitectureGuard()
    paths = [
        "frontend/cypress/e2e/login.cy.ts",
        "frontend/cypress/e2e/crud.cy.ts",
        "frontend/cypress/support/e2e.ts",
        "frontend/cypress/fixtures/user.json",
        "frontend/cypress.config.ts",
    ]
    validated = guard.validate("frontend", paths)
    assert validated == paths


if __name__ == "__main__":
    test_frontend_accepts_cypress_paths()
    print("ok")
