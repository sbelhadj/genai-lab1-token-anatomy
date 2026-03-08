"""
Sampling Utilities for Lab 1 — Token Anatomy of Code

- generate(): Fully implemented — calls Ollama for text generation.
- measure_diversity(), measure_stability(), measure_coherence():
  STUBS — students must implement these (marked with TODO).

After implementing, the auto-grading tests in tests/test_metrics.py
will verify correctness.
"""

import requests
import json
import numpy as np
from collections import Counter


# ============================================================
# Generation Function (provided — do not modify)
# ============================================================


def generate(prompt, temperature=1.0, top_k=40, top_p=0.9, n=1,
             model="llama3.2:3b", max_tokens=150, timeout=60):
    """
    Generate n completions using Ollama.

    Args:
        prompt: The input prompt string.
        temperature: Sampling temperature (0.0 = greedy, higher = more random).
        top_k: Keep only top-k tokens before sampling.
        top_p: Nucleus sampling threshold.
        n: Number of completions to generate.
        model: Ollama model name.
        max_tokens: Maximum tokens to generate per completion.
        timeout: Request timeout in seconds.

    Returns:
        List of n completion strings.
    """
    results = []
    for _ in range(n):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p,
                        "num_predict": max_tokens,
                    },
                },
                timeout=timeout,
            )
            response.raise_for_status()
            results.append(response.json()["response"])
        except requests.exceptions.RequestException as e:
            results.append(f"[Generation failed: {e}]")
    return results


def generate_from_precomputed(key, filepath="data/precomputed_sampling.json"):
    """
    Load pre-computed outputs as a fallback when Ollama is unavailable.

    Args:
        key: The experiment key (e.g., "temperature_0.5").
        filepath: Path to the precomputed JSON file.

    Returns:
        List of output strings, or empty list if key not found.
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data.get(key, [])
    except FileNotFoundError:
        print(f"⚠ Pre-computed file not found: {filepath}")
        return []


# ============================================================
# Metric Functions — STUDENTS MUST IMPLEMENT THESE
# ============================================================


def measure_diversity(outputs):
    """
    Measure lexical diversity across n outputs using unique bigrams.

    The idea: if all outputs are identical, most bigrams repeat across
    outputs → low diversity score. If outputs are very different, most
    bigrams are unique → high diversity score.

    Args:
        outputs: List of output strings.

    Returns:
        float between 0.0 and 1.0.
        Higher = more diverse outputs.

    Algorithm:
        1. For each output, split into words (lowercase) and extract
           bigrams (pairs of consecutive words).
        2. Collect ALL bigrams from ALL outputs into one list.
        3. Return len(unique_bigrams) / len(all_bigrams).
        4. If there are no bigrams, return 0.0.
    """
    # TODO: Implement this function.
    # Step 1: Collect all bigrams from all outputs
    # Step 2: Count unique vs. total
    # Step 3: Return the ratio
    #
    # Hint:
    #   words = output.lower().split()
    #   bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]

    raise NotImplementedError(
        "measure_diversity() is not yet implemented. "
        "Complete the TODO in utils/sampling_utils.py"
    )


def measure_stability(outputs):
    """
    Measure how similar the outputs are to each other using
    average pairwise Jaccard similarity of word sets.

    Args:
        outputs: List of output strings.

    Returns:
        float between 0.0 and 1.0.
        Higher = more similar (stable) outputs.

    Algorithm:
        1. For each output, create a set of lowercase words.
        2. For every pair of outputs (i, j) where i < j, compute
           Jaccard similarity: |A ∩ B| / |A ∪ B|.
        3. Return the average Jaccard similarity across all pairs.
        4. If there are fewer than 2 outputs, return 1.0.
    """
    # TODO: Implement this function.
    # Hint: use itertools.combinations for generating pairs
    #
    # from itertools import combinations
    # word_sets = [set(o.lower().split()) for o in outputs]
    # for a, b in combinations(word_sets, 2):
    #     jaccard = len(a & b) / len(a | b) if len(a | b) > 0 else 1.0

    raise NotImplementedError(
        "measure_stability() is not yet implemented. "
        "Complete the TODO in utils/sampling_utils.py"
    )


def measure_coherence(outputs):
    """
    Basic coherence check: fraction of outputs that are well-formed.

    A well-formed output:
      - Ends with proper punctuation (. ! ? " ))
      - Does NOT contain excessive repetition (no 3-word sequence
        appearing 3 or more times)

    Args:
        outputs: List of output strings.

    Returns:
        float between 0.0 and 1.0.
        Higher = more coherent outputs.

    Algorithm:
        1. For each output:
           a. Check if the stripped text ends with . ! ? " or )
           b. Extract all 3-word sequences (trigrams).
           c. Check if any trigram appears 3+ times.
           d. Well-formed = ends_ok AND NOT has_repetition.
        2. Return the fraction of well-formed outputs.
        3. If there are no outputs, return 0.0.
    """
    # TODO: Implement this function.
    # Hint:
    #   text = output.strip()
    #   ends_ok = text and text[-1] in '.!?")'
    #   words = text.split()
    #   trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]
    #   trigram_counts = Counter(trigrams)
    #   has_repetition = any(c >= 3 for c in trigram_counts.values())

    raise NotImplementedError(
        "measure_coherence() is not yet implemented. "
        "Complete the TODO in utils/sampling_utils.py"
    )
