---
CLASSIFICATION: CADET EYES ONLY
MISSION: 1.1 — FLEET INSPECTION
DOCUMENT: EXERCISES — Phase-by-Phase Operational Instructions
---

# EXERCISES — MISSION 1.1: FLEET INSPECTION

Complete each phase in sequence. Run `make test` after each phase. Do not advance until ARIA confirms compliance.

**Two directories, two purposes:**

- **Ansible commands** (`ansible`, `ansible-playbook`): Run from `workspace/` where `ansible.cfg` lives.
- **Make commands** (`make test`, `make reset`): Run from the **project root** (where the `Makefile` lives).

When a phase says "Run ARIA's Verification", return to the project root first:

```bash
cd ..        # from workspace/ back to project root
make test
cd workspace # return to workspace for the next phase
```

---

## PHASE 0: Launch the Fleet

> Before any mission can begin, your fleet must be online. Launch the fleet nodes and confirm they are operational.

### Step 0.1 — Start the Fleet

From the **project root directory** (not `workspace/`), run:

```bash
make setup
```

This builds the Docker containers, generates SSH credentials, and starts all three fleet nodes. Wait for the output to confirm:

```
  Fleet Status: 3 nodes ONLINE
```

### Step 0.2 — If Things Go Wrong

If containers are in a bad state or you need a clean start at any point during the mission:

```bash
make reset
```

This destroys all containers and rebuilds them from scratch. Your work in `workspace/` (inventory, reports) is preserved — only the containers are reset.

---

## PHASE 1: Build the Asset Registry

> The fleet's ships are scattered and undocumented. Your first task is to create a complete asset registry — without it, there is no fleet, only chaos. Every node must be catalogued before any operation can proceed.

### What You Are Building

An Ansible **inventory file** is the foundation of all automation. It tells Ansible which systems exist, how to reach them, and how they are grouped. Without an inventory, Ansible has nothing to act on.

You will create the fleet's inventory at `workspace/inventory/hosts.yml`.

### Step 1.1 — Understand the Fleet Asset Table

Before writing anything, study the fleet you are registering:

| Designation | Role | SSH Host | SSH Port |
|-------------|------|----------|----------|
| `sdc-web` | Fleet Web Server | localhost | 2221 |
| `sdc-db` | Fleet Database Server | localhost | 2222 |
| `sdc-comms` | Fleet Communications Relay | localhost | 2223 |

All three nodes are Docker containers running locally. They listen on different ports, which is how Ansible distinguishes between them.

### Step 1.2 — Understand Groups

Ansible inventory groups allow you to target subsets of your fleet. Instead of running a command against a specific host by name, you can run it against a group — and Ansible handles the rest.

In this fleet, the three nodes belong to three functional groups:

- `web_servers` — hosts running web-facing services
- `db_servers` — hosts running database workloads
- `comms_relays` — hosts handling communications infrastructure

There is also a built-in group called `all` that automatically includes every host in the inventory. You will use this group frequently.

### Step 1.3 — Create the Inventory File

Create the file `workspace/inventory/hosts.yml`. The `inventory/` directory already exists.

The inventory file uses YAML format. The structure is:

```
all:
  children:
    <group_name>:
      hosts:
        <host_name>:
          <variable>: <value>
```

- `all` is the root group. All other groups nest inside it under `children`.
- Each group contains a `hosts` block.
- Each host can have variables — connection details like `ansible_host` and `ansible_port`.

Here is the complete inventory for the fleet. Copy this into `workspace/inventory/hosts.yml` and review each line:

```yaml
all:
  children:
    web_servers:
      hosts:
        sdc-web:
          ansible_host: localhost
          ansible_port: 2221

    db_servers:
      hosts:
        sdc-db:
          ansible_host: localhost
          ansible_port: 2222

    comms_relays:
      hosts:
        sdc-comms:
          ansible_host: localhost
          ansible_port: 2223
```

**Key variables explained:**

| Variable | Purpose |
|----------|---------|
| `ansible_host` | The IP address or hostname Ansible connects to |
| `ansible_port` | The SSH port Ansible uses to connect |

The `remote_user` and `private_key_file` are already configured in `ansible.cfg` — you do not need to repeat them in the inventory.

### Step 1.4 — Verify the File Exists

Confirm the file is in place:

```bash
ls workspace/inventory/
```

You should see `hosts.yml` listed.

### Step 1.5 — Run ARIA's Verification

```bash
make test
```

ARIA will confirm whether Phase 1 is complete before you proceed.

---

## PHASE 2: Verify Connectivity

> An inventory is worthless if you cannot reach your fleet. Every node on the registry must respond before any operation can be authorised. Run the connectivity check — confirm every ship is online.

### What You Are Doing

You will use Ansible's `ping` module to verify that Ansible can connect to each node over SSH. This is not an ICMP ping — it is an Ansible-specific check that confirms:

1. SSH connectivity is working
2. Python is available on the remote host
3. Ansible can execute commands on the node

All commands in this phase are run from the `workspace/` directory.

### Step 2.1 — Change Into the Workspace Directory

```bash
cd workspace
```

You must be in `workspace/` for Ansible to find `ansible.cfg` and the inventory path it references.

### Step 2.2 — Ping the Entire Fleet

```bash
ansible all -m ping
```

**Command breakdown:**

| Part | Meaning |
|------|---------|
| `ansible` | The Ansible ad-hoc command tool |
| `all` | Target all hosts in the inventory |
| `-m ping` | Use the `ping` module |

**What success looks like:**

```
sdc-web | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
sdc-db | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
sdc-comms | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

Each host returns `SUCCESS` with a `"ping": "pong"` response. The output will be colour-coded green in your terminal.

**What failure looks like:**

```
sdc-web | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh",
    "unreachable": true
}
```

If you see `UNREACHABLE`, see the troubleshooting notes at the end of this phase.

### Step 2.3 — Ping a Specific Group

```bash
ansible web_servers -m ping
```

This targets only hosts in the `web_servers` group. You should see only `sdc-web` respond.

Try the other groups:

```bash
ansible db_servers -m ping
ansible comms_relays -m ping
```

### Step 2.4 — Troubleshooting Connectivity Failures

If any node returns `UNREACHABLE`, work through this checklist in order:

**Check 1: Are the containers running?**

```bash
docker ps
```

You should see three containers: `sdc-web`, `sdc-db`, `sdc-comms`. If they are absent, run:

```bash
make reset
```

Wait for the build to complete, then retry.

**Check 2: Is your inventory correct?**

Open `workspace/inventory/hosts.yml` and verify the port numbers match the fleet asset table in Phase 1. A single transposed digit causes connection failure.

**Check 3: Are you running from `workspace/`?**

Ansible reads `ansible.cfg` from the current directory. If you are not in `workspace/`, it will not find the configuration and may use wrong defaults.

### Step 2.5 — Run ARIA's Verification

```bash
make test
```

ARIA requires all nodes to be reachable. Do not proceed until all three pass.

---

## PHASE 3: Fleet Reconnaissance

> ARIA requires a complete intelligence picture of the fleet. Every node must be interrogated — operating system, network configuration, hardware profile. This data forms the baseline against which future anomalies will be detected. Begin the sweep.

### What You Are Doing

Ansible's `setup` module collects **facts** — system information automatically gathered from each host. This includes OS version, IP addresses, CPU count, memory, mounted disks, and hundreds of other variables.

You will gather facts across the entire fleet, then use filters to extract specific data points. Your findings will be recorded in an **intel report** that ARIA will verify.

All commands are run from `workspace/`.

### Step 3.0 — Prepare the Intel Report

Copy the report template to create your working intel file:

```bash
cp workspace/reports/fleet-intel.yml.example workspace/reports/fleet-intel.yml
```

You will fill in this file as you complete Phases 3, 4, and 5. ARIA verifies your report when you run `make test`.

### Step 3.1 — Gather All Facts

```bash
ansible all -m setup
```

This produces a large JSON output for each host. Every fact Ansible collects is listed here. The structure looks like:

```json
sdc-web | SUCCESS => {
    "ansible_facts": {
        "ansible_architecture": "x86_64",
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_version": "22.04",
        "ansible_hostname": "sdc-web",
        "ansible_memtotal_mb": 7838,
        ...
    },
    "changed": false
}
```

The facts are nested under `ansible_facts`. Each fact is a key-value pair. Some facts contain nested objects (like `ansible_default_ipv4`), others are simple strings or integers.

Scroll through the output and familiarise yourself with what is available. You will be querying specific facts in Phase 5.

### Step 3.2 — Filter for OS Information

Collecting all facts produces a lot of output. The `-a "filter=..."` argument narrows it to matching fact names. The `*` wildcard matches any suffix.

```bash
ansible all -m setup -a "filter=ansible_distribution*"
```

This returns only facts whose names begin with `ansible_distribution`. You will see:

- `ansible_distribution` — the OS name (e.g. `Ubuntu`)
- `ansible_distribution_version` — the version number (e.g. `22.04`)
- `ansible_distribution_release` — the release codename (e.g. `jammy`)

**Record your finding:** Open `workspace/reports/fleet-intel.yml` and fill in the `os` field for each node (e.g. `Ubuntu 22.04`).

### Step 3.3 — Filter for Network Information

```bash
ansible all -m setup -a "filter=ansible_default_ipv4"
```

This returns the primary IPv4 network interface information for each host. The output will include:

```json
"ansible_default_ipv4": {
    "address": "172.30.0.x",
    "gateway": "172.30.0.1",
    "interface": "eth0",
    "netmask": "255.255.255.0",
    ...
}
```

**Record your finding:** Open `workspace/reports/fleet-intel.yml` and fill in the `ip_address` field for each node (e.g. `172.30.0.11`).

### Step 3.4 — Run ARIA's Verification

```bash
make test
```

---

## PHASE 4: Ad-hoc Operations

> Agent Chmod-777 has been active. Intelligence suggests permission tampering has occurred across fleet nodes — classified data may be exposed. Conduct immediate damage assessment. Do not remediate. Observe and document only.

### What You Are Doing

Ad-hoc commands let you run arbitrary shell commands across your fleet without writing a playbook. You will use the `shell` module to interrogate each node, checking system health and locating Agent Chmod-777's tampering.

All commands are run from `workspace/`.

### Step 4.1 — Check Disk Space

Before investigating damage, establish a baseline of system health.

```bash
ansible all -m shell -a "df -h"
```

`df -h` reports disk usage in human-readable format. Review the output and note whether any node is approaching capacity. This matters — a full disk can indicate exfiltration staging or log manipulation.

**Output to look for:** The `/` filesystem usage percentage for each node.

### Step 4.2 — Verify OS Details

```bash
ansible all -m shell -a "cat /etc/os-release"
```

This reads the OS release file directly from the filesystem — a lower-level check than the Ansible `setup` facts. It confirms what operating system and version each container is running.

### Step 4.3 — Enumerate Running Services

```bash
ansible all -m shell -a "systemctl list-units --type=service --state=running"
```

This lists all active systemd services on each node. Review what is running. Look for anything that should not be present — unexpected services can indicate compromise.

### Step 4.4 — Locate Agent Chmod-777's Evidence

Agent Chmod-777's signature is `777` permissions on files that should be restricted. A permission of `777` means every user on the system — and potentially any process — can read, write, and execute the file. For classified data, this is a critical exposure.

Search for files with `777` permissions in the fleet data directory:

```bash
ansible all -m shell -a "find /opt -perm -0777 -type f 2>/dev/null"
```

**Command breakdown:**

| Part | Meaning |
|------|---------|
| `find /opt` | Search recursively under `/opt` |
| `-perm -0777` | Match files where all three permission bits (owner, group, other) include read+write+execute |
| `-type f` | Match regular files only, not directories |
| `2>/dev/null` | Suppress permission-denied errors from directories we cannot read |

You should find files under `/opt/fleet-data/`. This is Chmod-777's damage report.

**Record your finding:** Open `workspace/reports/fleet-intel.yml` and list every compromised file path in the `compromised_files` section.

### Step 4.5 — Read the Exposed Classified Files

The files Agent Chmod-777 left exposed contain sensitive fleet data. Read them:

```bash
ansible all -m shell -a "cat /opt/fleet-data/encryption-keys.txt"
```

Review the content. Document what you find. This is the intelligence that Chmod-777 left unprotected.

**Why 777 permissions are dangerous:**

On a properly secured system, sensitive files should be readable only by the owning process or user — typically permissions like `600` (owner read/write only) or `640` (owner read/write, group read). With `777`:

- Any local user can read the file — including compromised service accounts
- Any local user can modify or overwrite the file — allowing data tampering
- Any local user can execute the file — if it contains commands, it becomes a weapon
- Backup tools, log aggregators, and monitoring agents may inadvertently transmit the content

A single misconfigured permission on an encryption key file can invalidate the security of every system that key protects.

### Step 4.6 — Run ARIA's Verification

```bash
make test
```

---

## PHASE 5: Filtered Facts

> ARIA requires a targeted intelligence report — not raw data, but specific variables extracted from every node. Memory capacity, processor configuration, network addresses. Precision is doctrine. Extract only what is needed.

### What You Are Doing

You have already used `filter` in Phase 3 to narrow `setup` output. In this phase, you will use it systematically to extract specific variables and build a targeted picture of fleet resources.

All commands are run from `workspace/`.

### Step 5.1 — Memory Per Node

```bash
ansible all -m setup -a "filter=ansible_memtotal_mb"
```

This returns the total physical memory in megabytes for each node. Record the value for each host.

**Record your finding:** Calculate the total memory available across the entire fleet by adding the three values together. Record the sum in `workspace/reports/fleet-intel.yml` under `fleet_memory_total_mb`.

### Step 5.2 — CPU Information

```bash
ansible all -m setup -a "filter=ansible_processor*"
```

The `*` wildcard matches all facts beginning with `ansible_processor`. You will see facts including:

| Fact | Meaning |
|------|---------|
| `ansible_processor_count` | Number of physical CPU sockets |
| `ansible_processor_cores` | Cores per physical CPU |
| `ansible_processor_vcpus` | Total virtual CPUs available |
| `ansible_processor` | List of processor identifiers |

Note the vCPU count for each node. This tells you the parallel processing capacity available.

### Step 5.3 — All IPv4 Addresses

```bash
ansible all -m setup -a "filter=ansible_all_ipv4_addresses"
```

Unlike `ansible_default_ipv4` which returns a single interface, this fact returns a list of every IPv4 address assigned to the host. Nodes with multiple network interfaces will show multiple addresses.

Compare this output to what you saw in Phase 3, Step 3.3. Are there differences? Some nodes may be connected to more than one network.

### Step 5.4 — Understanding the Filter Parameter

The `filter` parameter accepts:

- **Exact fact names**: `filter=ansible_hostname` — returns only that one fact
- **Wildcard patterns**: `filter=ansible_processor*` — returns all facts matching the prefix
- **No filter**: omit the `-a` argument entirely — returns all facts (hundreds of variables)

This is essential knowledge for writing efficient Ansible playbooks. When a playbook only needs one or two facts, gathering all facts is wasteful. The `gather_subset` and `gather_facts` options in playbooks build on the same principle.

### Step 5.5 — Optional: Explore Further

If you want to practice, try these additional filters and examine the output:

```bash
# Hostname of each node
ansible all -m setup -a "filter=ansible_hostname"

# All network interfaces
ansible all -m setup -a "filter=ansible_interfaces"

# System uptime
ansible all -m setup -a "filter=ansible_uptime_seconds"

# Kernel version
ansible all -m setup -a "filter=ansible_kernel"
```

### Step 5.6 — Final ARIA Verification

When you are satisfied with your reconnaissance, run the full verification suite:

```bash
make test
```

ARIA will execute all phase checks and report final mission status. All phases must pass for the mission to be considered complete.

---

## MISSION COMPLETE — DEBRIEF CHECKLIST

Before closing this mission, confirm the following:

- [ ] `workspace/inventory/hosts.yml` exists and contains all three fleet nodes
- [ ] All three nodes respond to `ansible all -m ping` with `SUCCESS`
- [ ] `workspace/reports/fleet-intel.yml` contains OS and IP for every node
- [ ] You have located Agent Chmod-777's 777-permission files and recorded them in the intel report
- [ ] You have read the exposed classified file content
- [ ] You have calculated total fleet memory and recorded it in the intel report
- [ ] `make test` reports all phases passing

If any item is incomplete, return to the corresponding phase and complete it before closing the mission record.

---

*SDC Cyber Command — 2187 — CADET EYES ONLY*
