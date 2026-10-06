# Slurm jobs and diagnosis

Set account, partition, walltime, CPU/memory and GPU requests explicitly. Historical source notes recorded a one-hour default walltime and a per-user submitted-job cap; query current limits rather than assuming those numbers apply today.

```bash
mkdir -p logs
bash -n job.sbatch
sbatch --test-only job.sbatch
# Only when running/submitting is requested:
sbatch --parsable job.sbatch
squeue -u "$USER" -o '%.18i %.12P %.28j %.8T %.10M %.10l %R'
scontrol show job REPLACE_JOB_ID
sacct -j REPLACE_JOB_ID --format=JobID,State,ExitCode,Elapsed,MaxRSS,AllocTRES,NodeList
```

Record the submission result before any follow-up. A test-only check does not guarantee later placement or computational correctness. Missing accounting records can reflect retention or delay; do not automatically resubmit.

## CPUs, arrays and dependencies

Explicitly pass `srun --cpus-per-task="$SLURM_CPUS_PER_TASK"` or export `SRUN_CPUS_PER_TASK` for job steps; the source Slurm installation did not propagate the batch setting to steps automatically. Match thread settings to the application rather than multiplying ranks and threads beyond the allocation.

Each array task can count toward the submitted-job QoS limit, including pending tasks. A `%N` concurrency throttle limits running tasks, not the number submitted. Query the active account/QoS and account for other jobs before choosing an array size. Pack work or submit smaller windows when needed. Use `afterok` when downstream work requires success; `afterany` only when either outcome is acceptable. Use actual upstream IDs.

A `--signal=B:USR1@SECONDS` warning reaches the batch shell. Add a tested forwarding/checkpoint mechanism only if the application handles that signal; the default signal action can terminate applications. Persist checkpoints periodically, since node failures need not provide warning.

## Diagnostic patterns

| Symptom | Evidence to check | Response |
|---|---|---|
| Missing/invalid account or QoS | Association, partition access, original submission error | Use an authorized account/partition |
| Job submission limit | Current QoS limits and all submitted array tasks | Wait or restructure within the existing allocation budget |
| TIMEOUT | Requested time and checkpoint logs | Prepare a suitable walltime/checkpoint plan |
| OUT_OF_MEMORY | MaxRSS, per-step usage and memory request | Diagnose peak use before proposing resource changes |
| Truncated output, FAILED without traceback | Project quota, inode limits, exit status, stderr | Confirm storage exhaustion before altering data |
| Node-specific hang | Node state, software/driver versions, comparative logs | Record evidence; use another permitted node for an authorized retry |
| Resources/Priority pending reason | Request size, fair share, available partitions | Explain scheduling; do not duplicate submissions |

Log job ID, node, source revision, selected modules and relevant runtime versions. Successful GPU import alone does not demonstrate a completed GPU workload. After execution, check application outputs as well as scheduler state.
