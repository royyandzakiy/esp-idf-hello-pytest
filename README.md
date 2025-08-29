# ESP32S3 Hello World with Pytest Testing

A comprehensive example demonstrating pytest for ESP32S3 applications with ESP-IDF framework. Includes basic and advanced testing patterns for embedded development.

## Project Structure

```
hello_world/
├── main/
│   └── hello_world.c          # Main ESP32S3 application
├── test/
│   ├── test_hello_world.py    # Basic test suite
│   ├── test_advanced_features.py # Advanced pytest patterns
│   └── conftest.py            # Pytest configuration and fixtures
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

### ESP32S3 Application
- System information display (chip model, cores, memory stats)
- GPIO LED control with built-in LED
- Memory allocation testing
- ESP_LOG integration
- Test pattern generation
- Automatic restart cycle

### Test Coverage

| Category | Test Function | Description |
|----------|---------------|-------------|
| **Basic** | `test_hello_world` | Counter functionality |
| | `test_system_info` | Chip information validation |
| | `test_memory_allocation` | Memory operations |
| | `test_gpio_functionality` | GPIO operations via logs |
| | `test_log_messages` | ESP_LOG message verification |
| | `test_restart_sequence` | Application restart cycle |
| | `test_heap_memory` | Memory bounds checking |
| | `test_multiple_cycles` | Multi-cycle execution |
| **Advanced** | `test_slow_operation` | Long-running operations |
| | `test_advanced_assertions` | Complex regex matching |
| | `test_fixture_usage` | Multiple fixture demonstration |
| | `test_performance_metrics` | Response time validation |
| | `test_configuration_dependent` | Config-based testing |

## Getting Started

```shell
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

pytest

clang-format -i main/hello_world.c
```

## Configuration

### pytest.ini
```ini
[pytest]
addopts = --embedded-services esp,idf -s -v
testpaths = test/
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: mark test as slow running
    hardware_dependent: mark test as hardware dependent
    performance: mark test as performance related
    stress: stress tests (run with --stress)
    advanced: advanced feature tests
    
[tools]
; Additional configuration for ESP-IDF testing

[env]
IDF_TARGET = esp32s3
```

### requirements.txt
```txt
pytest
pytest-embedded
pytest-embedded-serial
pytest-embedded-idf
...
```

## Running Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest test/test_hello_world.py

# Specific test function
pytest test/test_hello_world.py::test_hello_world

# Run with markers
pytest -m "not slow"
pytest -m "performance"

# Run stress tests
pytest --stress

# Custom hardware target
pytest --hardware esp32s3
```

## Advanced Testing Patterns

### Fixtures
- **Session-scoped**: Data persists across all tests
- **Function-scoped**: Per-test execution counters
- **Custom fixtures**: Random delays, configuration data

### Markers and Skipping
- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.skip` - Skip with reason
- `@pytest.mark.xfail` - Expected failures
- `@pytest.mark.hardware_dependent` - Hardware-specific tests

### Test Classes
```python
class TestClassFeatures:
    @classmethod
    def setup_class(cls):
        # Runs once before all tests in class
        
    def setup_method(self):
        # Runs before each test method
```

### Advanced Assertions
```python
# Regex with multiple captures
match = dut.expect(r'Free Heap: (\d+) bytes.*Minimum Free Heap: (\d+) bytes')
free_heap, min_heap = int(match[1]), int(match[2])

# Custom error messages
assert free_heap > min_heap, f"Free heap ({free_heap}) should be greater than min heap ({min_heap})"

# Numerical comparisons with tolerance
assert value == pytest.approx(expected, rel=0.1)
```

### Dynamic Test Generation
```python
# Generate tests programmatically
for i in range(3):
    def make_test(number):
        def test_dynamic(dut):
            dut.expect(f'Hello World! Counter: {number}')
        return test_dynamic
    
    globals()[f'test_dynamic_{i}'] = make_test(i)
```

## Key Testing Patterns

### Device Under Test (DUT)
```python
def test_example(dut):
    dut.expect('Expected output')
    dut.expect(r'Regex pattern: (\d+)', timeout=5)
```

### Timing-Sensitive Tests
```python
def test_restart_sequence(dut):
    dut.expect('Restarting now.')
    time.sleep(3)  # Wait for restart
    dut.expect('=== ESP32 Hello World Application ===')
```

### Exception Handling
```python
try:
    dut.expect('NonexistentText', timeout=2)
    assert False, "Should have timed out"
except Exception as e:
    assert "timeout" in str(e).lower()
```

## Hardware Requirements
- ESP32S3 development board
- Built-in LED on GPIO 2
- USB connection for serial communication

## Common Issues

| Issue | Solution |
|-------|----------|
| Test timeouts | Increase timeout values, check serial connection |
| GPIO failures | Verify pin assignment, check hardware |
| Memory test failures | Adjust thresholds for ESP32S3 variant |
| Marker not recognized | Add marker to pytest.ini configuration |

## Best Practices

- Use descriptive test names and docstrings
- Group related tests in classes
- Implement proper setup/teardown with fixtures
- Handle timing-sensitive operations appropriately
- Use markers to categorize tests
- Implement meaningful error messages with actual values
- Test hardware functionality through observable outputs

## Learning Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-embedded documentation](https://github.com/espressif/pytest-embedded)
- [ESP-IDF Testing Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/unit-tests.html)