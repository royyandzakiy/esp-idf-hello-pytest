# hello_world/test/test_hello_world.py

import pytest
import re
import time

def test_hello_world(dut):
    """Test basic hello world functionality"""
    dut.expect('Hello World! Counter: 0')
    dut.expect('Hello World! Counter: 4')

def test_system_info(dut):
    """Test system information output"""
    dut.expect('Chip Info:')
    dut.expect('Model: esp32s3')
    dut.expect('Cores: 2')  # Most ESP32 have 2 cores
    dut.expect('Free Heap:')

def test_memory_allocation(dut):
    """Test memory allocation functionality"""
    dut.expect('Memory allocation test passed')

def test_gpio_functionality(dut):
    """Test GPIO operations (indirectly through logs)"""
    dut.expect('GPIO test completed')

def test_log_messages(dut):
    """Test ESP_LOG messages"""
    dut.expect('HELLO_WORLD: Running tests...')
    dut.expect('HELLO_WORLD: Log message - Counter:')

def test_restart_sequence(dut):
    """Test proper restart sequence"""
    dut.expect('Restarting now.')
    # After restart, we should see the initialization again
    time.sleep(3)  # Wait for restart
    dut.expect('=== ESP32 Hello World Application ===')

def test_heap_memory(dut):
    """Test heap memory values are reasonable"""
    heap_info = dut.expect(r'Free Heap: (\d+) bytes')[1]
    heap_size = int(heap_info)
    assert heap_size > 100000, f"Heap size too low: {heap_size}"
    
    min_heap = dut.expect(r'Minimum Free Heap: (\d+) bytes')[1]
    min_heap_size = int(min_heap)
    assert min_heap_size > 80000, f"Minimum heap size too low: {min_heap_size}"

def test_multiple_cycles(dut):
    """Test multiple cycles of the application"""
    for i in range(3):
        dut.expect(f'Hello World! Counter: {i}')
    dut.expect('Restarting now.')