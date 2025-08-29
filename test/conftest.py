# hello_world/test/conftest.py

import pytest

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption("--stress", action="store_true", help="Run stress tests")
    parser.addoption("--hardware", action="store", default="esp32s3", 
                    help="Target hardware platform")

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "stress: mark test as stress test (run with --stress)"
    )
    config.addinivalue_line(
        "markers", "hardware_dependent: mark test as hardware dependent"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options"""
    if not config.getoption("--stress"):
        skip_stress = pytest.mark.skip(reason="need --stress option to run")
        for item in items:
            if "stress" in item.keywords:
                item.add_marker(skip_stress)