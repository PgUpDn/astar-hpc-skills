# A*STAR HPC Skills

Reusable agent skills for A*STAR researchers working with ACRC Orion and NSCC ASPIRE2A. Community-maintained guidance; not an official A*STAR, ACRC or NSCC publication.

| Skill | System | Capabilities |
|---|---|---|
| [acrc-hpc](skills/acrc-hpc/SKILL.md) | ACRC Orion and HPC · Slurm | Account and partition discovery on both ACRC systems, SSH key diagnosis, CPU/GPU jobs, storage, containers, cron, transfers and institutional LLM gateways |
| [nscc-hpc](skills/nscc-hpc/SKILL.md) | NSCC ASPIRE2A · PBS Professional | Connection setup and relayed access, projects and charging, queue limits and resource-based routing, CPU/GPU/array jobs, bulk transfers, headless FreeCAD/gmsh, crash solvers, portals and inference services |

## Install

Clone this repository, then copy the skill folders into your agent's supported skills directory. For Codex:

```bash
git clone https://github.com/PgUpDn/astar-hpc-skills.git
mkdir -p ~/.codex/skills
cp -R astar-hpc-skills/skills/acrc-hpc ~/.codex/skills/
cp -R astar-hpc-skills/skills/nscc-hpc ~/.codex/skills/
```

If those folders already exist, review and merge or back them up before copying. Other agents that support `SKILL.md` can use the same folders in their own skill location.

## Configure for your account

Obtain your approved login host, access method, username, charging project and storage paths from your institution. Configure local SSH aliases such as `acrc` and `nscc`; these names are examples, not preconfigured connections. Never commit your real SSH configuration or credentials.

Templates intentionally contain `REPLACE_*` fields. Replace all of them, review resources and commands, and verify current account permissions before submission. Scheduler directives do not expand shell variables. Slurm and PBS are different schedulers: use the skill for the actual destination.

Examples:

- “Use $acrc-hpc to inspect my account and prepare a one-GPU Slurm job.”
- “Use $nscc-hpc to prepare a PBS array for these input files.”
- “Use $nscc-hpc to verify my completed job and transfer its outputs.”
- “用 $acrc-hpc 检查我的项目配额，并准备 CPU 作业脚本。”

Preparing a script does not submit it. A request to run or submit permits the requested execution; the skills preserve that distinction.

## Sources and validation

Adapted from operational skill notes and dated NSCC training-guide summaries. Personal identifiers, project records, credentials, private addresses and account-specific entitlements are excluded. Original manuals and private logs are not redistributed. See each skill's source notes for provenance and limits.

Cluster settings change. Historical examples are not promises of current access, capacity, charging rates or installed versions. Check the active scheduler and current institutional guidance.

The source skills were retrieved from the two clusters on 2026-10-06. The NSCC remote copy matched the local reference copy byte for byte.

Updated 2026-11-20 with dated operational observations: NSCC queue limits, resource-based routing and default charging (2026-10-10), relayed access and engineering workflows (October-November 2026), the separate older ACRC HPC cluster and SSH key diagnosis (2026-11-20), and ACRC cron and Apptainer defaults (November 2026). Account identifiers, balances, private paths and addresses remain excluded.

Validation covers skill metadata, local links, shell syntax, helper behavior and publication hygiene. It does not establish live scheduler acceptance or workload correctness; no real compute jobs are submitted for validation.

Run the offline helper checks from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## License

[MIT](LICENSE) for this repository's skill instructions and helpers. Referenced institutional manuals and services retain their own terms and are not included.
