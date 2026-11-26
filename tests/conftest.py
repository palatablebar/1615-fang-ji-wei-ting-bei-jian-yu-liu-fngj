from pathlib import Path
import pytest

from loomreserve.settings import SAMPLE_NAME
from loomreserve.repair_followups.contracts import Windows
from loomreserve.loom_checklists.service import inspect_feed
from loomreserve.process import prepare_batch


@pytest.fixture(scope='session')
def source_bytes() -> bytes:
    root = Path(__file__).resolve().parent.parent
    return (root/'sample_data'/SAMPLE_NAME).read_bytes()


@pytest.fixture(scope='session')
def source(source_bytes):
    return inspect_feed(source_bytes)


@pytest.fixture(scope='session')
def prepared(source_bytes):
    return prepare_batch(source_bytes,Windows())
