---
CLASSIFICATION: CADET EYES ONLY
MISSION: 1.1 — FLEET CENSUS
THEATRE: Starfall Defence Corps Academy
AUTHORITY: SDC Cyber Command, 2187
---

# OPERATION ORDER — MISSION 1.1: FLEET CENSUS

---

## 1. SITUATION

### 1a. Enemy Forces

Voidborn operative **AGENT CHMOD-777** has infiltrated fleet infrastructure networks. Modus operandi: permission manipulation. Agent sets file permissions to `777` on classified fleet data — stripping access controls, exposing sensitive assets, creating vectors for exfiltration. Damage assessment is incomplete. Extent of compromise is unknown.

### 1b. Friendly Forces

The **Starfall Defence Corps (SDC)** fleet is currently blind. Asset registry is absent. Without a complete inventory of fleet nodes, we cannot defend, monitor, or respond. Half the fleet is uncatalogued.

### 1c. Attachments / Support

**ARIA** (Automated Review & Intelligence Analyst) is assigned to this mission. ARIA will verify your work and report compliance status.

### 1d. Operational Tool

All operations will be conducted using **ANSIBLE** — *Automated Network for Secure Infrastructure, Baseline Lockdown & Enforcement*. ANSIBLE is your primary tool for fleet automation, reconnaissance, and remediation.

---

## 2. MISSION

Conduct a full census of all fleet nodes. Build the asset registry. Establish connectivity to every node. Execute initial reconnaissance to gather fleet intelligence. Identify and document Agent Chmod-777's damage.

**End state**: Every node registered, reachable, and inspected. Compromise evidence documented.

---

## 3. EXECUTION

### 3a. Commander's Intent

The fleet cannot defend assets it cannot see. This mission establishes the foundation: a verified, complete asset registry with confirmed connectivity and a baseline intelligence profile on every node. Agent Chmod-777's tampering will be identified and logged before any remediation can proceed.

### 3b. Concept of Operations

Five sequential phases. Complete each phase before advancing. Full procedural detail is in **EXERCISES.md**.

| Phase | Task | Objective |
|-------|------|-----------|
| 1 | Build the Asset Registry | Construct ANSIBLE inventory file covering all fleet nodes |
| 2 | Verify Connectivity | Execute ad-hoc ping against all nodes; confirm zero failures |
| 3 | Fleet Reconnaissance | Gather full system facts from all nodes |
| 4 | Ad-hoc Operations | Investigate Agent Chmod-777's damage; locate 777-permission files |
| 5 | Filtered Facts | Extract targeted intelligence variables from fleet nodes |

### 3c. Fleet Assets

All nodes are accessible via SSH. Credentials are uniform across the fleet.

| Designation | Role | IP Address | SSH Port |
|-------------|------|------------|----------|
| `sdc-web` | Fleet Web Server | localhost | 2221 |
| `sdc-db` | Fleet Database Server | localhost | 2222 |
| `sdc-comms` | Fleet Communications Relay | localhost | 2223 |

**SSH User**: `cadet`
**Authentication**: SSH key located at `workspace/.ssh/cadet_key`

### 3d. Rules of Engagement

- Do not modify or delete fleet data during this mission. Observation and documentation only.
- All findings are to be reproducible. If ARIA cannot verify your work, your work is not complete.
- Agent Chmod-777's evidence must be documented before this mission is considered closed.

---

## 4. SUPPORT

| Resource | Function | Command |
|----------|----------|---------|
| **ARIA** | Verifies mission compliance; reports pass/fail per phase | `make test` |
| **HINTS.md** | Operational guidance if mission stalls | — |
| **Fleet Reset** | Rebuilds all fleet containers from scratch | `make reset` |

Run `make test` after each phase. Do not advance until ARIA confirms the phase complete.

Consulting **HINTS.md** is authorised at Cadet rank. Using available intelligence is not weakness — it is doctrine.

---

## 5. COMMAND AND SIGNAL

**Reporting**: ARIA is your automated reporting chain. Her output is your after-action record.

**Commander's Final Order**: This mission does not end until every node in the fleet is registered, reachable, and inspected. Agent Chmod-777's damage is documented. No exceptions.

Proceed to **EXERCISES.md** for phase-by-phase operational instructions.

---

*SDC Cyber Command — 2187 — CADET EYES ONLY*
