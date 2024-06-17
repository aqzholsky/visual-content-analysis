import json

import pytest
from freezegun import freeze_time

from src.analysis.service import PhotoAnalysis, VideoAnalysis, analyze_content


@pytest.fixture(autouse=True)
def mock_inference_session(mocker):
    return mocker.patch("src.analysis.service.rt.InferenceSession")


@pytest.fixture(autouse=True)
def mock_labels_map_path(mocker, tmpdir):
    file = tmpdir.join("labels_map.json")
    file.write('{"a": "b"}')
    mocker.patch("src.analysis.service.LABELS_MAP_PATH", str(file))


def test_video_analysis(mocker):
    file = "file"
    service = VideoAnalysis()
    mock_extract_frames = mocker.patch.object(
        service, "extract_frames", return_value=[1]
    )
    mock_analyze_frame = mocker.patch.object(
        service, "analyze_frame", return_value="result"
    )

    service.analyze(file)

    mock_extract_frames.assert_called_once_with(file)
    mock_analyze_frame.assert_called_once_with(1, 1)


def test_photo_analysis(mocker):
    file = "file"
    service = PhotoAnalysis()
    mock_analyze_frame = mocker.patch.object(
        service, "analyze_frame", return_value="result"
    )

    service.analyze(file)

    mock_analyze_frame.assert_called_once()


class TestAnalyzeContent:
    @pytest.mark.parametrize(
        "file, strategy",
        [
            ("content.jpg", PhotoAnalysis),
            ("file.png", PhotoAnalysis),
            ("file.jpeg", PhotoAnalysis),
            ("file.mp4", VideoAnalysis),
            ("file.avi", VideoAnalysis),
            ("file.mov", VideoAnalysis),
        ],
    )
    @freeze_time("2024-06-17 21:00:15.201309")
    def test(self, mocker, file, strategy, faker, tmpdir):
        file_path = str(tmpdir.join(file))
        mocker.patch(
            "src.analysis.service.construct_result_file_path",
            return_value=file_path,
        )

        request_id = faker.uuid4()
        mock_analyze = mocker.patch.object(
            strategy,
            "analyze",
            return_value={"a": "b"},
        )

        analyze_content(file, request_id)

        mock_analyze.assert_called_once_with(file)
        with open(file_path) as f:
            assert json.load(f) == {
                "request_id": request_id,
                "timestamp": "2024-06-17T21:00:15.201309",
                "results": {"a": "b"},
            }

    def test_unsupported_content_type(self, faker):
        with pytest.raises(ValueError, match="Unsupported content type"):
            analyze_content("file.unsupported_extension", faker.uuid4())
