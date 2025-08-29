# hello_world/test_hello_world.py

def test_hello_arduino(dut):
    dut.expect('Hello World!')