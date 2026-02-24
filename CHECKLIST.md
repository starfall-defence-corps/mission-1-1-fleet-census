# Mission 1.1: Fleet Census — Progress Tracker

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
- [ ] Identified OS of each node
- [ ] Identified IP address of each node

---

## Phase 4: Ad-hoc Operations

- [ ] Checked disk space across fleet
- [ ] Listed running services via `systemctl`
- [ ] Found Agent Chmod-777's 777-permission files in `/opt/fleet-data/`
- [ ] Read the exposed classified files

---

## Phase 5: Filtered Facts

- [ ] Used `setup` filter to extract specific facts
- [ ] Calculated total fleet memory

---

## Verification

- [ ] `make test` — all ARIA checks pass
