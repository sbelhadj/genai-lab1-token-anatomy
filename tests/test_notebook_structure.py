"""
Auto-grading tests for Lab 1 — Notebook Structure

Verifies that the student's notebook contains the expected sections
and that key cells have been filled in (not still TODO).
"""

import pytest
import json
import os

NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__), "..", "lab1_token_anatomy.ipynb"
)


def load_notebook():
    """Load and parse the notebook file."""
    if not os.path.exists(NOTEBOOK_PATH):
        pytest.skip(f"Notebook not found at {NOTEBOOK_PATH}")
    with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_source(nb):
    """Extract all cell source as a single string."""
    parts = []
    for cell in nb.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            parts.append("".join(source))
        else:
            parts.append(source)
    return "\n".join(parts)


def count_code_cells_with_output(nb):
    """Count code cells that have been executed (have outputs)."""
    count = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            outputs = cell.get("outputs", [])
            if outputs:
                count += 1
    return count


class TestNotebookExists:

    def test_notebook_file_exists(self):
        """The notebook file must exist."""
        assert os.path.exists(NOTEBOOK_PATH), (
            f"Notebook not found at {NOTEBOOK_PATH}. "
            "Make sure you haven't renamed or moved it."
        )

    def test_notebook_valid_json(self):
        """The notebook must be valid JSON."""
        nb = load_notebook()
        assert "cells" in nb, "Notebook is missing 'cells' key"
        assert len(nb["cells"]) > 0, "Notebook has no cells"


class TestNotebookContent:

    def test_has_minimum_cells(self):
        """Notebook should have a reasonable number of cells (indicating work was done)."""
        nb = load_notebook()
        assert len(nb["cells"]) >= 15, (
            f"Notebook has only {len(nb['cells'])} cells. "
            "Expected at least 15 (the starter has ~20). Did you accidentally delete cells?"
        )

    def test_code_cells_executed(self):
        """At least some code cells should have been executed."""
        nb = load_notebook()
        executed = count_code_cells_with_output(nb)
        assert executed >= 5, (
            f"Only {executed} code cells have outputs. "
            "Run your notebook before submitting."
        )


class TestAnalysisComplete:

    def test_todo_count_reduced(self):
        """Most TODO markers should have been replaced with actual content."""
        nb = load_notebook()
        source = get_all_source(nb)
        # Count remaining TODO markers in markdown cells
        todo_count = 0
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "markdown":
                cell_source = "".join(cell.get("source", []))
                # Count TODOs that are on their own line (student placeholders)
                lines = cell_source.split("\n")
                for line in lines:
                    stripped = line.strip()
                    if stripped == "TODO" or stripped == "TODO\n":
                        todo_count += 1

        # Allow some TODOs (bonus questions, etc.) but most should be filled
        assert todo_count <= 5, (
            f"Found {todo_count} unfilled TODO markers in analysis cells. "
            "Please complete your written analyses."
        )

    def test_portfolio_entry_exists(self):
        """The portfolio entry section should contain student work."""
        nb = load_notebook()
        source = get_all_source(nb)
        assert "portfolio" in source.lower() or "Portfolio" in source, (
            "Portfolio entry section not found. "
            "Make sure you completed the Portfolio Entry v0 section."
        )

    def test_key_takeaways_written(self):
        """The wrap-up section should have key takeaways."""
        nb = load_notebook()
        source = get_all_source(nb)
        assert "takeaway" in source.lower() or "Takeaway" in source or "learned" in source.lower(), (
            "Key takeaways section not found or empty."
        )
