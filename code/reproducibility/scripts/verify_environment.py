from __future__ import annotations

import importlib
import json
import platform
import sys
from importlib import metadata


EXPECTED = {
    "pip": "26.0.1",
    "numpy": "1.26.4",
    "scipy": "1.17.0",
    "matplotlib": "3.7.2",
    "pandas": "3.0.0",
    "networkx": "3.6.1",
    "h5py": "3.9.0",
    "pyarrow": "11.0.0",
    "PyYAML": "6.0",
    "sympy": "1.14.0",
    "Pillow": "12.3.0",
    "psutil": "5.9.0",
}

IMPORT_NAMES = {
    "PyYAML": "yaml",
    "Pillow": "PIL",
}


def main() -> int:
    report: dict[str, object] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {},
        "checks": {},
    }
    failures: list[str] = []

    if platform.python_version() != "3.11.5":
        failures.append(f"python expected 3.11.5, found {platform.python_version()}")

    packages = report["packages"]
    assert isinstance(packages, dict)
    for distribution, expected_version in EXPECTED.items():
        try:
            actual_version = metadata.version(distribution)
            importlib.import_module(IMPORT_NAMES.get(distribution, distribution))
        except Exception as exc:  # noqa: BLE001 - verifier must report every import failure
            actual_version = f"ERROR: {exc}"
        packages[distribution] = actual_version
        if actual_version != expected_version:
            failures.append(
                f"{distribution} expected {expected_version}, found {actual_version}"
            )

    import numpy as np
    import scipy.linalg as scipy_linalg

    matrix = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=float)
    numpy_eigenvalues = np.linalg.eigvalsh(matrix)
    scipy_eigenvalues = scipy_linalg.eigvalsh(matrix)
    expected_eigenvalues = np.array([1.0, 3.0])
    numpy_ok = bool(np.allclose(numpy_eigenvalues, expected_eigenvalues))
    scipy_ok = bool(np.allclose(scipy_eigenvalues, expected_eigenvalues))
    agreement_ok = bool(np.allclose(numpy_eigenvalues, scipy_eigenvalues))

    checks = report["checks"]
    assert isinstance(checks, dict)
    checks["numpy_hermitian_eigenvalues"] = numpy_eigenvalues.tolist()
    checks["scipy_hermitian_eigenvalues"] = scipy_eigenvalues.tolist()
    checks["numpy_expected"] = numpy_ok
    checks["scipy_expected"] = scipy_ok
    checks["numpy_scipy_agree"] = agreement_ok
    if not (numpy_ok and scipy_ok and agreement_ok):
        failures.append("Hermitian eigensolver smoke test failed")

    report["failures"] = failures
    report["status"] = "PASS" if not failures else "FAIL"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

