import pytest
from notes21 import __version__

def test_version():
    assert __version__ == "0.1.0"

def test_imports():
    try:
        import music21
        import numpy
    except ImportError:
        pytest.fail("Core dependencies (music21, numpy) failed to import")
