"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for mission verification.

Writes all output to stderr so check-work.sh can discard pytest's
default stdout while preserving our formatted display.
"""
import pytest
import sys

# -- ANSI escape codes ------------------------------------------------------

_COLOR = hasattr(sys.stderr, "isatty") and sys.stderr.isatty()


def _c(code):
    return code if _COLOR else ""


GREEN = _c("\033[32m")
RED = _c("\033[31m")
YELLOW = _c("\033[33m")
CYAN = _c("\033[36m")
DIM = _c("\033[2m")
BOLD = _c("\033[1m")
RESET = _c("\033[0m")

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


class _ARIAReporter:
    def __init__(self):
        self._current_class = None
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    @staticmethod
    def _out(text):
        sys.stderr.write(text)
        sys.stderr.flush()

    def record(self, nodeid, outcome, longrepr):
        parts = nodeid.split("::")
        cls = parts[1] if len(parts) > 1 else ""
        test = parts[-1]

        num, label = PHASES.get(cls, ("?", "Unknown"))
        name = FRIENDLY.get(test, test)

        # Phase header on first test in each class
        if cls != self._current_class:
            self._current_class = cls
            self._out(f"\n  {CYAN}{BOLD}Phase {num}: {label}{RESET}\n")

        if outcome == "passed":
            self.passed += 1
            self._out(f"    {GREEN}✓{RESET} {name}\n")
        elif outcome == "skipped":
            self.skipped += 1
            self._out(f"    {YELLOW}○{RESET} {DIM}{name} — skipped{RESET}\n")
        else:
            self.failed += 1
            self._out(f"    {RED}✗{RESET} {name}\n")
            hint = _extract_hint(longrepr)
            if hint:
                self._out(f"      {DIM}↳ {hint}{RESET}\n")

    def summary(self):
        total = self.passed + self.failed + self.skipped
        self._out(f"\n  {'─' * 44}\n")
        parts = []
        if self.passed:
            parts.append(f"{GREEN}{self.passed} verified{RESET}")
        if self.failed:
            parts.append(f"{RED}{self.failed} deficient{RESET}")
        if self.skipped:
            parts.append(f"{YELLOW}{self.skipped} skipped{RESET}")
        self._out(
            f"  {BOLD}Results:{RESET} {' · '.join(parts)}"
            f"  {DIM}({total} checks){RESET}\n"
        )


def _extract_hint(longrepr):
    """Pull the ARIA: message from an assertion failure."""
    if longrepr is None:
        return None
    # Prefer the clean crash message over the full traceback repr
    crash = getattr(longrepr, "reprcrash", None)
    if crash:
        msg = getattr(crash, "message", "")
        if "ARIA:" in msg:
            return msg.split("ARIA:", 1)[-1].strip()
    # Fallback: search the string representation
    text = str(longrepr)
    if "ARIA:" in text:
        raw = text.split("ARIA:")[-1].splitlines()[0].strip()
        return raw.rstrip("'\"")
    return None


# -- Singleton instance -----------------------------------------------------

_reporter = _ARIAReporter()

# -- Pytest hooks -----------------------------------------------------------


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """Intercept results before the default reporter sees them."""
    if report.when == "call":
        _reporter.record(report.nodeid, report.outcome, report.longrepr)
        report.longrepr = None  # suppress default traceback display
    elif report.when == "setup" and report.skipped:
        _reporter.record(report.nodeid, "skipped", report.longrepr)
        report.longrepr = None


def pytest_report_teststatus(report, config):
    """Return empty strings so the default reporter prints nothing per-test."""
    if report.when == "call":
        return report.outcome, "", ""
    if report.when == "setup" and report.skipped:
        return "skipped", "", ""


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print our summary; clear stats to suppress the default summary."""
    _reporter.summary()
