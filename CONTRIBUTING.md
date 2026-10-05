# Contributing

Use Python 3.11. Install `requirements.txt`, keep generated data under ignored output directories, and run:

```bash
python reproduce.py audit
python reproduce.py test validation
python reproduce.py test r6
python reproduce.py test r7
python reproduce.py r6-demo
python reproduce.py r7-certificate
python tools/audit_release.py
```

Do not commit generated figures, checkpoints, run logs, publication PDFs, large binary registries, or Node.js dependencies. Keep new current code outside `code/exact_replay/`; that directory is the frozen complete replay layer.
