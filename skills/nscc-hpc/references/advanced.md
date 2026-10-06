# Arrays, dependencies, multiple nodes, and troubleshooting

Sources: Advanced pp. 27-44, 47-53, 74-75, 81-83, 105-107, 117-131, 150-163, 166-168.

## Arrays and dependencies

For independent tasks with identical resource requirements, use `#PBS -J 1-10` and choose inputs with `$PBS_ARRAY_INDEX`. The concurrency-limited form is `-J 1-10%2`; confirm support in the current qsub. Do not reproduce the typesetting space on p. 130 as a separate argument. Give each subjob independent outputs and account for resources per subjob. Interactive arrays using `qsub -I -J` are not supported.

```bash
qstat -t '1234[].pbs101'
qstat -f '1234[2].pbs101'
qsub -W depend=afterok:REAL_UPSTREAM_JOB_ID downstream.pbs
```

Quote IDs containing brackets. A finished parent array does not establish success of every subjob. `afterok` requires upstream success; `afterany` accepts either outcome; `afternotok` is for failure follow-up. Separate multiple upstream IDs with colons. Save actual upstream IDs and never submit dependents using an empty ID. A dependent job's H state may be expected; do not release it automatically.

## MPI, GPU, and AI jobs

- Match MPI ranks and OpenMP threads per chunk to the allocation and application parallelism. Select mpirun/mpiexec for the actual MPI module. Do not assume `$MPI_NPROCS` is always defined automatically.
- Inspect `$PBS_NODEFILE`; do not hard-code nodes belonging to other jobs. A chunk does not guarantee an exclusive node.
- Preserve PBS-assigned `CUDA_VISIBLE_DEVICES`. Advanced pp. 151-152 describe a helper environment file for multiple nodes. Where present and applicable, use `source "${PBS_NODEFILE}.env"` on the appropriate nodes. Do not blindly broadcast the primary node's bindings or expose all host GPUs.
- The ai queue needs project permission and may use `pbs102`. Query `qstat -a @pbs102` or the full job ID. Do not resubmit merely because the default server does not show the job.
- `$TMPDIR` is node-local, not shared storage. Distribute inputs per node and persist outputs before the allocation ends.

## Troubleshooting

1. Submission rejected: retain the original error and check project, balance, validity, routing queue permission, resource combinations, select syntax, executable commands, ASCII punctuation, and line endings.
2. Q: inspect comments, resource requests, and queue state. Waiting can result from resource scarcity, user limits, or scheduler priority; do not repeatedly submit the same task.
3. H: inspect Hold_Types, dependencies, and failure history. Use qrls only when the cause is understood and release is authorized.
4. W/E: inspect requested start time, stage-in/out, output directory permissions, and logs. Collect evidence for server-side issues rather than modifying cluster services.
5. Failed or finished: inspect Exit_status, requested versus used resources, stdout/stderr, memory or walltime limits, and application outputs. Interpret nonzero codes in both PBS and application context.

```bash
qstat -anstw
qstat -f FULL_JOB_ID
qstat -x -f FULL_JOB_ID
qstat -f -F json FULL_JOB_ID
```

Cancel, hold/release, change resources, or resubmit only the specific authorized jobs. qdel is not a diagnostic test. When support is needed, collect job ID, time, host, resources, and errors. Do not send email unless requested.
