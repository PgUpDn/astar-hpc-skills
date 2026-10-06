---
name: nscc-hpc
description: Operate NSCC ASPIRE2A for A*STAR researchers using their own approved connection, including file transfers, environment and quota checks, PBS CPU/GPU job preparation, submission, monitoring, troubleshooting, and the NSCC Job/Visualization Portals. Use for NSCC, ASPIRE2A, and PBS tasks on this cluster, not generic Slurm operations on other clusters.
---

# NSCC ASPIRE2A Assistant

Use the source-guide summaries and current cluster output to complete the user's task. Keep commands and PBS scripts in ASCII punctuation. Respond in the user's preferred language.

## Read by task

| Task | Reference |
|---|---|
| SSH, password prompts, transfers, paths, and checksums | [connection.md](references/connection.md) |
| Quotas, storage, modules, CPU/GPU and interactive jobs | [jobs.md](references/jobs.md) |
| Arrays, dependencies, multiple nodes, and troubleshooting | [advanced.md](references/advanced.md) |
| Job Portal, Jupyter, remote desktops, and browser uploads | [portal.md](references/portal.md) |
| Bulk multi-TB transfers, long-lived SSH sessions, and scan jobs | [transfers.md](references/transfers.md) |
| inf-pod LLM endpoint and Claude Code on the cluster | [llm-infopod.md](references/llm-infopod.md) |
| Original PDFs, versions, page references, and conflicting guidance | [sources.md](references/sources.md) |

The reference files carry both digests of the supplied guides and operational experience recorded from live use (dated where it matters). Prefer current cluster output over either when they disagree.

Reuse the account, project, resource requirements, and authorization already established in the conversation. Distinguish connecting, transferring files, preparing scripts, and running jobs. Ask only for missing information that materially affects the outcome. Before using an existing terminal, confirm the target host, user, working directory, and whether the shell is idle.

## Site constraints

- ASPIRE2A uses **PBS Professional**. Do not default to Slurm commands such as `sbatch`, `srun`, or `#SBATCH`.
- Run computational workloads through PBS batch or interactive allocations, not on login nodes. Use suitable compute allocations for substantial builds and data movement as well. Sources: Quickstart p. 2; Theory pp. 45, 56.
- File-tree scans (`find`, `du`) over large directories are login-node load: administrators watch for them and complain. Run scans in a short CPU job such as [scan.pbs](assets/scan.pbs). See [transfers.md](references/transfers.md).
- The source environment required password authentication. Confirm the current approved method; for repeated transfers, reuse an authenticated ControlMaster where supported - see [transfers.md](references/transfers.md).
- Use the `normal` routing queue for ordinary submissions. Use `ai` when required and authorized for the project. A queue appearing in `qstat -Q` does not imply users may submit directly to it. Use reservation queues only under the applicable authorized site arrangements.
- Specify the charging project with `#PBS -P`. Visibility of several projects does not authorize choosing any one arbitrarily. Login banner balances are not necessarily current.
- Scratch and AI-node `$TMPDIR` are temporary storage. Preserve important outputs in persistent directories. Scratch is subject to purge policies; job-local temporary storage is removed after the job.
- Guide versions, resource ratios, queue limits, quotas, and SU charging rules are historical snapshots. Verify current modules, scheduler settings, and applicable announcements before execution. Identify unverified values as guidance from the supplied documents.

## Preparation, execution, and completion

Templates: [CPU](assets/cpu.pbs), [GPU](assets/gpu.pbs), [array](assets/array.pbs), and [scan](assets/scan.pbs). Replace the project, resources, workload command, and environment setup. Check input/output paths, LF line endings, ASCII hyphens, and shell syntax. Do not submit unresolved placeholders. Passing static syntax checks does not establish scheduler acceptance or computational correctness.

Requests to draft scripts or provide advice authorize preparation; requests to submit or run authorize the corresponding job execution. Respect existing authorization without asking again. Unrequested cancellation, bulk deletion, resource expansion, or resubmission is outside the default scope. Do not submit real jobs solely to test this skill.

If submission results are ambiguous, inspect existing jobs before retrying to avoid duplicates. Record the full job ID and distinguish prepared, submitted, queued, running, and successfully completed states. Verify uploaded filenames, sizes, and SHA-256 hashes when appropriate. Starting a transfer or reaching a password prompt is not completion.
