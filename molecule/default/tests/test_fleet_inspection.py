"""
=== STARFALL DEFENCE CORPS ACADEMY ===
ARIA Automated Verification - Mission 1.1: Fleet Inspection
========================================================
"""
import os
import subprocess
import yaml
import pytest


def _root_dir():
    """Return the mission root directory."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(tests_dir, "..", "..", ".."))


def _workspace_dir():
    return os.path.join(_root_dir(), "workspace")


def _student_inventory():
    return os.path.join(_workspace_dir(), "inventory", "hosts.yml")


def _intel_report():
    return os.path.join(_workspace_dir(), "reports", "fleet-intel.yml")


def _load_intel_report():
    path = _intel_report()
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


# -------------------------------------------------------------------
# Phase 1: Inventory file exists and has correct structure
# -------------------------------------------------------------------

class TestInventoryStructure:
    """ARIA verifies: Has the cadet created a valid fleet registry?"""

    def test_inventory_file_exists(self):
        """Inventory file must exist at workspace/inventory/hosts.yml"""
        assert os.path.isfile(_student_inventory()), (
            "ARIA: No inventory file detected at workspace/inventory/hosts.yml. "
            "Cadet, the fleet cannot be managed without an asset registry. "
            "Create your inventory file and try again."
        )

    def test_inventory_is_valid_yaml(self):
        """Inventory must be valid YAML"""
        inv = _student_inventory()
        if not os.path.isfile(inv):
            pytest.skip("Inventory file does not exist yet")
        with open(inv) as f:
            data = yaml.safe_load(f)
        assert data is not None, (
            "ARIA: Inventory file is empty. A blank registry protects no one."
        )

    def test_inventory_has_all_hosts(self):
        """All three fleet nodes must be listed"""
        inv = _student_inventory()
        if not os.path.isfile(inv):
            pytest.skip("Inventory file does not exist yet")
        with open(inv) as f:
            content = f.read()
        missing = []
        for host in ["sdc-web", "sdc-db", "sdc-comms"]:
            if host not in content:
                missing.append(host)
        assert not missing, (
            f"ARIA: The following fleet nodes are missing from your inventory: "
            f"{', '.join(missing)}. Unregistered assets are unprotected assets."
        )

    def test_inventory_has_groups(self):
        """Inventory should use groups, not just a flat list"""
        inv = _student_inventory()
        if not os.path.isfile(inv):
            pytest.skip("Inventory file does not exist yet")
        with open(inv) as f:
            data = yaml.safe_load(f)
        # Walk the structure to find 'children' at any level
        group_count = _count_groups(data)
        assert group_count >= 2, (
            "ARIA: Insufficient grouping detected. A flat inventory is a sign of "
            "disorganised fleet management. Group your hosts logically — "
            "web servers, database servers, communications relays."
        )


def _count_groups(data, depth=0):
    """Count group definitions in an Ansible inventory structure."""
    if not isinstance(data, dict):
        return 0
    count = 0
    for key, val in data.items():
        if key == "children" and isinstance(val, dict):
            count += len(val)
            for child in val.values():
                if isinstance(child, dict):
                    count += _count_groups(child, depth + 1)
        elif isinstance(val, dict):
            count += _count_groups(val, depth + 1)
    return count


# -------------------------------------------------------------------
# Phase 2: Connectivity verified
# -------------------------------------------------------------------

class TestConnectivity:
    """ARIA verifies: Can the cadet reach all fleet nodes?"""

    def test_ping_all_nodes(self):
        """All nodes must respond to ansible ping via student inventory"""
        inv = _student_inventory()
        if not os.path.isfile(inv):
            pytest.skip("Inventory file does not exist yet")
        result = subprocess.run(
            ["ansible", "all", "-m", "ping", "-i", inv],
            capture_output=True, text=True, timeout=30,
            cwd=_workspace_dir(),
        )
        assert result.returncode == 0, (
            f"ARIA: Ping failed. Fleet nodes are unreachable via your inventory.\n"
            f"Output: {result.stdout}\n"
            f"Errors: {result.stderr}\n"
            f"Verify your ansible_host, ansible_user, and ansible_port values. "
            f"Ensure containers are running with 'make setup'."
        )


# -------------------------------------------------------------------
# Phase 3: Facts gathered
# -------------------------------------------------------------------

class TestFactsGathered:
    """ARIA verifies: Has the cadet conducted fleet reconnaissance?"""

    def test_can_gather_facts(self):
        """setup module must succeed on all nodes"""
        inv = _student_inventory()
        if not os.path.isfile(inv):
            pytest.skip("Inventory file does not exist yet")
        result = subprocess.run(
            [
                "ansible", "all", "-m", "setup",
                "-i", inv,
                "-a", "filter=ansible_distribution",
            ],
            capture_output=True, text=True, timeout=30,
            cwd=_workspace_dir(),
        )
        assert result.returncode == 0, (
            "ARIA: Facts gathering failed. You cannot defend a fleet "
            "you cannot inspect. Verify connectivity first."
        )
        assert "Ubuntu" in result.stdout, (
            "ARIA: Expected Ubuntu distribution in facts output. "
            "Verify your nodes are reachable and running the correct OS."
        )

    def test_intel_report_exists(self):
        """Intel report must exist at workspace/reports/fleet-intel.yml"""
        assert os.path.isfile(_intel_report()), (
            "ARIA: No intel report detected at workspace/reports/fleet-intel.yml. "
            "Copy the template: cp workspace/reports/fleet-intel.yml.example "
            "workspace/reports/fleet-intel.yml — then fill in your findings."
        )

    def test_intel_report_has_os_info(self):
        """Intel report must contain OS information for all nodes"""
        data = _load_intel_report()
        if data is None:
            pytest.skip("Intel report does not exist yet")
        nodes = data.get("fleet_nodes", {})
        for host in ["sdc-web", "sdc-db", "sdc-comms"]:
            node = nodes.get(host, {})
            os_val = node.get("os", "REPLACE_ME")
            assert os_val != "REPLACE_ME" and os_val, (
                f"ARIA: OS not recorded for {host}. Run "
                f"'ansible all -m setup -a \"filter=ansible_distribution*\"' "
                f"and record the OS in your intel report."
            )

    def test_intel_report_has_ip_addresses(self):
        """Intel report must contain IP addresses for all nodes"""
        data = _load_intel_report()
        if data is None:
            pytest.skip("Intel report does not exist yet")
        nodes = data.get("fleet_nodes", {})
        for host in ["sdc-web", "sdc-db", "sdc-comms"]:
            node = nodes.get(host, {})
            ip_val = node.get("ip_address", "REPLACE_ME")
            assert ip_val != "REPLACE_ME" and ip_val, (
                f"ARIA: IP address not recorded for {host}. Run "
                f"'ansible all -m setup -a \"filter=ansible_default_ipv4\"' "
                f"and record the address in your intel report."
            )


# -------------------------------------------------------------------
# Phase 4: Agent Chmod-777 damage documented
# -------------------------------------------------------------------

class TestChmod777Evidence:
    """ARIA verifies: Has the cadet documented Agent Chmod-777's damage?"""

    def test_compromised_files_recorded(self):
        """Intel report must list compromised files found on fleet nodes"""
        data = _load_intel_report()
        if data is None:
            pytest.skip("Intel report does not exist yet")
        files = data.get("compromised_files", [])
        real_files = [f for f in files if f and f != "REPLACE_ME"]
        assert len(real_files) >= 3, (
            f"ARIA: Insufficient evidence documented. Found {len(real_files)} "
            f"compromised file(s) in your report — expected at least 3. "
            f"Run 'ansible all -m shell -a \"find /opt -perm -0777 -type f "
            f"2>/dev/null\"' and record every file path in your intel report."
        )

    def test_compromised_files_are_valid_paths(self):
        """Compromised file paths must look like real filesystem paths"""
        data = _load_intel_report()
        if data is None:
            pytest.skip("Intel report does not exist yet")
        files = data.get("compromised_files", [])
        real_files = [f for f in files if f and f != "REPLACE_ME"]
        if not real_files:
            pytest.skip("No compromised files recorded yet")
        for path in real_files:
            assert path.startswith("/opt/fleet-data/"), (
                f"ARIA: Suspicious file path '{path}'. Agent Chmod-777's "
                f"evidence should be under /opt/fleet-data/. Verify your findings."
            )


# -------------------------------------------------------------------
# Phase 5: Filtered facts and fleet memory
# -------------------------------------------------------------------

class TestFilteredFacts:
    """ARIA verifies: Has the cadet extracted targeted intelligence?"""

    def test_fleet_memory_total_recorded(self):
        """Intel report must contain total fleet memory"""
        data = _load_intel_report()
        if data is None:
            pytest.skip("Intel report does not exist yet")
        mem = data.get("fleet_memory_total_mb", 0)
        assert isinstance(mem, (int, float)) and mem > 0, (
            "ARIA: Fleet memory total not recorded or is zero. "
            "Run 'ansible all -m setup -a \"filter=ansible_memtotal_mb\"', "
            "sum the values from all 3 nodes, and record in your intel report."
        )
