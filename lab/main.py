import machine
import ssd1306
import time
import micropython

# Allocate memory for exception tracebacks in ISRs
micropython.alloc_emergency_exception_buf(100)


# Hardware Initialization
i2c = machine.I2C(1)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

uart5 = machine.UART(5, baudrate=115200)
rtc = machine.RTC()

led_red = machine.Pin("C13", machine.Pin.OUT)
led_red.on()

uart_buffer = ""


def process_bluetooth_data(_):
    global uart_buffer

    while uart5.any():
        try:
            uart_buffer += uart5.read().decode("utf-8")
        except UnicodeError:
            pass

        if len(uart_buffer) > 64:
            uart_buffer = uart_buffer[-64:]

        if "\n" in uart_buffer:
            parts = uart_buffer.split("\n")

            for i in range(len(parts) - 1):
                time_str = parts[i].strip()
                date_str = parts[i + 1].strip()

                t_split = time_str.split(":")
                d_split = date_str.split(":")

                if len(t_split) == 3 and len(d_split) == 3:
                    try:
                        hh, mm, ss = int(t_split[0]), int(t_split[1]), int(t_split[2])
                        dd, mo, yyyy = int(d_split[0]), int(d_split[1]), int(d_split[2])

                        rtc.datetime((yyyy, mo, dd, 0, hh, mm, ss, 0))
                        uart_buffer = ""

                        # Flash LED
                        led_red.off()  # ON
                        time.sleep(0.1)
                        led_red.on()  # OFF

                        print(f"RTC Synced to: {hh}:{mm}:{ss} on {dd}/{mo}/{yyyy}")

                    except ValueError:
                        continue


# 3. Interrupt Service Routine
def uart_rx_isr(uart):
    """
    Hardware IRQ callback. NO MEMORY ALLOCATION ALLOWED.
    We schedule the processing function to run safely.
    """
    try:
        # Schedule the parser to run in the main thread.
        # The '0' is just a dummy argument required by the schedule function.
        micropython.schedule(process_bluetooth_data, 0)
    except RuntimeError:
        pass


def main():
    # Attach the Interrupt
    uart5.irq(handler=uart_rx_isr, trigger=machine.UART.IRQ_RXIDLE)

    oled.fill(0)
    oled.text("Waiting for", 0, 20)
    oled.text("Bluetooth Sync...", 0, 32)
    oled.show()

    while True:
        dt = rtc.datetime()
        yyyy, mo, dd, wd, hh, mm, ss, subsec = dt

        oled.fill(0)
        oled.text("Time (RTC):", 0, 0)
        oled.text(f"{hh:02d}:{mm:02d}:{ss:02d}", 0, 16)
        oled.text("Date:", 0, 36)
        oled.text(f"{dd:02d}/{mo:02d}/{yyyy}", 0, 52)
        oled.show()

        time.sleep(0.1)
