# ESP32 Hello World with Pytest Testing

A comprehensive example demonstrating how to use pytest for testing ESP32 applications with ESP-IDF framework. This project serves as a reference for embedded testing patterns and pytest configuration.

## 📋 Project Overview

This project demonstrates:
- Basic ESP32 application with system info, GPIO control, and memory operations
- Comprehensive pytest test suite for embedded applications
- Proper test configuration for ESP-IDF projects
- Testing patterns for hardware-dependent code

## 🏗️ Project Structure

```
hello_world/
├── main/
│   └── hello_world.c          # Main ESP32 application
├── test/
│   └── test_hello_world.py    # Pytest test suite
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Features

### ESP32 Application Features
- **System Information**: Displays chip model, cores, revision, and memory stats
- **GPIO Control**: LED blinking functionality using built-in GPIO
- **Memory Testing**: Dynamic memory allocation testing
- **Logging**: ESP_LOG integration with different log levels
- **Auto-restart**: Automatic restart cycle after completion

### Test Coverage
- Basic functionality verification
- System information validation
- Memory allocation testing
- GPIO operations testing
- Log message verification
- Restart sequence testing
- Memory bounds checking
- Multi-cycle testing

## 🛠️ Setup & Installation

### Prerequisites
- ESP-IDF framework installed and configured
- Python 3.7+ with pip
- ESP32 development board

### Installation Steps

1. **Clone or create the project structure**
   ```bash
   mkdir esp32_pytest_example
   cd esp32_pytest_example
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```cmd
   .venv\Scripts\activate
   ```
   
   **Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📝 Configuration Files

### pytest.ini
```ini
[pytest]
addopts = --embedded-services esp,idf -s -v
testpaths = test/
python_files = test_*.py
python_classes = Test*
python_functions = test_*

[tools]
; Additional configuration for ESP-IDF testing

[env]
IDF_TARGET = esp32
```

### requirements.txt
```txt
pytest
pytest-embedded
pytest-embedded-serial
pytest-embedded-idf
```

## 🧪 Running Tests

### Basic Test Execution
```bash
pytest
```

### Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest test/test_hello_world.py
```

### Run Specific Test Function
```bash
pytest test/test_hello_world.py::test_hello_world
```

### Run with Live Output
```bash
pytest -s
```

## 📊 Test Categories

### 1. Basic Functionality Tests
- `test_hello_world()`: Verifies main counter functionality
- `test_multiple_cycles()`: Tests application cycles

### 2. System Information Tests
- `test_system_info()`: Validates chip information display
- `test_heap_memory()`: Checks memory values are within expected ranges

### 3. Hardware Tests
- `test_gpio_functionality()`: Verifies GPIO operations through logs
- `test_memory_allocation()`: Tests dynamic memory allocation

### 4. Logging Tests
- `test_log_messages()`: Validates ESP_LOG output
- `test_restart_sequence()`: Tests proper application restart

## 🔧 Key Testing Patterns

### Device Under Test (DUT) Pattern
```python
def test_hello_world(dut):
    """Test basic hello world functionality"""
    dut.expect('Hello World! Counter: 0')
    dut.expect('Hello World! Counter: 4')
```

### Regular Expression Matching
```python
def test_heap_memory(dut):
    """Test heap memory values are reasonable"""
    heap_info = dut.expect(r'Free Heap: (\d+) bytes')[1]
    heap_size = int(heap_info)
    assert heap_size > 100000, f"Heap size too low: {heap_size}"
```

### Timing-Sensitive Tests
```python
def test_restart_sequence(dut):
    """Test proper restart sequence"""
    dut.expect('Restarting now.')
    time.sleep(3)  # Wait for restart
    dut.expect('=== ESP32 Hello World Application ===')
```

## 🎯 Best Practices Demonstrated

1. **Clear Test Organization**: Tests grouped by functionality
2. **Descriptive Test Names**: Each test clearly states its purpose
3. **Proper Assertions**: Using both expect() and assert statements
4. **Error Handling**: Meaningful error messages with actual values
5. **Hardware Abstraction**: Testing hardware functionality through logs
6. **Timing Considerations**: Proper delays for hardware operations

## 🔍 ESP32 Application Details

### Key Components
- **NVS Flash Initialization**: Proper flash memory setup
- **System Info Display**: Comprehensive chip information
- **GPIO Configuration**: LED control with proper pin setup
- **Memory Management**: Dynamic allocation testing
- **FreeRTOS Integration**: Task delays and system calls

### Hardware Requirements
- ESP32 development board
- Built-in LED on GPIO 2 (or modify `BLINK_GPIO` definition)

## 🚨 Common Issues & Solutions

### Test Timeout Issues
- Increase timeout values in pytest configuration
- Check serial connection and baud rate

### GPIO Test Failures
- Verify correct GPIO pin assignment
- Check hardware connections

### Memory Test Failures
- Adjust memory thresholds based on your ESP32 variant
- Consider available heap size variations

## 📚 Learning Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-embedded documentation](https://github.com/espressif/pytest-embedded)
- [ESP-IDF Testing Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/unit-tests.html)

## 🤝 Contributing

Feel free to extend this example with additional test patterns or ESP32 features. Common additions might include:
- WiFi connectivity tests
- I2C/SPI communication tests
- Deep sleep functionality tests
- OTA update tests

## 📄 License

This project is provided as-is for educational and reference purposes.