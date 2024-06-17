import os
import shutil

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from src.analysis.constants import RESULT_FILE_DIR, UPLOAD_FILE_DIR
from src.main import app


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def analysis_url():
    return "/analysis"


@pytest.fixture(scope="module", autouse=True)
def clear_dirs():
    yield
    for directory in [UPLOAD_FILE_DIR, RESULT_FILE_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
