# flask-services

## To run tests under a service, e.g. cv-generator

- Live mode: <code>echo api/tests/test_helper.py | entr -c python -m unittest api.tests.test_helper</code>
- <code>echo api/tests/test_helper.py | coverage run -m unittest api.tests.test_helper</code>
- <code>coverage report -m</code>
