# Android Battery & UFS Health Monitor (Termux)

A simple **Python script** to monitor **battery and UFS storage health** on Android devices with **Snapdragon SoCs**.  
It provides a **colorful, human-readable output** in Termux with detailed battery info, charge cycles, battery health %, and UFS life estimation.

---

## Features

- 🔋 **Battery Info**
  - Full Charge Capacity (µAh)
  - Cycle Count
  - Battery Health % (compared to design capacity)
- 💾 **UFS Storage Health**
  - Life Time Estimation A & B (hex → % remaining)
  - Color-coded status (Green=Good, Yellow=Moderate, Red=Poor)
- ℹ **Detailed notes**
  - Explains what Life Time Estimation A/B mean
  - Explains battery health %
  - Health color guide
- ✅ Works in **Termux** on Android

---

## Compatibility

- Designed for **Snapdragon SoC devices** with **UFS storage**.
- Tested on:
  - Xiaomi Redmi series
  - Google Pixel devices
  - OnePlus devices
- Should work on **most modern Snapdragon Android phones**.
- **May not work** on:
  - MediaTek or Exynos devices (battery paths differ)
  - Phones with **eMMC storage** (no UFS health)
  - Custom kernels that hide sysfs paths
- Requires **root access** to read system paths (`/sys/devices/...`).

---

## Prerequisites

- **Termux** installed on your Android device
- **Python 3.7+**
- **Root access**
  - In Termux, you can use [`tsu`](https://github.com/termux/termux-packages/wiki/tsu) for sudo permissions.
- Recommended to run with **sudo/tsu** for full access:
  ```bash
  tsu
  python3 battery_ufs.py
