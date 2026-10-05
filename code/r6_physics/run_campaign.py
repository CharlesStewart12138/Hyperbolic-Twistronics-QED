"""Canonical R6 entry point for calculations, figures, and catalogs."""

from __future__ import annotations

import argparse
import json

from campaign_core import ROOT, compute_all
import campaign_figures as figure_module
from figure_repair import install as install_figure_repair


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="recompute numerical HDF5 checkpoints")
    parser.add_argument("--figures-only", action="store_true")
    args = parser.parse_args()
    if not args.figures_only:
        compute_all(force=args.force)
    install_figure_repair(figure_module)
    rows = figure_module.generate_all_figures()
    print(json.dumps({"status": "figures_complete", "count": len(rows), "catalog": str(ROOT / "12_FIGURES" / "FINAL_FIGURE_CATALOG.json")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

