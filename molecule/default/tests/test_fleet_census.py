"""
=== STARFALL DEFENCE CORPS ACADEMY ===
ARIA Automated Verification - Mission 1.1: Fleet Census
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
