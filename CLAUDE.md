# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

XQAA is a new and improved version of the QAA (Quasi-Analytical Algorithm)
developed by Lee et al. for retrieving Inherent Optical Properties (IOPs) from
remote-sensing reflectance.

## Package layout

- `xqaa/` — the Python package source (`retrieve.py`, `inversion.py`,
  `geometric.py`, `params.py`, and the `qssa/` subpackage).
- `xqaa/data/` — packaged data files (e.g. QSSA bspline/fit coefficients).
- `xqaa/tests/` — the test suite.
- `nb/` — Jupyter notebooks for development and exploration.
- `papers/` — analysis and figure code for publications.
- `claude_prompts/` — prompts and task definitions that drive this work.

## Conventions

- Write clear, well-documented Python with docstrings.

## Git

- **The user (J. Xavier Prochaska) performs all git commands.** Do not run
  `git add`, `git commit`, `git push`, or any other git command that changes
  repository state unless explicitly asked. You may run read-only git commands
  (e.g. `git status`, `git diff`, `git log`) when helpful.
