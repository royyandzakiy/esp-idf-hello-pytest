# hello_world/test/test_advanced_features.py

import pytest
import re
import time
import random
from datetime import datetime

# ---------- FIXTURES ----------
@pytest.fixture(scope="session")
def session_data():
    """Session-scoped fixture for data that persists across all tests"""
    return {"start_time": datetime.now(), "total_tests": 0}

@pytest.fixture(scope="function")
def test_counter():
    """Function-scoped fixture that counts test executions"""
    return {"executions": 0}

@pytest.fixture
def random_delay():
    """Fixture that introduces a random delay between 0.1-0.5 seconds"""
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)
    return delay

# ---------- PARAMETRIZED TESTS ----------
# @pytest.mark.parametrize("counter_value", [0, 2, 4])
# def test_parametrized_counter(dut, counter_value):
#     """Test different counter values using parametrization"""
#     dut.expect(f'Hello World! Counter: {counter_value}')

# @pytest.mark.parametrize("test_input,expected", [
#     ("Chip Info:", True),
#     ("Nonexistent Text", False)
# ])
# def test_parametrized_expectations(dut, test_input, expected):
#     """Test both positive and negative expectations"""
#     if expected:
#         dut.expect(test_input)
#     else:
#         # Verify the text doesn't appear within a short timeframe
#         try:
#             dut.expect(test_input, timeout=1)
#             assert False, f"Unexpectedly found: {test_input}"
#         except:
#             pass  # Expected behavior - text not found

# ---------- MARKERS AND SKIPPING TESTS ----------
@pytest.mark.slow
def test_slow_operation(dut):
    """Marked as slow - might take longer to execute"""
    time.sleep(2)
    dut.expect('Hello World!')

@pytest.mark.skip(reason="This test demonstrates skipping functionality")
def test_skipped_example(dut):
    """This test will be skipped with a reason"""
    assert False, "This should not execute"

@pytest.mark.xfail(reason="Expected to fail - demonstrates xfail marker")
def test_expected_failure(dut):
    """This test is expected to fail"""
    dut.expect('This text will never appear')  # This should fail

# ---------- TEST CLASSES ----------
class TestClassFeatures:
    """Demonstrating class-based testing"""
    
    @classmethod
    def setup_class(cls):
        """Class setup - runs once before all tests in this class"""
        cls.class_setup_time = datetime.now()
    
    def setup_method(self):
        """Method setup - runs before each test method"""
        self.method_setup_time = datetime.now()
    
    def test_class_based_test(self, dut):
        """Test within a class structure"""
        dut.expect('Hello World!')
        assert hasattr(self, 'method_setup_time')
        assert hasattr(self.__class__, 'class_setup_time')
    
    def test_another_class_test(self, dut):
        """Another test in the same class"""
        dut.expect('Chip Info:')

# ---------- ADVANCED ASSERTIONS ----------
def test_advanced_assertions(dut):
    """Demonstrating advanced assertion techniques"""
    # Capture multiple values with regex
    match = dut.expect(r'Free Heap: (\d+) bytes.*Minimum Free Heap: (\d+) bytes', timeout=5)
    free_heap, min_heap = int(match[1]), int(match[2])
    
    # Multiple assertions with custom messages
    assert free_heap > min_heap, f"Free heap ({free_heap}) should be greater than min heap ({min_heap})"
    assert min_heap > 50000, f"Min heap too small: {min_heap}"
    
    # Using pytest.approx for numerical comparisons (though not needed here)
    assert free_heap == pytest.approx(free_heap, rel=0.1)  # 10% relative tolerance

# ---------- EXCEPTION TESTING ----------
# def test_exception_handling(dut):
#     """Testing exception handling patterns"""
#     # Test that we can handle timeouts properly
#     start_time = time.time()
#     try:
#         dut.expect('ThisTextWillNeverAppear', timeout=2)
#         assert False, "Should have timed out"
#     except Exception as e:
#         # Verify it took approximately 2 seconds
#         duration = time.time() - start_time
#         assert 1.9 <= duration <= 2.5, f"Timeout duration incorrect: {duration}"
#         assert "Timeout" in str(e) or "timeout" in str(e).lower()

# ---------- FIXTURE USAGE DEMONSTRATION ----------
def test_fixture_usage(dut, session_data, test_counter, random_delay):
    """Demonstrating multiple fixture usage"""
    # Use session data
    session_data["total_tests"] += 1
    
    # Use test counter
    test_counter["executions"] += 1
    
    # Use random delay
    assert 0.1 <= random_delay <= 0.5
    
    # Actual test logic
    dut.expect('HELLO_WORLD: Running tests...')
    
    # Verify fixtures worked
    assert test_counter["executions"] == 1
    assert session_data["total_tests"] >= 1

# ---------- CUSTOM MARKERS ----------
@pytest.mark.hardware_dependent
def test_hardware_dependent_features(dut):
    """Marked as hardware dependent - might behave differently on different hardware"""
    # This test might need adjustment for different ESP32 variants
    dut.expect('Model: esp32s3')

@pytest.mark.performance
def test_performance_metrics(dut):
    """Performance-related testing"""
    start_time = time.time()
    dut.expect('Hello World! Counter: 0')
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response_time < 5.0, f"Response too slow: {response_time} seconds"

# ---------- TEST CONFIGURATION ----------
def test_configuration_dependent(dut, pytestconfig):
    """Test that uses pytest configuration"""
    # Access pytest configuration
    verbose = pytestconfig.getoption("verbose")
    if verbose > 0:
        print(f"Running in verbose mode (level {verbose})")
    
    # Test logic
    dut.expect('Restarting now.')

# ---------- DYNAMIC TEST GENERATION ----------
# Generate tests dynamically based on some condition
for i in range(3):
    def make_test(number):
        def test_dynamic(dut):
            dut.expect(f'Hello World! Counter: {number}')
        return test_dynamic
    
    # Create dynamic test functions
    globals()[f'test_dynamic_{i}'] = make_test(i)

# ---------- HOOKS (would typically be in conftest.py) ----------
# Note: These are just shown here for demonstration
# In practice, they would be in a conftest.py file

def pytest_configure(config):
    """Pytest configuration hook"""
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "hardware_dependent: mark test as hardware dependent"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance related"
    )

def pytest_collection_modifyitems(items):
    """Modify test collection"""
    for item in items:
        if "advanced" in item.nodeid:
            item.add_marker(pytest.mark.advanced)