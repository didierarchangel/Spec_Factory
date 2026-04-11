#!/usr/bin/env python3
"""Regression test: avoid literal placeholder command `npm_path run build`."""

from pathlib import Path


def test_no_literal_npm_path_build_command_in_graph() -> None:
    graph_path = Path(__file__).parent / "core" / "graph.py"
    content = graph_path.read_text(encoding="utf-8")
    assert "npm_path run build" not in content


if __name__ == "__main__":
    test_no_literal_npm_path_build_command_in_graph()
    print("ok")
