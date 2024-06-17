import json
import os
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator

import cv2
import ffmpeg
import numpy as np
import onnxruntime as rt

from src.config import LABELS_MAP_PATH, ONNX_MODEL_NAME

from .constants import ANALYSIS_ACCURACY
from .utils import construct_result_file_path


class AbstractFrameAnalysis(ABC):
    def __init__(self) -> None:
        self.session = rt.InferenceSession(
            f"{ONNX_MODEL_NAME}", providers=["CPUExecutionProvider"]
        )
        self.labels = json.load(open(LABELS_MAP_PATH, "r"))

    @abstractmethod
    def analyze(self, file: str) -> list:
        pass

    def analyze_frame(self, frame: np.ndarray, order: int):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = self.pre_process_edgetpu(img, (224, 224, 3))
        img = np.expand_dims(img, axis=0)

        analyze_results = self.session.run(["Softmax:0"], {"images:0": img})[0]
        analyze_result = reversed(analyze_results[0].argsort()[-5:])

        classes = []
        for i in analyze_result:
            probability = round(analyze_results[0][i], 2)
            if probability >= ANALYSIS_ACCURACY:
                class_name = self.labels[str(i)]
                classes.append(
                    {
                        "probability": str(probability),
                        "class_name": class_name,
                    }
                )

        return {
            "frame": order,
            "classes": classes,
        }

    @classmethod
    def pre_process_edgetpu(cls, img, dims):
        output_height, output_width, _ = dims
        img = cls.resize_with_aspectratio(
            img, output_height, output_width, inter_pol=cv2.INTER_LINEAR
        )
        img = cls.center_crop(img, output_height, output_width)
        img = np.asarray(img, dtype="float32")
        img -= [127.0, 127.0, 127.0]
        img /= [128.0, 128.0, 128.0]
        return img

    @staticmethod
    def resize_with_aspectratio(
        img, out_height, out_width, scale=87.5, inter_pol=cv2.INTER_LINEAR
    ):
        height, width, _ = img.shape
        new_height = int(100.0 * out_height / scale)
        new_width = int(100.0 * out_width / scale)
        if height > width:
            w = new_width
            h = int(new_height * height / width)
        else:
            h = new_height
            w = int(new_width * width / height)
        img = cv2.resize(img, (w, h), interpolation=inter_pol)
        return img

    @staticmethod
    def center_crop(img, out_height, out_width):
        height, width, _ = img.shape
        left = int((width - out_width) / 2)
        right = int((width + out_width) / 2)
        top = int((height - out_height) / 2)
        bottom = int((height + out_height) / 2)
        img = img[top:bottom, left:right]
        return img


class PhotoAnalysis(AbstractFrameAnalysis):
    def analyze(self, file: str) -> list:
        frame = cv2.imread(file)
        result = self.analyze_frame(frame, 1)
        return [result]


class VideoAnalysis(AbstractFrameAnalysis):
    def analyze(self, file: str) -> list:
        results = []

        frames = self.extract_frames(file)
        for i, frame in enumerate(frames, start=1):
            result = self.analyze_frame(frame, i)
            results.append(result)

        return results

    def extract_frames(self, file: str) -> Generator:
        with tempfile.TemporaryDirectory() as temp_dir:
            (
                ffmpeg.input(file)
                .filter("fps", fps=1)
                .output(os.path.join(temp_dir, "frame_%04d.png"))
                .run(capture_stdout=True, capture_stderr=True)
            )

            for file in sorted(
                [
                    os.path.join(temp_dir, f)
                    for f in os.listdir(temp_dir)
                    if f.startswith("frame_") and f.endswith(".png")
                ]
            ):
                yield cv2.imread(file)


class ContentAnalyzer:
    def __init__(self, strategy: AbstractFrameAnalysis):
        self._strategy = strategy

    def set_strategy(self, strategy: AbstractFrameAnalysis):
        self._strategy = strategy

    def analyze(self, content):
        return self._strategy.analyze(content)


def analyze_content(file_location, request_id):
    content_extension = os.path.splitext(file_location)[1]

    if content_extension in [
        ".jpg",
        ".png",
        ".jpeg",
    ]:
        strategy = PhotoAnalysis()
    elif content_extension in [".mp4", ".avi", ".mov"]:
        strategy = VideoAnalysis()
    else:
        raise ValueError("Unsupported content type")

    analyzer = ContentAnalyzer(strategy)
    content_results = analyzer.analyze(file_location)

    file_content = {
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "results": content_results,
    }

    file_path = construct_result_file_path(request_id)
    with open(file_path, "w") as f:
        json.dump(file_content, f, indent=4)
