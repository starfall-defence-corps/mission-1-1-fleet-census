# Mission 1.1: Fleet Inspection — Hints & Troubleshooting Guide

**Rank**: Cadet (Maximum Scaffolding)

This guide is your safety net. If something is not working, the answer is likely here. Read the relevant section carefully before asking for help.

---

## YAML Inventory Hints

**YAML uses spaces, never tabs.**
This is the most common source of errors. Your editor may insert tabs when you press the Tab key. Use 2 spaces for each level of indentation.

Bad:
```yaml
all:
	children:   # TAB character — YAML will reject this
```

Good:
```yaml
all:
  children:    # 2 spaces — correct
```

**Strings with colons may need quoting.**
Simple values like `ansible_host: localhost` are fine as-is. If a value itself contains a colon or other special characters, wrap it in quotes.

**The group structure follows this nesting order:**

```
all
  children
    group_name
      hosts
        hostname
          variable: value
```

**Minimal working inventory example** — this is a complete, valid hosts.yml:

```yaml
all:
  children:
    web_servers:
      hosts:
        sdc-web:
          ansible_host: localhost
          ansible_port: 2221
          ansible_user: cadet
          ansible_ssh_private_key_file: .ssh/cadet_key
    db_servers:
      hosts:
        sdc-db:
          ansible_host: localhost
          ansible_port: 2222
          ansible_user: cadet
          ansible_ssh_private_key_file: .ssh/cadet_key
    comms_relays:
      hosts:
        sdc-comms:
          ansible_host: localhost
          ansible_port: 2223
          ansible_user: cadet
          ansible_ssh_private_key_file: .ssh/cadet_key
```

---

## Connection Hints

**"Connection refused"**
The containers are not running. Start them with:
```
make setup
```

Then verify they are up:
```
docker ps
```
You should see `sdc-web`, `sdc-db`, and `sdc-comms` in the list.

**"Permission denied (publickey)"**
Ansible cannot find or use your SSH key. Check that the key file exists at `workspace/.ssh/cadet_key`. If the path in your inventory does not match the actual file location, correct it.

**"Host key verification failed"**
The `ansible.cfg` file in this mission already disables strict host key checking. If you are running Ansible manually outside of the project directory and hit this error, add:
```
-o StrictHostKeyChecking=no
```
as an SSH argument, or set `host_key_checking = False` in an `ansible.cfg`.

**Understanding `ansible_host` vs `ansible_port`**
- `ansible_host` is the address Ansible connects to. Because the containers expose their SSH ports to your local machine, this is always `localhost`.
- `ansible_port` is which port on localhost maps to that container's SSH service. Each container gets its own port: 2221, 2222, or 2223.

---

## Facts Hints

**Facts are returned as a large JSON structure.**
When you run `ansible hostname -m setup`, Ansible prints every fact it gathered as nested JSON. Look for the key name you need inside the `ansible_facts` dictionary.

**`filter=ansible_*` uses shell-style wildcards.**
The `*` matches any characters. So `filter=ansible_distribution` gives you only that fact, while `filter=ansible_*` gives you all facts whose keys start with `ansible_`.

Example:
```
ansible all -m setup -a "filter=ansible_distribution"
```

**Commonly useful facts for this mission:**

| Fact Key | What It Contains |
|---|---|
| `ansible_distribution` | OS name (e.g., Ubuntu, Debian) |
| `ansible_default_ipv4.address` | Primary IP address of the host |
| `ansible_memtotal_mb` | Total RAM in megabytes |
| `ansible_hostname` | The hostname as the system reports it |

**To see every available fact for a host:**
```
ansible sdc-web -m setup
```
Warning: this outputs a lot. Pipe it through `less` or `grep` if you need to search.

---

## Ad-hoc Command Hints

**The two most important flags:**
- `-m` specifies the **module**: `-m ping`, `-m setup`, `-m shell`
- `-a` specifies the **arguments** to pass to that module: `-a "df -h"`, `-a "filter=ansible_distribution"`

**The `ping` module is not ICMP ping.**
It does not send network pings. It tests whether Ansible can connect to the host, authenticate, and run Python. A `pong` response means full Ansible connectivity is confirmed.

**The `shell` module runs arbitrary commands on remote hosts.**
Use it when you need to run something that is not covered by a dedicated Ansible module:
```
ansible all -m shell -a "df -h"
ansible all -m shell -a "systemctl list-units --type=service --state=running"
ansible all -m shell -a "find /opt/fleet-data/ -perm 777"
```

**Targeting hosts and groups:**
```
ansible all -m ping             # target every host in the inventory
ansible web_servers -m ping     # target only the web_servers group
ansible sdc-web -m ping         # target one specific host by name
```

---

## WSL (Windows Subsystem for Linux) Hints

**"Ansible is ignoring my ansible.cfg"**
On WSL, Windows-mounted directories have `777` permissions by default. Ansible treats world-writable directories as untrusted and will silently ignore any `ansible.cfg` found in them.

**Quick fix — set the ANSIBLE_CONFIG environment variable:**
```
export ANSIBLE_CONFIG=$(pwd)/ansible.cfg
```
Run this from the `workspace/` directory before running Ansible commands. Add it to your `~/.bashrc` or `~/.zshrc` to make it persistent.

**Permanent fix — configure WSL mount options:**
Create or edit `/etc/wsl.conf`:
```ini
[automount]
options = "metadata,umask=22,fmask=11"
```
Then restart WSL (`wsl --shutdown` from PowerShell). This sets proper file permissions on Windows-mounted directories.

---

## General Troubleshooting

**If everything is broken and you are not sure where to start:**
```
make reset
```
This rebuilds the entire fleet from scratch. You will not lose your inventory file — only the containers are reset.

**"make: *** No targets specified" or "make: *** No rule to make target"**
You are in the wrong directory. `make` commands must be run from the project root where the `Makefile` is located — not from `workspace/`. Run `cd ..` to go back to the project root.

**If `make test` fails:**
Read the ARIA error message carefully. ARIA tells you specifically what it expected versus what it found. Fix that one thing, then run `make test` again.

**Check container status at any time:**
```
docker ps
```
All three containers (`sdc-web`, `sdc-db`, `sdc-comms`) should appear with a status of `Up`.

**Quick diagnostic sequence when something is not working:**
1. `docker ps` — are containers running?
2. `ansible all -m ping` — can Ansible reach them?
3. Check your `workspace/inventory/hosts.yml` for typos or indentation errors
4. Check `ansible.cfg` is present and points to the correct inventory path
