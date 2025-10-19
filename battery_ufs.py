#!/usr/bin/env python3
import os
import glob

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return None

def ufs_health_percent(hex_value):
    try:
        val = int(hex_value, 16)
        percent = max(0, 100 - val*10)
        return percent
    except:
        return None

def health_color(percent):
    if percent is None:
        return CYAN
    if percent >= 80:
        return GREEN
    elif percent >= 50:
        return YELLOW
    else:
        return RED

def battery_health_color(percent):
    if percent is None:
        return CYAN
    if percent >= 90:
        return GREEN
    elif percent >= 70:
        return YELLOW
    else:
        return RED

# --- UFS Health ---
ufs_paths = glob.glob("/sys/devices/platform/soc/*.ufshc/health_descriptor/life_time_estimation_*")
ufs_a_percent = ufs_b_percent = None

if len(ufs_paths) >= 2:
    ufs_a_percent = ufs_health_percent(read_file(ufs_paths[0]))
    ufs_b_percent = ufs_health_percent(read_file(ufs_paths[1]))
else:
    print(f"{RED}⚠ Could not find UFS health paths!{RESET}")

# --- Battery Info ---
charge_full_paths = [
    "/sys/class/power_supply/battery/charge_full",
    "/sys/class/power_supply/battery/charge_full_design",
    "/sys/devices/platform/soc/*/battery/charge_full"
]
charge_design_paths = [
    "/sys/class/power_supply/battery/charge_full_design",
    "/sys/devices/platform/soc/*/battery/charge_full_design"
]
cycle_count_paths = [
    "/sys/class/power_supply/battery/cycle_count",
    "/sys/devices/platform/soc/*/battery/cycle_count"
]

def find_first_existing(paths):
    for pattern in paths:
        for f in glob.glob(pattern):
            val = read_file(f)
            if val is not None:
                return val
    return None

charge_full = find_first_existing(charge_full_paths)
charge_design = find_first_existing(charge_design_paths)
cycle_count = find_first_existing(cycle_count_paths)

battery_health_percent = None
if charge_full and charge_design:
    try:
        battery_health_percent = int(int(charge_full) / int(charge_design) * 100)
    except:
        battery_health_percent = None

# --- Print Output ---
print(f"{BOLD}{CYAN}================== Battery & UFS Status =================={RESET}\n")

print(f"{BOLD}🔋 Battery Info{RESET}")
if charge_full:
    try:
        charge_mAh = int(charge_full) / 1000
        print(f"  → Full Charge Capacity: {YELLOW}{charge_mAh} mAh{RESET}")
    except:
        print(f"  → Full Charge Capacity: {RED}Invalid value{RESET}")
else:
    print(f"  → Full Charge Capacity: {RED}Not found{RESET}")

if cycle_count:
    print(f"  → Cycle Count: {YELLOW}{cycle_count}{RESET}")
else:
    print(f"  → Cycle Count: {RED}Not found{RESET}")

if battery_health_percent:
    print(f"  → Battery Health: {battery_health_color(battery_health_percent)}{battery_health_percent}%{RESET}")
else:
    print(f"  → Battery Health: {RED}Not found{RESET}")

print(f"\n{BOLD}💾 UFS Health{RESET}")
if ufs_a_percent is not None:
    print(f"  → Life Time Estimation A: {health_color(ufs_a_percent)}{ufs_a_percent}% remaining{RESET}")
else:
    print(f"  → Life Time Estimation A: {RED}Not found{RESET}")

if ufs_b_percent is not None:
    print(f"  → Life Time Estimation B: {health_color(ufs_b_percent)}{ufs_b_percent}% remaining{RESET}")
else:
    print(f"  → Life Time Estimation B: {RED}Not found{RESET}")

# --- Notes ---
print(f"\n{BOLD}{MAGENTA}====================== Notes ======================{RESET}")
notes = [
    "🟢 Life Time Estimation A: Tracks overall UFS health based on wear of LUN A (first memory unit).",
    "🟢 Life Time Estimation B: Tracks overall UFS health based on wear of LUN B (second memory unit).",
    "🔋 Battery Health %: Estimated remaining capacity compared to design capacity. Higher % = healthier battery.",
    "⚠ Colors indicate health status (Green=Good, Yellow=Moderate, Red=Poor)."
]
for note in notes:
    print(f"  {note}")

print(f"\n{BOLD}{CYAN}====================================================={RESET}")
