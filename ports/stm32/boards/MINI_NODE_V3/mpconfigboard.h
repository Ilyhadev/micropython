#define MICROPY_HW_BOARD_NAME       "MINI_NODE_V3"
#define MICROPY_HW_MCU_NAME         "STM32G0B1CE"

#define MICROPY_HW_ENABLE_DWT_CYCCNT (1)
#define MICROPY_HW_HAS_SWITCH        (0)
#define MICROPY_HW_HAS_FLASH         (1)
#define MICROPY_HW_ENABLE_RNG        (0)
#define MICROPY_HW_ENABLE_RTC        (1)
#define MICROPY_HW_ENABLE_DAC        (1)
#define MICROPY_HW_ENABLE_USB        (0)

#define MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE (1)

#define MICROPY_PY_PYB_LEGACY       (0)

// Clock: 64 MHz from internal HSI
#define MICROPY_HW_CLK_USE_HSI      (1)
#define MICROPY_HW_FLASH_LATENCY    FLASH_LATENCY_2

#define MICROPY_HW_CLK_PLLM         (1)
#define MICROPY_HW_CLK_PLLN         (8)
#define MICROPY_HW_CLK_PLLP         (2)
#define MICROPY_HW_CLK_PLLQ         (2)
#define MICROPY_HW_CLK_PLLR         (2)

// REPL on UART1
#define MICROPY_HW_UART_REPL        PYB_UART_1
#define MICROPY_HW_UART_REPL_BAUD   115200

// USART1
#define MICROPY_HW_UART1_TX         (pin_B6)
#define MICROPY_HW_UART1_RX         (pin_B7)

#define MICROPY_HW_UART5_TX         (pin_B0)
#define MICROPY_HW_UART5_RX         (pin_D2)

// I2C1
#define I2C1_EV_IRQn   I2C1_IRQn
#define I2C1_ER_IRQn   I2C1_IRQn

#define MICROPY_HW_I2C1_SCL         (pin_B8)
#define MICROPY_HW_I2C1_SDA         (pin_B9)

// SPI1 + SPI2
#define MICROPY_HW_SPI1_NSS         (pin_A4)
#define MICROPY_HW_SPI1_SCK         (pin_B3)
#define MICROPY_HW_SPI1_MISO        (pin_B4)
#define MICROPY_HW_SPI1_MOSI        (pin_B5)

#define MICROPY_HW_SPI2_NSS         (pin_B12)
#define MICROPY_HW_SPI2_SCK         (pin_B13)
#define MICROPY_HW_SPI2_MISO        (pin_B14)
#define MICROPY_HW_SPI2_MOSI        (pin_B11)

#define MICROPY_HW_LED_RED          (pin_C13)
#define MICROPY_HW_LED_GREEN        (pin_C14)
#define MICROPY_HW_LED_BLUE         (pin_C15)

#define MICROPY_HW_LED1             (MICROPY_HW_LED_RED)
#define MICROPY_HW_LED2             (MICROPY_HW_LED_GREEN)
#define MICROPY_HW_LED3             (MICROPY_HW_LED_BLUE)

#define MICROPY_HW_LED_ON(pin)      (mp_hal_pin_high(pin)) // Helpful bug: in current config red.on() turns off, red.off() turns on - i decided to let it be that way for debug purposes - to swiftly understand if micropython initialized successfully
#define MICROPY_HW_LED_OFF(pin)     (mp_hal_pin_low(pin))
