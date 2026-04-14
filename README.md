# ECSE520

# Information-Theoretic Inequality Proofs with Consumer LLMs: A Benchmark Using PSITIP

This repository contains the code, data, and results from the project that evaluates six consumer large language models (LLMs) on a benchmark of 75 information‑theoretic inequalities. The ground truth for each inequality was established using PSITIP, a Python library that verifies both Shannon‑type and non‑Shannon‑type inequalities.

## Necessary Files to Run the Notebooks

- **`psitip_exprs.py`** – Python module containing the PSITIP region objects and context managers for each inequality. The notebooks import this module to obtain the ground truth for verification.
- **`all_ineq_ordered.txt`** – Text file with one inequality per line, in the same order as `psitip_exprs.py`. The notebooks read this file to display labels, build prompts, and map results.

Both files **must** be present in the main folder (or in a location where the notebooks can import/read them).

## Dependencies and License Requirements

- **PSITIP** requires a working installation of `psitip`. The project uses the **Gurobi** LP solver (recommended for numerical stability). A **Gurobi license** is required; academic licenses are available free of charge from Gurobi. Without a Gurobi license, PSITIP may fall back to other solvers (e.g., CBC) but may produce false positives or be slower. For full reproducibility, obtain a Gurobi license and set it up before running the notebooks.

- **API keys** for the LLM providers:
  - OpenAI: `OPENAI_API_KEY`
  - Anthropic: `ANTHROPIC_API_KEY`
  - DeepSeek: `DEEPSEEK_API_KEY` (optional, depending on which models you run)

- **Python packages**: `psitip`, `openai`, `anthropic`, `requests`, `jupyter`, `gurobipy`, `pyomo` . Install with:
  ```bash
  pip install psitip openai anthropic requests jupyter gurobipy pyomo
## Contents
## 1. Results (Result/ folder)
JSON files contain the detailed evaluation results for each model. Each file includes:

Verdict accuracy (True/False) per inequality

Type classification (Shannon vs. Non‑Shannon) for true inequalities

Proof quality metrics: PV Consecutive, Axiom Recall, and composite Proof Quality

LLM raw output

PV Consecutive failure analysis (LP‑contradicted / LP‑unproven steps)

Token usage and estimated cost (standard and batch‑discounted)

DeepSeek Chat returned 72 valid responses; three cases failed due to cases that hit the maximum token limit.

GPT-5.4 Pro had one case that hit the maximum token limit (74/75).

All other models completed all 75 inequalities.

## 2. Notebooks (main folder)
Each Jupyter notebook reproduces the evaluation for one model. The notebooks:

Load the test set from psitip_exprs.py and all_ineq_ordered.txt

Send the prompt to the model’s API

Parse the responses and compute metrics

Save the results as JSON in the Result/ folder

To run a notebook, ensure you have the required API keys and a Gurobi license.

## 3. PSITIP Test Cases (psitip_exprs.py)
This Python module exports:

psitip_exprs: a list of tuples (region, ctx_fn) where region is a PSITIP region object and ctx_fn is a context manager for constraints (e.g., Markov chains, copy lemma) or None.

CL: a constant (e.g., "Copy Lemma") used for type classification.

## 4. Inequality List (all_ineq_ordered.txt)
Plain text file with one inequality per line, in the same order as psitip_exprs.py. Used for cross‑referencing and prompt generation.


Notes on the Data
The ground truth for all inequalities was pre‑verified using PSITIP with the Gurobi solver.

Internet search is not enabled for all API calls to prevent contamination.

Temperature was set to 0 for all models (except DeepSeek Reasoner, which does not support temperature) to ensure deterministic outputs.

Batch API discounts (50%) were applied for OpenAI and Anthropic models where possible.

{LLM_PSITIP_2026,
  author = {Kenza Bellebouir},
  title = {Information-Theoretic Inequality Proofs with Consumer LLMs: A Benchmark Using PSITIP},
  institution = {Mcgill University - ECSE520},
  year = {2026},
  note = {Available at: [\url{(https://github.com/kbellebouir/ECSE520)](https://github.com/kbellebouir/ECSE520)}}
}

Contact
For questions or issues, please contact the author at kbellebouir@gmail.com
