# Python API Request Helper with Unit Tests

A self-directed learning project (2026) where I built a reusable Python helper for making HTTP API requests and wrote a full `unittest` suite for it, using mocking so the tests never touch a real network.

## What it does

`make_request(method, url, **kwargs)` in `api_test.py` wraps the `requests` library and always returns a simple, predictable result:

- `(True, data)` when the request succeeds and the response is valid JSON
- `(True, None)` when the request succeeds but the response body is empty
- `(False, None)` when anything goes wrong, with a short message printed explaining why

It handles:

- **HTTP errors** (such as 404 and 500) using `raise_for_status()`, so a failed response is never treated as a success, even if its body contains valid JSON
- **Invalid JSON** in the response body
- **Empty responses**
- **Connection errors** and **timeouts**, caught through the `requests.exceptions.RequestException` hierarchy
- **A default 5-second timeout** that the caller can override (for example `timeout=8`)
- **Extra options** such as headers, query parameters, and JSON request bodies, passed through to `requests`

## Tests

`mocking_test.py` contains 13 tests built with `unittest` and `unittest.mock.patch`. The tests replace `requests.request` with a mock, so they run in milliseconds and don't depend on any outside server.

| Test | What it checks |
|---|---|
| `test_valid_json` | Valid JSON is returned, with the default timeout of 5 |
| `test_json_array` | A JSON array response is returned correctly |
| `test_json_null` | A JSON `null` response is handled |
| `test_invalid_json` | Bad JSON returns `(False, None)` and prints an error |
| `test_empty_response` | An empty body returns `(True, None)` |
| `test_http_error` | A 404 returns `(False, None)` and prints `HTTP error: 404` |
| `test_server_error` | A 500 with a JSON body still returns `(False, None)` |
| `test_connection_error` | A connection failure is caught and reported |
| `test_timeout_error` | A timeout is caught and reported |
| `test_custom_timeout` | A caller-supplied timeout is passed through |
| `test_headers_forwarded` | Custom headers are passed through |
| `test_query_parameters` | Query parameters are passed through |
| `test_post_json` | A POST with a JSON body is sent correctly |

Techniques used in the tests:

- Building mock `Response` objects with a helper method and a shared `setUp()`
- Capturing printed output with `StringIO` and `redirect_stdout` and checking the exact message
- Checking the mock's call arguments with `assert_called_once_with` to confirm the right method, URL, timeout, and options were sent
- Re-running the full suite after every change to make sure existing tests still pass (regression testing)

## How to run it

Requires Python 3 and the `requests` library.

```bash
pip install -r requirements.txt
python -m unittest mocking_test.py -v
```

Expected result:

```
Ran 13 tests

OK
```

(The `JSON decoding failure.` line printed during the run is expected; it comes from the invalid-JSON test.)

## What I learned

- How to design a function that fails safely and predictably instead of crashing
- How the `requests` exception classes relate to each other, and why order matters (checking the HTTP status before parsing JSON)
- Why `kwargs.pop("timeout", 5)` is used instead of `kwargs.get(...)`, so the timeout isn't passed twice
- How to isolate code from the network with mocks, and how to verify behavior, printed output, and call arguments in tests

## About

Built by Douglas Marsh as part of my hands-on study toward IT support, QA, and cybersecurity roles. B.S. in Computer Information Science, CompTIA Security+.
