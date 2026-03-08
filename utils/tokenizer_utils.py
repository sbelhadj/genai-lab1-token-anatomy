"""
Tokenizer Utilities for Lab 1 — Token Anatomy of Code

Provides helper functions for tokenization analysis.
These are fully implemented — students use them as tools.
"""

import os

# ============================================================
# Tokenizer Loading
# ============================================================

_tokenizer = None


def get_tokenizer():
    """Load and cache the tokenizer. Tries Llama 3.2, falls back to GPT-2."""
    global _tokenizer
    if _tokenizer is not None:
        return _tokenizer

    from transformers import AutoTokenizer

    # Try Llama 3.2 first
    try:
        _tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B")
        print(f"✓ Loaded Llama 3.2 tokenizer (vocab size: {_tokenizer.vocab_size})")
    except Exception:
        # Fallback to GPT-2 (no auth required)
        _tokenizer = AutoTokenizer.from_pretrained("gpt2")
        print(f"⚠ Llama tokenizer unavailable. Using GPT-2 fallback (vocab size: {_tokenizer.vocab_size})")
        print("  (Token counts will differ from Llama, but all concepts still apply.)")

    return _tokenizer


# ============================================================
# Core Analysis Functions
# ============================================================


def analyze_tokens(text, label="", tokenizer=None):
    """
    Tokenize text and display detailed results.

    Args:
        text: The string to tokenize.
        label: A short label for identification.
        tokenizer: Optional tokenizer override. Uses default if None.

    Returns:
        dict with keys: label, text, token_count, char_count,
                        tokens_per_char, tokens (decoded), ids
    """
    if tokenizer is None:
        tokenizer = get_tokenizer()

    token_ids = tokenizer.encode(text)
    decoded_tokens = [tokenizer.decode([t]) for t in token_ids]
    char_count = len(text)
    token_count = len(token_ids)
    ratio = token_count / max(char_count, 1)

    print(f"\n{'=' * 60}")
    print(f"  Label:        {label}")
    print(f"  Input:        {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"  Token count:  {token_count}")
    print(f"  Char count:   {char_count}")
    print(f"  Tokens/char:  {ratio:.3f}")
    print(f"  Tokens:       {decoded_tokens[:12]}{'...' if len(decoded_tokens) > 12 else ''}")
    print(f"{'=' * 60}")

    return {
        "label": label,
        "text": text,
        "token_count": token_count,
        "char_count": char_count,
        "tokens_per_char": round(ratio, 3),
        "tokens": decoded_tokens,
        "ids": token_ids,
    }


def compare_tokenizations(texts_dict, tokenizer=None):
    """
    Tokenize a dictionary of {label: text} and return all results.

    Args:
        texts_dict: dict mapping labels to text strings.
        tokenizer: Optional tokenizer override.

    Returns:
        dict mapping labels to analyze_tokens results.
    """
    results = {}
    for label, text in texts_dict.items():
        results[label] = analyze_tokens(text, label=label, tokenizer=tokenizer)
    return results


def build_comparison_table(results):
    """
    Build a pandas DataFrame from tokenization results.

    Args:
        results: dict from compare_tokenizations().

    Returns:
        pandas DataFrame sorted by token count descending.
    """
    import pandas as pd

    rows = []
    for key, r in results.items():
        rows.append({
            "Label": r["label"],
            "Text (preview)": r["text"][:50] + ("..." if len(r["text"]) > 50 else ""),
            "Token Count": r["token_count"],
            "Char Count": r["char_count"],
            "Tokens/Char": r["tokens_per_char"],
            "First 8 Tokens": str(r["tokens"][:8]),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("Token Count", ascending=False).reset_index(drop=True)
    return df
