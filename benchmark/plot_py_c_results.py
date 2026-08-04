import matplotlib.pyplot as plt
import numpy as np
import os

# Data based on sources
# Speeds in us
c_speed = {"GPIO": 34419, "Math": 191080, "String": 10839986, "Struct": 16192}
py_speed = {"GPIO": 3525397, "Math": 332681, "String": 24852289, "Struct": 140329}
mpy_speed = {"GPIO": 3525400, "Math": 332698, "String": 24851257, "Struct": 140329}

py_gpio_variants = {
    "Regular (machine.Pin)": 3525398,
    "Direct Reg Access": 5532059,
    "Optimized Direct Reg Access": 2607305,
}

# 1. Size: mpy vs py
plt.figure(figsize=(6, 4))
plt.bar(["Source (.py)", "Compiled (.mpy)"], [4374, 2249], color=["#e74c3c", "#3498db"])
plt.title("Script Size: .py vs .mpy")
plt.ylabel("Bytes")
for i, v in enumerate([4374, 2249]):
    plt.text(i, v + 100, str(v), ha="center")
plt.savefig("size_mpy_vs_py.png")
plt.close()

# 2. Size: py vs C (Firmware footprint)
plt.figure(figsize=(6, 4))
plt.bar(["Bare Metal C", "MicroPython Base"], [42.3, 296.4], color=["#2ecc71", "#9b59b6"])
plt.title("Firmware Base Size: C vs MicroPython")
plt.ylabel("Kilobytes (KB)")
for i, v in enumerate([42.3, 296.4]):
    plt.text(i, v + 5, f"{v} KB", ha="center")
plt.savefig("size_c_vs_py.png")
plt.close()

# 3. Speed: py vs C
labels = list(c_speed.keys())
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width / 2, list(c_speed.values()), width, label="C", color="#2ecc71")
ax.bar(x + width / 2, list(py_speed.values()), width, label="Python", color="#e74c3c")

ax.set_ylabel("Execution Time (µs) - Log Scale")
ax.set_title("Execution Speed: C vs Python")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_yscale("log")
ax.legend()
plt.savefig("speed_c_vs_py.png")
plt.close()

# 4. Speed: Python GPIO Access Variants
plt.figure(figsize=(8, 5))
labels_gpio = list(py_gpio_variants.keys())
values_gpio = list(py_gpio_variants.values())
bars = plt.bar(labels_gpio, values_gpio, color=["#e67e22", "#c0392b", "#d35400"])
plt.title("Python GPIO Access Strategies")
plt.ylabel("Execution Time (µs)")
plt.xticks(rotation=15)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 50000, f"{int(yval)}", ha="center")
plt.tight_layout()
plt.savefig("speed_gpio_variants.png")
plt.close()

print("Images generated.")
