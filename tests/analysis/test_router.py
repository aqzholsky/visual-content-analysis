import os
from io import BytesIO
from unittest.mock import AsyncMock

import pytest


class TestAnalysis:
    @pytest.fixture
    def request_id(self, faker):
        return faker.uuid4()

    @pytest.fixture
    def detail_url(self, analysis_url, request_id):
        return f"{analysis_url}/{request_id}"

    @pytest.fixture
    def setup_file(self, request_id):
        os.makedirs("result_files", exist_ok=True)
        file_path = f"result_files/result_{request_id}.json"
        with open(file_path, "w") as file:
            file.write('{"key": "value"}')
        return file_path

    class TestGetAnalysis:

        @pytest.mark.usefixtures("setup_file")
        def test_get_analysis(self, test_client, detail_url):
            response = test_client.get(detail_url)
            assert response.status_code == 200
            assert response.json() == {"key": "value"}

        def test_get_analysis_not_found(self, test_client, detail_url):
            response = test_client.get(detail_url)
            assert response.status_code == 404
            assert response.json() == {"detail": "Analysis not found"}

    class TestDeleteAnalysis:

        @pytest.mark.usefixtures("setup_file")
        def test_delete_analysis(self, test_client, detail_url):
            response = test_client.delete(detail_url)
            assert response.status_code == 200

        def test_delete_analysis_not_found(self, test_client, detail_url):
            response = test_client.delete(detail_url)
            assert response.status_code == 404
            assert response.json() == {"detail": "Analysis not found"}

    def test_upload_file(self, test_client, mocker, faker, analysis_url):
        mock_analyze_content = mocker.patch(
            "src.analysis.router.analyze_content", new_callable=AsyncMock
        )

        file_name = faker.file_name()
        file = BytesIO(b"content")
        file.name = file_name

        response = test_client.post(
            analysis_url, files={"file": (file.name, file, "text/plain")}
        )
        assert response.status_code == 201
        assert "request_id" in response.json()
        mock_analyze_content.assert_called_once()
