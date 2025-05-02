import unittest
from unittest.mock import patch, Mock
from etl.ingestion.ingestion import fetch_api_data
from pathlib import Path
import requests

class TestFetchAPIData(unittest.TestCase):
    OUTPUT_SUBDIR = "etl/tests/storage/ingestion"

    @patch("etl.ingestion.ingestion.requests.get")
    def test_fetch_successful(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "incident": "fire"}]
        mock_get.return_value = mock_response

        output_dir = Path(self.OUTPUT_SUBDIR)
        json_files_before = set(output_dir.glob("*.json"))

        # Act
        fetch_api_data("http://fake.api/fire", output_subdir=self.OUTPUT_SUBDIR)

        # Assert
        json_files_after = set(output_dir.glob("*.json"))
        new_files = json_files_after - json_files_before
        self.assertTrue(len(new_files) == 1)

        # Clean up
        for file in new_files:
            file.unlink()

    @patch("etl.ingestion.ingestion.requests.get")
    def test_fetch_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = fetch_api_data("http://fake.api/fire", output_subdir=self.OUTPUT_SUBDIR)
        self.assertIsNone(result)

    @patch("etl.ingestion.ingestion.requests.get")
    def test_fetch_empty_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = fetch_api_data("http://fake.api/fire", output_subdir=self.OUTPUT_SUBDIR)
        self.assertIsNone(result)

    @patch("etl.ingestion.ingestion.requests.get")
    def test_fetch_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        try:
            fetch_api_data("http://fake.api/fire", output_subdir=self.OUTPUT_SUBDIR)
        except Exception as e:
            self.fail(f"fetch_api_data raised an unexpected exception: {e}")

if __name__ == "__main__":
    unittest.main()
