# Python API Request Helper with Unit Tests

A self-directed learning project (2026) where I built a reusable Python helper for making HTTP API requests and wrote a full `unittest` suite for it, using mocking so the tests never touch a real network.

## What it does

`make_request(method, url, **kwargs)` in `api_test.py` wraps the `requests` library and always returns a simple, predictable result:

- `(True, data)` when the request succeeds and the response is valid JSON
- `(True, None)` when the request succeeds but the response body is empty, or the JSON body is `null`
- `(False, None)` when anything goes wrong, with a short message printed explaining why

It handles:

- **HTTP errors** (such as 404 and 500) using `raise_for_status()`, so a failed response is never treated as a success, even if its body contains valid JSON
- **Invalid JSON** in the response body
- **Empty responses**
- **Connection errors** and **timeouts**, caught through the `requests.exceptions.RequestException` hierarchy
- **A default 5-second timeout** that the caller can override (for example `timeout=8`)
- **Extra options** such as headers, query parameters, and JSON request bodies, passed through to `requests`

The same file also includes small demo helpers (`get_user`, `create_user`, `update_user`, `delete_user`, `search_users`) that call [JSONPlaceholder](https://jsonplaceholder.typicode.com/). `authenticated_request()` and `bearer_request()` show how to load an API key or bearer token from environment variables (`MY_API_KEY`, `MY_API_TOKEN`) rather than hardcoding secrets. Running `python api_test.py` calls both helpers and raises `ValueError` if `MY_API_KEY` or `MY_API_TOKEN` is missing.

## Tests

`mocking_test.py` contains 13 tests built with `unittest` and `unittest.mock.patch`. The tests replace `requests.request` with a mock, so they run in milliseconds and don't depend on any outside server.

| Test | What it checks |
|---|---|
| `test_valid_json` | Valid JSON is returned, with the default timeout of 5 |
| `test_json_array` | A JSON array response is returned correctly |
| `test_json_null` | A JSON `null` response is treated as success with `None` data |
| `test_invalid_json` | Bad JSON returns `(False, None)` and prints `JSON decoding failure.` |
| `test_empty_response` | An empty body returns `(True, None)` |
| `test_http_error` | A 404 returns `(False, None)` and prints `HTTP error: 404` |
| `test_server_error` | A 500 with a JSON body still returns `(False, None)` and prints `HTTP error: 500` |
| `test_connection_error` | A connection failure returns `(False, None)` and prints `Request failed: Connection failed` |
| `test_timeout_error` | A timeout returns `(False, None)` and prints `Request failed: Request timed out` |
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

Expected result on Python 3.12. Verbose mode prints one `ok` line per test, then a summary. The elapsed time varies from run to run. A passing run does not print any error text:

```
test_connection_error (mocking_test.TestMakeRequest.test_connection_error) ... ok
test_custom_timeout (mocking_test.TestMakeRequest.test_custom_timeout) ... ok
test_empty_response (mocking_test.TestMakeRequest.test_empty_response) ... ok
test_headers_forwarded (mocking_test.TestMakeRequest.test_headers_forwarded) ... ok
test_http_error (mocking_test.TestMakeRequest.test_http_error) ... ok
test_invalid_json (mocking_test.TestMakeRequest.test_invalid_json) ... ok
test_json_array (mocking_test.TestMakeRequest.test_json_array) ... ok
test_json_null (mocking_test.TestMakeRequest.test_json_null) ... ok
test_post_json (mocking_test.TestMakeRequest.test_post_json) ... ok
test_query_parameters (mocking_test.TestMakeRequest.test_query_parameters) ... ok
test_server_error (mocking_test.TestMakeRequest.test_server_error) ... ok
test_timeout_error (mocking_test.TestMakeRequest.test_timeout_error) ... ok
test_valid_json (mocking_test.TestMakeRequest.test_valid_json) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.003s

OK
```

`make_request` does print on the failure paths. The tests capture those lines with `redirect_stdout` and assert the exact text, so they do not appear in the runner output above. The asserted messages are `JSON decoding failure.`, `HTTP error: 404`, `HTTP error: 500`, `Request failed: Connection failed`, and `Request failed: Request timed out`.

## What I learned

- How to design a function that fails safely and predictably instead of crashing
- How the `requests` exception classes relate to each other, and why order matters (checking the HTTP status before parsing JSON)
- Why `kwargs.pop("timeout", 5)` is used instead of `kwargs.get(...)`, so the timeout isn't passed twice
- How to isolate code from the network with mocks, and how to verify behavior, printed output, and call arguments in tests
- How to keep credentials out of source code by reading them from environment variables

## About

Built by Douglas Marsh as a self-directed learning project. B.S. in Computer Information Science, CompTIA Security+.
