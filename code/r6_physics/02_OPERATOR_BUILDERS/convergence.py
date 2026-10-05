"""Resolution comparisons and simple competing extrapolation models."""

from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit


def normalized_residual(coarse: np.ndarray, fine: np.ndarray) -> float:
    a, b = np.asarray(coarse, dtype=float), np.asarray(fine, dtype=float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(b), 1e-300))


def fit_limit(level: np.ndarray, values: np.ndarray) -> dict[str, float | str]:
    x, y = np.asarray(level, dtype=float), np.asarray(values, dtype=float)

    def power(z, limit, amplitude, exponent):
        return limit + amplitude / np.maximum(z, 1e-12) ** exponent

    try:
        params, _ = curve_fit(power, x, y, p0=(y[-1], y[0] - y[-1], 1.0), maxfev=20000)
        fitted = power(x, *params)
        rss = float(np.sum((y - fitted) ** 2))
        return {"model": "limit+a/N^alpha", "limit": float(params[0]), "amplitude": float(params[1]), "exponent": float(params[2]), "rss": rss}
    except Exception:
        return {"model": "rejected", "limit": float(y[-1]), "amplitude": float("nan"), "exponent": float("nan"), "rss": float("inf")}

