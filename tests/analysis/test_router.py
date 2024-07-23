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

    class TestGetAnalysis:
        @pytest.fixture
        def analysis_results(self):
            return {
                "request_id": "123",
                "timestamp": "2021-01-01T00:00:00",
                "results": [],
            }

        def test_get_analysis(self, test_client, detail_url, analysis_results, mocker):
            mocker.patch(
                "src.analysis.router.get_analysis_by_request_id",
                new_callable=AsyncMock,
                return_value=analysis_results,
            )
            response = test_client.get(detail_url)
            assert response.status_code == 200
            assert response.json() == {
                "request_id": "123",
                "timestamp": "2021-01-01T00:00:00",
                "results": [],
            }

        def test_get_analysis_not_found(self, test_client, detail_url, mocker):
            mocker.patch(
                "src.analysis.router.get_analysis_by_request_id",
                new_callable=AsyncMock,
                return_value=None,
            )
            response = test_client.get(detail_url)
            assert response.status_code == 404
            assert response.json() == {"detail": "Analysis not found"}

    class TestDeleteAnalysis:

        @pytest.fixture(autouse=True)
        def mock_delete_analysis_result(self, mocker):
            return mocker.patch(
                "src.analysis.router.delete_analysis_result",
                new_callable=AsyncMock,
                return_value=True,
            )

        def test_delete_analysis(
            self, test_client, detail_url, mocker, mock_delete_analysis_result
        ):
            mocker.patch(
                "src.analysis.router.is_analysis_exists",
                new_callable=AsyncMock,
                return_value=True,
            )
            response = test_client.delete(detail_url)
            assert response.status_code == 200
            mock_delete_analysis_result.assert_called_once()

        def test_delete_analysis_not_found(
            self, test_client, detail_url, mock_delete_analysis_result, mocker
        ):
            mocker.patch(
                "src.analysis.router.is_analysis_exists",
                new_callable=AsyncMock,
                return_value=False,
            )
            response = test_client.delete(detail_url)
            assert response.status_code == 404
            assert response.json() == {"detail": "Analysis not found"}
            mock_delete_analysis_result.assert_not_called()

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
