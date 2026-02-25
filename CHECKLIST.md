# Mission 1.1: Fleet Inspection — Progress Tracker

**Rank**: Cadet
**Mission Progress**: 1 of 5 toward Ensign

Check each item off as you complete it. If a phase is blocked, see `docs/HINTS.md`.

---

## Phase 1: Asset Registry

- [ ] Created inventory file at `workspace/inventory/hosts.yml`
- [ ] All 3 fleet nodes listed (`sdc-web`, `sdc-db`, `sdc-comms`)
- [ ] Hosts organized into groups (`web_servers`, `db_servers`, `comms_relays`)
- [ ] Connection variables set (`ansible_host`, `ansible_port`)

---

## Phase 2: Connectivity

- [ ] `ansible all -m ping` returns SUCCESS for all nodes
- [ ] Can target specific groups (e.g., `ansible web_servers -m ping`)

---

## Phase 3: Reconnaissance

- [ ] `ansible all -m setup` returns facts for all nodes
- [ ] Recorded OS of each node in `workspace/reports/fleet-intel.yml`
- [ ] Recorded IP address of each node in `workspace/reports/fleet-intel.yml`

---

## Phase 4: Ad-hoc Operations

- [ ] Checked disk space across fleet
- [ ] Listed running services via `systemctl`
- [ ] Found Agent Chmod-777's 777-permission files in `/opt/fleet-data/`
- [ ] Recorded compromised file paths in `workspace/reports/fleet-intel.yml`
- [ ] Read the exposed classified files

---

## Phase 5: Filtered Facts

- [ ] Used `setup` filter to extract specific facts
- [ ] Calculated total fleet memory and recorded in `workspace/reports/fleet-intel.yml`

---

## Verification

- [ ] `make test` — all ARIA checks pass
