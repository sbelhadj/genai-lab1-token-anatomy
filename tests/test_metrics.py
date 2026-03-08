"""
Auto-grading tests for Lab 1 — Metric Implementations

Tests verify that students correctly implemented the three sampling metrics:
  - measure_diversity()
  - measure_stability()
  - measure_coherence()

Students must copy their implementations to utils/sampling_utils.py
for these tests to import them correctly.
"""

import pytest
import sys
import os

# Add project root to path so we can import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Try to import student implementations
try:
    from utils.sampling_utils import measure_diversity, measure_stability, measure_coherence

    # Check if functions are actually implemented (not just stubs)
    try:
        measure_diversity(["test sentence one", "test sentence two"])
        DIVERSITY_IMPLEMENTED = True
    except NotImplementedError:
        DIVERSITY_IMPLEMENTED = False

    try:
        measure_stability(["test sentence one", "test sentence two"])
        STABILITY_IMPLEMENTED = True
    except NotImplementedError:
        STABILITY_IMPLEMENTED = False

    try:
        measure_coherence(["Test sentence one.", "Test sentence two."])
        COHERENCE_IMPLEMENTED = True
    except NotImplementedError:
        COHERENCE_IMPLEMENTED = False

except ImportError:
    DIVERSITY_IMPLEMENTED = False
    STABILITY_IMPLEMENTED = False
    COHERENCE_IMPLEMENTED = False


# ============================================================
# Test: measure_diversity
# ============================================================


@pytest.mark.skipif(not DIVERSITY_IMPLEMENTED, reason="measure_diversity not implemented yet")
class TestMeasureDiversity:

    def test_identical_outputs_low_diversity(self):
        """Identical outputs should have low diversity."""
        outputs = ["The cat sat on the mat."] * 5
        score = measure_diversity(outputs)
        assert score is not None, "measure_diversity returned None"
        assert isinstance(score, (int, float)), f"Expected numeric, got {type(score)}"
        assert 0.0 <= score <= 1.0, f"Score {score} not in [0, 1]"
        assert score < 0.3, f"Identical outputs should have low diversity, got {score}"

    def test_diverse_outputs_high_diversity(self):
        """Very different outputs should have high diversity."""
        outputs = [
            "The quick brown fox jumps over the lazy dog near the river bank.",
            "Python is a popular programming language for data science and web development.",
            "Mount Everest is the tallest mountain in the world at over eight thousand meters.",
            "Jazz music originated in New Orleans in the early nineteen hundreds.",
            "The periodic table organizes chemical elements by their atomic number and properties.",
        ]
        score = measure_diversity(outputs)
        assert score > 0.7, f"Diverse outputs should have high diversity, got {score}"

    def test_returns_float(self):
        """Should return a float."""
        score = measure_diversity(["Hello world.", "Goodbye world."])
        assert isinstance(score, (int, float)), f"Expected numeric, got {type(score)}"

    def test_empty_output_handled(self):
        """Should handle outputs containing empty strings gracefully."""
        score = measure_diversity(["", "", ""])
        assert score is not None, "Should handle empty strings without crashing"

    def test_single_word_outputs(self):
        """Single-word outputs have no bigrams — should handle gracefully."""
        score = measure_diversity(["Hello", "World", "Test"])
        assert score is not None, "Should handle single-word outputs"


# ============================================================
# Test: measure_stability
# ============================================================


@pytest.mark.skipif(not STABILITY_IMPLEMENTED, reason="measure_stability not implemented yet")
class TestMeasureStability:

    def test_identical_outputs_high_stability(self):
        """Identical outputs should have high (near 1.0) stability."""
        outputs = ["Unit testing is important for code quality and reliability."] * 5
        score = measure_stability(outputs)
        assert score is not None, "measure_stability returned None"
        assert isinstance(score, (int, float)), f"Expected numeric, got {type(score)}"
        assert score > 0.9, f"Identical outputs should have high stability, got {score}"

    def test_different_outputs_low_stability(self):
        """Completely different outputs should have low stability."""
        outputs = [
            "Apples are red fruits that grow on trees.",
            "The Eiffel Tower is located in Paris France.",
            "Quantum computing uses qubits instead of classical bits.",
            "Soccer is the most popular sport played worldwide.",
            "Photosynthesis converts light energy into chemical energy.",
        ]
        score = measure_stability(outputs)
        assert score < 0.3, f"Different outputs should have low stability, got {score}"

    def test_partially_similar_outputs(self):
        """Outputs sharing some words should have medium stability."""
        outputs = [
            "Unit testing verifies that individual components work correctly.",
            "Unit testing ensures that each function produces expected results.",
            "Unit testing is a practice where developers test small pieces of code.",
        ]
        score = measure_stability(outputs)
        assert 0.1 < score < 0.8, f"Partially similar outputs: expected medium stability, got {score}"

    def test_single_output(self):
        """A single output should return 1.0 (nothing to compare against)."""
        score = measure_stability(["Just one output."])
        assert score == 1.0 or score is not None, "Single output should be handled"


# ============================================================
# Test: measure_coherence
# ============================================================


@pytest.mark.skipif(not COHERENCE_IMPLEMENTED, reason="measure_coherence not implemented yet")
class TestMeasureCoherence:

    def test_wellformed_outputs_high_coherence(self):
        """Well-formed sentences should score high."""
        outputs = [
            "Unit testing ensures code reliability.",
            "Testing is crucial for API development.",
            "Automated tests catch bugs early in the process.",
        ]
        score = measure_coherence(outputs)
        assert score is not None, "measure_coherence returned None"
        assert isinstance(score, (int, float)), f"Expected numeric, got {type(score)}"
        assert score > 0.8, f"Well-formed outputs should score high, got {score}"

    def test_repetitive_outputs_low_coherence(self):
        """Outputs with heavy repetition should score lower."""
        outputs = [
            "the the the the the the the the the the the the the the the",
            "testing is is is testing is is is testing is is is very good",
            "I think I think I think I think I think this is a test result",
        ]
        score = measure_coherence(outputs)
        assert score < 0.5, f"Repetitive outputs should score low, got {score}"

    def test_no_punctuation_lower_coherence(self):
        """Outputs without proper ending punctuation should score lower."""
        outputs = [
            "This sentence does not end properly and keeps going on and",
            "Another sentence that just trails off without any clear ending",
            "Testing one two three four five six seven eight nine ten",
        ]
        score = measure_coherence(outputs)
        assert score < 0.5, f"Outputs without punctuation should score low, got {score}"

    def test_mixed_quality(self):
        """Mix of well-formed and malformed should give medium score."""
        outputs = [
            "This is a well-formed sentence.",
            "the the the the the the the the the the the the",
            "Another proper sentence with good structure!",
            "trailing off without punctuation or clear ending and",
        ]
        score = measure_coherence(outputs)
        assert 0.2 < score < 0.8, f"Mixed quality should give medium score, got {score}"

    def test_empty_outputs(self):
        """Should handle empty strings gracefully."""
        score = measure_coherence(["", "", ""])
        assert score is not None, "Should handle empty strings without crashing"
