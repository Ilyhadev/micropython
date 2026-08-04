# MINI_NODE_V3 RTC Bluetooth Sync

This project synchronizes the hardware RTC of the **STM32G0B1CE** using time data received via Bluetooth (USART5) and renders a real-time clock on an **SSD1306 OLED** display.

---

## Key Features
*   **Interrupt-Driven RX**: Uses `UART.IRQ_RXIDLE` to trigger data processing immediately upon packet completion.
*   **Thread-Safe Parsing**: Leverages `micropython.schedule` to handle string decoding and RTC updates outside of the hardware interrupt context, preventing memory allocation errors.
*   **Visual Feedback**: The Red LED (Pin C13) flashes briefly upon a successful time synchronization.
*   **Robust Buffering**: Implements a sliding window buffer to handle fragmented Bluetooth serial packets.

---

## Hardware Configuration

| Component | Pins | Notes |
| :--- | :--- | :--- |
| **Bluetooth (UART5)** | RX: **D2** (half duplex) | Baudrate: 57600 |
| **OLED (I2C1)** | SCL: **B8**, SDA: **B9** | Address: 0x3C (60) |
| **Status LED** | Pin **C13** (Red) | Active Low (Inverted logic) |
| **REPL (UART1)** | TX: **B6**, RX: **B7** | Baudrate: 115200 |

---

##  Requirements
1.  **MicroPython Firmware**: Compiled for `MINI_NODE_V3` with `MICROPY_HW_ENABLE_RTC` enabled.
2.  **Files**:
    *   `main.py`: The application logic.
    *   `ssd1306.py`: Standard MicroPython OLED driver.

---

## Run Section
To deploy the code to your node and monitor the output, run the following commands in your terminal:

```bash
# Copy the application files to the board
mpremote connect /dev/ttyUSB0 cp lab/main.py :main.py
mpremote connect /dev/ttyUSB0 cp lab/ssd1306.py :ssd1306.py

# Open the serial terminal to view the REPL and RTC status
tio /dev/ttyUSB0 -b 115200
import main
main.main()
```

---

## Bluetooth Protocol
The parser expects data in the following format followed by a newline:
`HH:MM:SS\nDD:MM:YYYY`

Once received, the script automatically updates the internal STM32 RTC, which then maintains the time using the onboard **32768Hz LSE oscillator**.
