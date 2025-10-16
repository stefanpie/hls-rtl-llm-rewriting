# HLS RTL LLM Rewriting

## Project Overview

High-Level Synthesis (HLS) tools quickly generate RTL, but the output is often hard to read, modify, and integrate into a larger system design. This project explores using large language models (LLMs) to rewrite HLS-generated Verilog so that the resulting code is cleaner, easier to maintain, and potentially more efficient. The workflow pairs LLM rewriting with open-source formal verification (Eqy, SymbiYosys, Yosys, SMT solvers) to guarantee that the rewritten design remains functionally equivalent to the original.

We are intrested in two notions of equivalence between the original and rewritten RTL:

- **Cycle-accurate equivalence**: rewritten RTL matches the original on every clock cycle.
- **Latency-insensitive equivalence**: rewritten RTL eventually matches outputs, even if asserted on the output at a different clock cycle. Achieving this requires a richer verification harness driven by SystemVerilog Assertions, which is part of the planned work.

Beyond rewriting RTL directly, we plan to correlate C/C++ HLS source, LLVM IR, and generated RTL (via extensions to `libvhls`) so that LLMs can reason over consistent semantic context across compilation stages.

## Current Prototype

The repository currently implements a simple zero-shot prototype that:

1. Sends HLS-generated Verilog to an LLM (OpenRouter model configuration).
2. Captures the rewritten module from the model response.
3. Validates the result by checking that Yosys can synthesize it.
4. Runs an Eqy-based formal equivalence check for cycle-accurate correctness.

Prototype entry point: `main.py`, which targets the sample design in `test_design/` and writes intermediate artifacts to `work/`.

## Running the Prototype

### Prerequisites

- Python 3.13 or newer.
- Yosys and Eqy available on your `PATH`.
- An OpenRouter API key (`OPENROUTER_API_KEY`) with access to the configured model.

### Install Python Dependencies

Using `uv` (preferred):

```bash
uv sync
```

Or with `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install llm-openrouter python-dotenv llm
```

### Configure Environment

Create a `.env` file or export the variable in your shell:

```bash
export OPENROUTER_API_KEY=sk-...
```

### Run

Execute the prototype from the repository root:

```bash
uv run python main.py
```

If not using `uv`, run the script with your environment’s Python:

```bash
python main.py
```

The script will print LLM progress, dump rewritten variants under `work/<top_module>/`, and log Yosys/Eqy outputs for inspection.

## Roadmap

- Structured prompts and model selection strategies to improve rewrite quality and pass rates.
- Variable-aware rewriting flows (rename-only passes, AST-guided transformations).
- Latency-insensitive verification harness generation using SystemVerilog Assertions.
- Integration with extended `libvhls` metadata to track constructs across HLS compilation stages.
- Tooling to triage and score multiple rewrite attempts automatically.
