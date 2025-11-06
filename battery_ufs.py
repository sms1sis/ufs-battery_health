#!/usr/bin/env python3
import os
import glob
import argparse

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def read_file(path):
    """Safely read a file and return its stripped content."""
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except (IOError, FileNotFoundError):
        return None

def ufs_health_percent(hex_value):
    """Convert UFS hex value to a health percentage."""
    try:
        val = int(hex_value, 16)
        percent = max(0, 100 - val * 10)
        return percent
    except (ValueError, TypeError):
        return None

def get_health_color(percent):
    """Return a color based on the health percentage."""
    if percent is None:
        return CYAN
    if percent >= 80:
        return GREEN
    elif percent >= 50:
        return YELLOW
    else:
        return RED

def find_first_existing_value(paths):
    """Find the first file that exists from a list of glob patterns and return its value."""
    for pattern in paths:
        for f in glob.glob(pattern):
            val = read_file(f)
            if val is not None:
                return val
    return None

def main():
    """Main function to gather and display battery and UFS health."""
    parser = argparse.ArgumentParser(
        description="Monitor battery and UFS storage health on rooted Android devices.",
        epilog="This script must be run with root privileges (e.g., via tsu/sudo) to access system files."
    )
    parser.parse_args() # We don't need any arguments, but this provides -h/--help

    # --- UFS Health ---
    ufs_paths = glob.glob("/sys/devices/platform/soc/*.ufshc/health_descriptor/life_time_estimation_*")
    ufs_a_percent = ufs_b_percent = None
    if len(ufs_paths) >= 2:
        ufs_a_percent = ufs_health_percent(read_file(ufs_paths[0]))
        ufs_b_percent = ufs_health_percent(read_file(ufs_paths[1]))

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

    charge_full_str = find_first_existing_value(charge_full_paths)
    charge_design_str = find_first_existing_value(charge_design_paths)
    cycle_count_str = find_first_existing_value(cycle_count_paths)

    battery_health_percent = None
    if charge_full_str and charge_design_str:
        try:
            battery_health_percent = int((int(charge_full_str) / int(charge_design_str)) * 100)
        except (ValueError, ZeroDivisionError, TypeError):
            battery_health_percent = None

    # --- Print Output ---
    print(f"{BOLD}{CYAN}=================== Battery & UFS Status ==================={RESET}\n")

    print(f"{BOLD}🔋 Battery Info{RESET}")
    if battery_health_percent is not None:
        try:
            charge_now_mAh = int(charge_full_str) / 1000
            charge_design_mAh = int(charge_design_str) / 1000
            health_color = get_health_color(battery_health_percent)
            
            print(f"  {CYAN}◆ Battery Capacity:{RESET} {YELLOW}{charge_now_mAh:.0f} / {charge_design_mAh:.0f} mAh{RESET}")

        except (ValueError, TypeError):
            print(f"  {CYAN}◆ Battery Capacity:{RESET} {RED}Invalid data{RESET}")
    else:
        print(f"  {CYAN}◆ Battery Capacity:{RESET} {RED}Not found{RESET}")

    if cycle_count_str:
        print(f"  {CYAN}◆ Cycle Count:{RESET} {YELLOW}{cycle_count_str}{RESET}")
    else:
        print(f"  {CYAN}◆ Cycle Count:{RESET} {RED}Not found{RESET}")

    if battery_health_percent is not None:
        color = get_health_color(battery_health_percent)
        print(f"  {CYAN}◆ Battery Health:{RESET} {color}{battery_health_percent}% remaining{RESET}")
    else:
        print(f"  {CYAN}◆ Battery Health:{RESET} {RED}Not found{RESET}")


    print(f"\n{BOLD}💾 UFS Health{RESET}")
    if ufs_a_percent is not None:
        color = get_health_color(ufs_a_percent)
        print(f"  {CYAN}◆ Life Time Estimation A:{RESET} {color}{ufs_a_percent}% remaining{RESET}")
    else:
        print(f"  {CYAN}◆ Life Time Estimation A:{RESET} {RED}Not found{RESET}")

    if ufs_b_percent is not None:
        color = get_health_color(ufs_b_percent)
        print(f"  {CYAN}◆ Life Time Estimation B:{RESET} {color}{ufs_b_percent}% remaining{RESET}")
    else:
        print(f"  {CYAN}◆ Life Time Estimation B:{RESET} {RED}Not found{RESET}")

    # --- Notes ---
    print(f"\n{BOLD}{MAGENTA}========================== Notes ==========================={RESET}")
    notes = [
        What are “Life Time Estimation A” and “B”?

        Your phone’s UFS chip has two health meters, labeled A and B.

        >> A (Main storage health):
        This measures how healthy the main part of your storage is — where your apps, photos, and files are kept.
        When you install, delete, or update apps, this area wears down little by little.

        >> B (System area health):
        This measures the hidden system part of the chip — used by your phone’s software to manage storage, cache, and boot data.
        Even though you don’t see it, this area also wears down as your phone works.
    ]
    for note in notes:
        print(f"{note}")
    print(f"\n{BOLD}{CYAN}============================================================{RESET}")

if __name__ == "__main__":
    main()
