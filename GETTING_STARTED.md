# Getting started

## 1. Set up Python

Python 3.10 or newer is required.

```bash
python -m venv .venv
```

Activate the environment using the command appropriate for your shell, then install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The runtime dependencies are deliberately small: NumPy, pandas, Matplotlib, and pytest.

## 2. Verify the workspace

```bash
pytest -q
python scripts/smoke_test.py
python scripts/anonymity_scan.py .
```

The smoke test runs at least 1,000 deterministic known-`M` cubic checks, several special action geometries, and a clearly labelled out-of-assumption diagnostic. A passing run is not a proof of the theorem.

## 3. Understand the two layers

Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md), then work through [docs/RESEARCH_TUTORIAL.md](docs/RESEARCH_TUTORIAL.md). The shortest reliable mental model is:

```text
frozen geometry -> intrinsic value -> finite candidate action
two candidate actions -> paired transfer radius -> certified or unresolved ranking
```

Intrinsic scale invariance does not imply equal finite actions: rescaling a geometry changes the step size unless the action-selection rule compensates for it.

## 4. Run a deeper theorem attack

```bash
python scripts/numerical_theorem_check.py --cases 50000 --seed 2027
python scripts/counterexample_search.py --cases 50000 --seed 2027
```

Any valid under-assumption violation exits nonzero and saves the exact inputs in a new `results/theorem_stress/...` directory. Do not weaken a test or silently discard a counterexample.

## 5. Choose an independent task

Start with [TASK 02](tasks/TASK_02_NUMERICAL_STRESS_TEST.md). It is designed to produce useful evidence without requiring access to frozen Gate-3 artifacts. Tasks involving frozen data must wait until authoritative, action-level artifacts are intentionally supplied read-only.
