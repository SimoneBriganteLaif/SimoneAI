from pathlib import Path

import pytest

from parser.extractor import extract_model
from parser.ir import TableIR


@pytest.fixture
def sample_model_path() -> Path:
    return Path(__file__).parent / "fixtures" / "sample_model.py"


@pytest.fixture
def sample_model_source(sample_model_path: Path) -> str:
    return sample_model_path.read_text()


@pytest.fixture
def parsed_tables(sample_model_source: str) -> list[TableIR]:
    return extract_model(sample_model_source)
