# Results Layout

This directory contains tracked experiment outputs used by the thesis repository.

## Canonical Layout

- `<model>/<batch>/runs/` — per-run raw artifacts.
- `<model>/<batch>/reports/` — aggregated CSVs, plots, and analysis JSON files.
- `<model>/no_explanation_java/` — Java contamination-control outputs and manual correctness tables.

## Legacy Material

- `archive_legacy/` stores older result layouts that were kept for traceability.

For the current reporting flow, prefer the non-legacy model folders at the root of this directory.
