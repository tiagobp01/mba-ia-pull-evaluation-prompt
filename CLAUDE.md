# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a prompt engineering challenge project for an MBA in AI. The goal is to convert bug reports into structured Agile User Stories using LangChain and LangSmith. The project evaluates two prompt versions (v1 = baseline bad prompt, v2 = optimized prompt) against a dataset, with all 5 metrics required to score ≥ 0.9 to pass.

## Setup

```bash
cp .env.example .env
# Fill in LANGSMITH_API_KEY, USERNAME_LANGSMITH_HUB, GOOGLE_API_KEY (or OPENAI_API_KEY)

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

```bash
# Run tests (validates prompts/bug_to_user_story_v2.yml structure)
pytest tests/test_prompts.py -v

# Pull v1 prompt from LangSmith Hub → saves to prompts/bug_to_user_story_v1.yml
python src/pull_prompts.py

# Push v2 prompt to LangSmith Hub (must be done before evaluate.py)
python src/push_prompts.py

# Run full evaluation (5 metrics against datasets/bug_to_user_story.jsonl)
python src/evaluate.py

# Test metrics module independently
python src/metrics.py
```

**Via Docker:**
```bash
docker compose build
docker compose run --rm app pytest tests/test_prompts.py -v
docker compose run --rm app python src/evaluate.py
```

## Architecture

**Data flow:** `datasets/bug_to_user_story.jsonl` → LangSmith dataset → prompt chain → LLM-as-Judge evaluation

**Key files:**
- `prompts/bug_to_user_story_v2.yml` — the optimized prompt (source of truth; push it to Hub, then evaluate)
- `src/evaluate.py` — orchestrates the full eval loop: loads dataset from JSONL, creates LangSmith dataset, pulls prompt from Hub, runs chain, computes 5 metrics
- `src/metrics.py` — LLM-as-Judge implementations for F1-Score, Clarity, Precision (used by evaluate.py) plus 4 domain-specific metrics not currently used in evaluate.py
- `src/utils.py` — shared helpers: `get_llm()` / `get_eval_llm()` (provider-switching), YAML I/O, env validation

**Metric computation in evaluate.py:**
- `helpfulness = (clarity + precision) / 2`
- `correctness = (f1 + precision) / 2`
- All 5 metrics (helpfulness, correctness, f1_score, clarity, precision) must be ≥ 0.9 and average ≥ 0.9 to pass

## LLM Provider Configuration

Controlled via `.env`. The `get_llm()` / `get_eval_llm()` functions in `src/utils.py` dispatch based on `LLM_PROVIDER`:

| Variable | Default | Purpose |
|---|---|---|
| `LLM_PROVIDER` | `openai` | `openai` or `google` |
| `LLM_MODEL` | `gpt-4o-mini` | Model for prompt execution |
| `EVAL_MODEL` | `gpt-4o` | Model for LLM-as-Judge metrics |

The `.env.example` defaults to `google` / `gemini-2.5-flash` for both.

## Prompt YAML Structure

`prompts/bug_to_user_story_v2.yml` must have these fields under the `bug_to_user_story_v2` key for `push_prompts.py` and tests to work:

```yaml
bug_to_user_story_v2:
  description: "..."
  system_prompt: |
    ...
  user_prompt: "{bug_report}"
  version: "v2"
  techniques_applied: ["...", "..."]  # minimum 2
```

The `user_prompt` must use `{bug_report}` as the input variable (matched by `evaluate.py` when building the chain).

## Evaluation Dataset

`datasets/bug_to_user_story.jsonl` — JSONL where each line has `inputs` and `outputs`:
- `inputs`: contains `bug_report` (or `question`) key
- `outputs`: contains `reference` key (ground truth User Story)
