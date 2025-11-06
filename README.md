# Android Battery & UFS Health Monitor (Termux)

A simple **Python script** to monitor **battery and UFS storage health** on Android devices with **Snapdragon SoCs**.  
It provides a **colorful, human-readable output** in Termux with detailed battery info, charge cycles, battery health %, and UFS life estimation.

---

## ✨ Features

- 🔋 **Battery Info**
  - Full Charge Capacity (mAh)
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

## 📱 Compatibility

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

## 📦 Requirements

- **Termux** installed on your Android device
- **Python 3.7+**
- **tsu**
- **Root access**
```bash
pkg update && pkg install python tsu
```
---

## 🚀 Usage
- In Termux, you can use [`tsu`](https://github.com/termux/termux-packages/wiki/tsu) for sudo permissions.
- Recommended to run with **sudo/tsu** for full access:

```bash
 sudo python3 battery_ufs.py
```

---

## 🖥️ Example Output

```
=================== Battery & UFS Status ===================

🔋 Battery Info
  ◆ Battery Capacity: 4768 / 5020 mAh
  ◆ Cycle Count: 40
  ◆ Battery Health: 94% remaining

💾 UFS Health
  ◆ Life Time Estimation A: 70% remaining
  ◆ Life Time Estimation B: 90% remaining

========================== Notes ===========================
UFS storage has two health values, A and B, because manufacturers use different vendor-specific algorithms to estimate the lifespan.
Both values track the health of the main UFS memory units based on program/erase cycles, but they may represent different wear patterns or types of memory blocks.

============================================================
```
