import unittest
import requests
from unittest.mock import patch
from requests import Response
from api_test import make_request
from contextlib import redirect_stdout
from io import StringIO

class TestMakeRequest(unittest.TestCase):

    def setUp(self):
        self.url = "https://example.com"

    def make_mock_response(self, status_code, content):
        mock_response = Response()
        mock_response.status_code = status_code
        mock_response._content = content
        mock_response.url = self.url
        return mock_response

    @patch("requests.request")
    def test_valid_json(self, mock_request):
        mock_response = self.make_mock_response(
            200,
            b'{"name": "Douglas"}'
        )
        mock_request.return_value = mock_response

        result = make_request("GET", self.url)

        self.assertEqual(result, (True, {"name": "Douglas"}))

        mock_request.assert_called_once_with(
            "GET",
            self.url,
            timeout=5
        )

    @patch("requests.request")
    def test_invalid_json(self, mock_request):
        mock_response = self.make_mock_response(
            200,
            b"not valid JSON"
        )

        mock_request.return_value = mock_response

        output = StringIO()
        with redirect_stdout(output):
            result = make_request("GET", self.url)

        self.assertEqual(result, (False, None))
        self.assertEqual(
            output.getvalue().strip(),
            "JSON decoding failure."
        )

    @patch("requests.request")
    def test_http_error(self, mock_request):
        mock_response = self.make_mock_response(
            404,
            b'{"error": "Not Found"}'
        )
        
        mock_request.return_value = mock_response

        output = StringIO()
        with redirect_stdout(output):
            result = make_request("GET", self.url)

        self.assertEqual(result, (False, None))
        self.assertEqual(
            output.getvalue().strip(),
            "HTTP error: 404"
        )

    @patch("requests.request")
    def test_empty_response(self, mock_request):
        mock_response = self.make_mock_response(
            204,
            b""
        )
        
        mock_request.return_value = mock_response

        result = make_request("GET", self.url)

        self.assertEqual(result, (True, None))

    @patch("requests.request")
    def test_connection_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        output = StringIO()
        with redirect_stdout(output):
            result = make_request("GET", self.url)

        self.assertEqual(result, (False, None))
        self.assertEqual(
            output.getvalue().strip(),
            "Request failed: Connection failed"
        )
        mock_request.assert_called_once_with(
            "GET",
            self.url,
            timeout=5
        )

    @patch("requests.request")
    def test_json_array(self, mock_request):
        mock_response = self.make_mock_response(
            200,
            b'["apple", "banana", "orange"]'
        )
        mock_request.return_value = mock_response

        result = make_request("GET", self.url)

        self.assertEqual(
            result,
            (True, ["apple", "banana", "orange"])
        )

    @patch("requests.request")
    def test_json_null(self, mock_request):
        mock_response = self.make_mock_response(200, b"null")
        mock_request.return_value = mock_response

        result = make_request("GET", self.url)

        self.assertEqual(result, (True,None))

    @patch("requests.request")
    def test_headers_forwarded(self, mock_request):
        mock_response = self.make_mock_response(
            200,
            b'{"success": true}'
        )
        mock_request.return_value = mock_response

        headers = {"Authorization": "Bearer test-token"}

        result = make_request(
            "GET",
            self.url,
            headers=headers
        )

        self.assertEqual(result, (True, {"success": True}))

        mock_request.assert_called_once_with(
            "GET",
            self.url,
            timeout=5,
            headers=headers
        )

    @patch("requests.request")
    def test_post_json(self, mock_request):
        mock_response = self.make_mock_response(
            201,
            b'{"id": 123, "name": "Douglas"}'
        )
        mock_request.return_value = mock_response

        payload = {"name": "Douglas"}

        result = make_request(
            "POST",
            self.url,
            json=payload
        )

        self.assertEqual(
            result,
            (True, {"id": 123, "name": "Douglas"})
        )

        mock_request.assert_called_once_with(
            "POST",
            self.url,
            timeout=5,
            json=payload
        )

    @patch("requests.request")
    def test_query_parameters(self, mock_request):
        mock_response = self.make_mock_response(
            200,
            b'{"id": 42, "name": "Douglas"}'
        )
        mock_request.return_value = mock_response

        params = {"id": 42}

        result = make_request(
            "GET",
            self.url,
            params=params
        )

        self.assertEqual(
            result,
            (True, {"id": 42, "name": "Douglas"})
        )

        mock_request.assert_called_once_with(
            "GET",
            self.url,
            timeout=5,
            params=params
        )
    @patch("requests.request")
    def test_custom_timeout(self, mock_request):
        mock_response = self.make_mock_response(
            200,
            b'{"id": 42, "name": "Douglas"}'
        )
        mock_request.return_value = mock_response

        params = {"id": 42}
        result = make_request(
            "GET",
            self.url,
            timeout=8,
            params=params
        )

        self.assertEqual(
            result,
            (True,{"id": 42, "name": "Douglas"})
        )

        mock_request.assert_called_once_with(
            "GET",
            self.url,
            timeout=8,
            params=params
        )

    @patch("requests.request")
    def test_server_error(self, mock_request):
        mock_response = self.make_mock_response(
            500,
            b'{"error": "Internal Server Error"}'
        )
        
        mock_request.return_value = mock_response

        output = StringIO()
        with redirect_stdout(output):
            result = make_request("GET", self.url)

        self.assertEqual(result, (False, None))
        self.assertEqual(
            output.getvalue().strip(),
            "HTTP error: 500"
        )

    @patch("requests.request")
    def test_timeout_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.Timeout(
                "Request timed out"
        )
    
        output = StringIO()
        with redirect_stdout(output):
            result = make_request("GET", self.url)

        self.assertEqual(result, (False, None))
        self.assertEqual(
            output.getvalue().strip(),
            "Request failed: Request timed out"
        )
        mock_request.assert_called_once_with(
            "GET",
            self.url,
            timeout=5
        )


if __name__ == "__main__":
    unittest.main()

