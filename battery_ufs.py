#!/usr/bin/env python3
import os

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception as e:
        return f"Error: {e}"

# Convert UFS hex to health %
def ufs_health_percent(hex_value):
    try:
        val = int(hex_value, 16)
        percent = max(0, 100 - val*10)  # approximate
        return percent
    except:
        return None

# Color based on % health
def health_color(percent):
    if percent is None:
        return CYAN
    if percent >= 80:
        return GREEN
    elif percent >= 50:
        return YELLOW
    else:
        return RED

# UFS Health
ufs_a_path = "/sys/devices/platform/soc/1d84000.ufshc/health_descriptor/life_time_estimation_a"
ufs_b_path = "/sys/devices/platform/soc/1d84000.ufshc/health_descriptor/life_time_estimation_b"

ufs_a_raw = read_file(ufs_a_path)
ufs_b_raw = read_file(ufs_b_path)

ufs_a_percent = ufs_health_percent(ufs_a_raw)
ufs_b_percent = ufs_health_percent(ufs_b_raw)

# Battery info
charge_full_path = "/sys/devices/platform/soc/c440000.qcom,spmi/spmi-0/spmi0-00/c440000.qcom,spmi:qcom,pm6150@0:qcom,qpnp-smb5/power_supply/battery/charge_full"
cycle_count_path = "/sys/devices/platform/soc/c440000.qcom,spmi/spmi-0/spmi0-00/c440000.qcom,spmi:qcom,pm6150@0:qcom,qpnp-smb5/power_supply/battery/cycle_count"

charge_full = read_file(charge_full_path)
cycle_count = read_file(cycle_count_path)

# Print output
print(f"{CYAN}🔋 Battery Info:{RESET}")
print(f"→ Full Charge Capacity: {YELLOW}{charge_full}{RESET} µAh")
print(f"→ Cycle Count: {YELLOW}{cycle_count}{RESET}")

print(f"\n{CYAN}💾 UFS Health:{RESET}")
print(f"→ Life Time Estimation A: {health_color(ufs_a_percent)}{ufs_a_percent}% remaining{RESET}")
print(f"→ Life Time Estimation B: {health_color(ufs_b_percent)}{ufs_b_percent}% remaining{RESET}")
