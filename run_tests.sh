cd src
# PYTHONPATH=. pytest -s tests.py --maxfail=1
PYTHONPATH=. pytest tests.py --maxfail=1

# bash run_tests.sh > output.log 2>&1
