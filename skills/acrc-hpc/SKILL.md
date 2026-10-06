---
name: acrc-hpc
description: Operate ACRC Orion for A*STAR researchers using Slurm, including account and partition checks, CPU/GPU jobs, storage, containers, transfers and institutional LLM gateway troubleshooting. Use for ACRC cluster tasks, not NSCC PBS jobs.
---

# ACRC Orion

Use the researcher's own connection, charging account and project paths. Respond in their preferred language. Historical observations in the references require current verification.

## Read by task

| Task | Reference |
|---|---|
| Login, account discovery, partitions, quotas and software | [cluster.md](references/cluster.md) |
| Slurm preparation, execution, arrays and failure diagnosis | [jobs.md](references/jobs.md) |
| Node-local staging, containers and file transfers | [storage-and-containers.md](references/storage-and-containers.md) |
| Institutional LLM endpoints, credentials and proxy diagnosis | [llm-gateway.md](references/llm-gateway.md) |
| Origin and limits of the guidance | [sources.md](references/sources.md) |

## Operating constraints

- ACRC Orion uses Slurm. Run substantive computation, builds, test suites, bulk transfers and large metadata scans in appropriate allocations; keep login-node activity light.
- Select a charging account and partition authorized for this researcher. A partition being visible does not establish access. Set walltime explicitly.
- Inspect project-directory quotas, not only whole-filesystem capacity. Preserve results outside job-local temporary storage before the allocation ends.
- Query current modules, resource ratios and QoS limits. Do not convert another account's historical permissions into defaults.
- Keep passwords and tokens out of chat, command arguments, logs and version control. Let the researcher authenticate through the approved mechanism.

## Prepare, execute, verify

Start from the [CPU](templates/cpu_job.sbatch) or [GPU](templates/gpu_job.sbatch) template. Replace every `REPLACE_*` field, choose resources and set up the workload's environment. Slurm directives do not expand shell variables. Create log directories before submission. Check shell syntax and, when appropriate, use `sbatch --test-only`; this does not run the workload.

A request to prepare permits preparation; a request to run or submit permits the corresponding execution. Do not submit real jobs merely to test the skill. Reuse authorization already established; do not expand resources, cancel other jobs or delete data without task authorization.

If submission output is ambiguous, inspect existing jobs before retrying. Save the actual job ID. Distinguish queued, running and completed; verify `sacct`, exit status, application logs and expected outputs before reporting success.

The [status helper](scripts/acrc_status.sh) performs read-only queries using an explicit project path. The [gateway helper](scripts/gateway_check.py) lists models; a model argument additionally sends one small inference request, so use that mode only within the requested scope.
