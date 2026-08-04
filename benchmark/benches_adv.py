import machine
import time
import gc
import math
import struct


def header(title):
    print("\n" + "=" * 5)
    print(title)
    print("=" * 5)


def test_gpio_speed():
    header("1. GPIO Toggle Speed (CPU Bound)")
    # Using PA0 to avoid burning out the onboard LEDs
    try:
        pin = machine.Pin("A0", machine.Pin.OUT)
    except ValueError:
        print("Pin A0 not available, skipping.")
        return

    gc.collect()
    N = 100000
    pin.off()

    t0 = time.ticks_us()
    for _ in range(N):
        pin.on()
        pin.off()
    t1 = time.ticks_us()

    dt_us = time.ticks_diff(t1, t0)
    freq_hz = (N * 1000000) / dt_us

    print(f"Iterations: {N}")
    print(f"Time taken: {dt_us} us")
    print(f"Estimated Output Frequency: {freq_hz:.0f} Hz")
    print(
        "-> Note: This measures the VM overhead of fetching the 'on'/'off' attributes and executing the bytecode loop."
    )


def test_math_kinematics():
    header("2. Math Overhead: Direct Euler Angles (RPY)")
    # A standard control loop calculating Roll, Pitch, Yaw from raw sensor data
    # explicitly bypassing quaternions entirely.
    gc.collect()

    N = 1000
    # Dummy simulated acceleration vectors
    ax, ay, az = 0.5, -0.2, 0.866

    t0 = time.ticks_us()
    for _ in range(N):
        # Calculate Roll and Pitch directly
        _roll = math.atan2(ay, az)
        _pitch = math.atan2(-ax, math.sqrt(ay * ay + az * az))
        # Simulated yaw integration
        _yaw = 0.1 * 0.01
    t1 = time.ticks_us()

    dt_us = time.ticks_diff(t1, t0)
    time_per_loop = dt_us / N

    print(f"Iterations: {N} RPY calculations")
    print(f"Time taken: {dt_us} us")
    print(f"Time per calculation: {time_per_loop:.2f} us")


def test_memory_and_formatting():
    header("3. Memory Allocation & String Formatting (BMS Simulation)")
    # Simulating parsing resistor-based voltage outputs for cell balancing
    gc.collect()
    initial_free = gc.mem_free()

    N = 5000
    dummy_voltages = [3.2, 3.5, 4.1, 3.8] * 4  # 16 cells

    t0 = time.ticks_us()
    for _ in range(N):
        # This forces string allocations in the heap
        _log_str = ",".join(["{:.2f}".format(v) for v in dummy_voltages])
    t1 = time.ticks_us()

    dt_us = time.ticks_diff(t1, t0)
    final_free = gc.mem_free()

    print(f"Iterations: {N} format cycles")
    print(f"Time taken: {dt_us} us")
    print(f"Heap before: {initial_free} B, Heap after (before GC): {final_free} B")


def test_struct_packing():
    header("4. Array Packing Speed")
    gc.collect()

    N = 5000
    static_bytes = struct.pack("<IIII", 100, 200, 300, 400)
    buf = bytearray(16)

    t0 = time.ticks_us()
    for i in range(N):
        buf[:] = static_bytes
    t1 = time.ticks_us()

    dt_us = time.ticks_diff(t1, t0)

    print(f"Iterations: {N} struct packing cycles")
    print(f"Time taken: {dt_us} us")


def test_gpio_optimized_register_access():
    header("5. GPIO Toggle Speed on direct register access optimized")
    m32 = machine.mem32
    bsrr = 0x50000018
    brr = 0x50000028
    pin0 = 1 << 0

    N = 100000
    t0 = time.ticks_us()

    for _ in range(N):
        m32[bsrr] = pin0
        m32[brr] = pin0

    t1 = time.ticks_us()

    dt_us = time.ticks_diff(t1, t0)
    freq_hz = (N * 1000000) / dt_us
    print(f"Iterations: {N}")
    print(f"Time taken: {dt_us} us")
    print(f"Estimated Output Frequency: {freq_hz:.0f} Hz")


def test_gpio_register_access():
    header("6. GPIO Toggle Speed on direct register access")
    bsrr = 0x50000018
    brr = 0x50000028
    pin0 = 1 << 0

    N = 100000
    t0 = time.ticks_us()

    for _ in range(N):
        machine.mem32[bsrr] = pin0
        machine.mem32[brr] = pin0

    t1 = time.ticks_us()

    dt_us = time.ticks_diff(t1, t0)
    freq_hz = (N * 1000000) / dt_us
    print(f"Iterations: {N}")
    print(f"Time taken: {dt_us} us")
    print(f"Estimated Output Frequency: {freq_hz:.0f} Hz")


def run_all():
    print("Starting MicroPython Benchmarks on STM32G0B1...")
    test_gpio_speed()
    time.sleep(0.1)
    test_math_kinematics()
    time.sleep(0.1)
    test_memory_and_formatting()
    time.sleep(0.1)
    test_struct_packing()
    time.sleep(0.1)
    test_gpio_optimized_register_access()
    time.sleep(0.1)
    test_gpio_register_access()


if __name__ == "__main__":
    run_all()
