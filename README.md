# flask-services

## To run tests under a service, e.g. cv-generator

- Live mode: <code>echo api/tests/test_helpers.py | entr -c python -m unittest api.tests.test_helpers</code>
- One time run: <code>python -m unittest discover -s api.tests.test_helpers</code>
- <code>echo api/tests/test_helpers.py | coverage run -m unittest api.tests.test_helpers</code>
- To run all tests under api/tests directory, <code>coverage run -m unittest discover -s api/tests</code>
- <code>coverage report -m</code>
