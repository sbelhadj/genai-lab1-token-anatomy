# Lab 1 — Token Anatomy of Code

**Generative AI & Prompt Engineering — A Mechanistic Approach**

Module 1: Understanding Text Generation | Duration: 90 minutes

---

## Overview

In this lab, you will explore **how an LLM tokenizes and generates text** — the foundational mechanics that every prompting technique in this course builds upon. You will work with real code from the **TaskFlow** project (a task management REST API) and discover why tokenization and sampling parameters matter for prompt engineering.

**Core principle:** *A prompt is not an incantation — it is a structured input that shapes which tokens the model considers probable.*

---

## Quick Start

### Option A: GitHub Codespaces (Recommended)

1. Click the green **"Code"** button → **"Codespaces"** → **"Create codespace on main"**
2. Wait for the environment to build (~3–5 minutes the first time)
3. The devcontainer will automatically install all dependencies and start Ollama
4. Open `lab1_token_anatomy.ipynb` in the Jupyter extension

### Option B: Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd genai-lab1-token-anatomy

# Install dependencies
pip install transformers tokenizers sentencepiece jupyter pandas matplotlib numpy requests pytest jsonschema

# Install and start Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.2:3b

# Launch Jupyter
jupyter notebook
```

### Verify Setup

Run these checks before starting:

```bash
# Check Python packages
python -c "from transformers import AutoTokenizer; print('✓ Tokenizer ready')"
python -c "import pandas, matplotlib, numpy, requests; print('✓ All packages ready')"

# Check Ollama (may take a moment on first run)
curl -s http://localhost:11434/api/tags | python -c "import sys,json; models=json.load(sys.stdin).get('models',[]); print(f'✓ Ollama running: {[m[\"name\"] for m in models]}')"
```

---

## Repository Structure

```
genai-lab1-token-anatomy/
├── .devcontainer/
│   └── devcontainer.json          # Codespaces configuration
├── .github/
│   └── workflows/
│       └── autograding.yml        # Auto-grading on push
├── lab1_token_anatomy.ipynb       # ← YOUR MAIN WORKSPACE
├── utils/
│   ├── __init__.py
│   ├── tokenizer_utils.py         # analyze_tokens() and helpers
│   └── sampling_utils.py          # generate() + metric stubs to complete
├── data/
│   ├── taskflow_snippets.json     # TaskFlow code samples
│   └── precomputed_sampling.json  # Backup if Ollama is unavailable
├── tests/
│   ├── __init__.py
│   ├── test_metrics.py            # Auto-graded: your metric implementations
│   └── test_notebook_structure.py # Auto-graded: notebook completeness
├── README.md                      # This file
└── .gitignore
```

---

## What to Do

1. Open `lab1_token_anatomy.ipynb`
2. Follow the instructions in each section
3. Complete all cells marked with `# TODO`
4. Write your analyses in the markdown cells
5. When finished, **copy your metric functions** to `utils/sampling_utils.py` (the auto-grader imports from there)

---

## Deliverables

| # | What | Where |
|---|------|-------|
| 1 | Completed notebook with all exercises | `lab1_token_anatomy.ipynb` |
| 2 | Metric implementations | `utils/sampling_utils.py` |
| 3 | Token comparison table (20 samples) | In notebook |
| 4 | Written analysis (4 questions) | In notebook |
| 5 | Temperature sweep chart | In notebook |
| 6 | Portfolio entry v0 | In notebook |

---

## Submitting

```bash
git add -A
git commit -m "Lab 1 complete"
git push
```

Auto-grading runs automatically on push. Check the **Actions** tab for results.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Ollama won't start | Run `ollama serve &` manually, wait 10s, then `ollama pull llama3.2:3b` |
| Out of memory in Codespaces | Use `gpt2` tokenizer for Part A; use `data/precomputed_sampling.json` for Part B |
| Can't load Llama tokenizer | You need a HuggingFace account with Llama access. Fallback: `AutoTokenizer.from_pretrained("gpt2")` |
| Kernel crashes during sampling | Reduce `n=10` to `n=5` in temperature sweep |
| Auto-grading fails | Ensure your metric functions are in `utils/sampling_utils.py` with correct names |

---

## Academic Integrity

You are encouraged to use AI tools as part of the learning process — this is a course about generative AI. However, all written analyses must reflect your own understanding. Document what you generated, what you modified, and why.

---

*Lab 1 of 8 — DevAssist / TaskFlow Lab Series*
