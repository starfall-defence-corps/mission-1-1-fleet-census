"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for mission verification.

Writes all output to stderr so check-work.sh can discard pytest's
default stdout while preserving our formatted display.
"""
import os
import pytest
import sys

# -- Phase and test name mappings -------------------------------------------

PHASES = {
    "TestInventoryStructure": ("1", "Fleet Registry"),
    "TestConnectivity":       ("2", "Connectivity"),
    "TestFactsGathered":      ("3", "Reconnaissance"),
    "TestChmod777Evidence":   ("4", "Threat Assessment"),
    "TestFilteredFacts":      ("5", "Filtered Intelligence"),
}

FRIENDLY = {
    "test_inventory_file_exists":         "Inventory file exists",
    "test_inventory_is_valid_yaml":       "Inventory is valid YAML",
    "test_inventory_has_all_hosts":       "All fleet nodes registered",
    "test_inventory_has_groups":          "Hosts organised into groups",
    "test_ping_all_nodes":                "All nodes respond to ping",
    "test_can_gather_facts":              "Facts gathering operational",
    "test_intel_report_exists":           "Intel report created",
    "test_intel_report_has_os_info":      "OS recorded for all nodes",
    "test_intel_report_has_ip_addresses": "IP addresses recorded",
    "test_compromised_files_recorded":    "Compromised files documented",
    "test_compromised_files_are_valid_paths": "File paths validated",
    "test_fleet_memory_total_recorded":   "Fleet memory total calculated",
}

# -- Reporter ---------------------------------------------------------------

# The phase-oriented summary is rendered by the shared `aria-reporter`
# pytest plugin (installed via requirements.txt); this file only declares
# the mission's phases + friendly objective names.
from aria_reporter import configure  # noqa: E402

configure(phases=PHASES, friendly=FRIENDLY, mission_id="1-1")
