# Environment, storage, and routine PBS jobs

Sources: Quickstart pp. 2, 7-9, 11; Theory pp. 21-23, 29-33, 38-39, 44-56; Handbook pp. 7-9, 13-28. Verify current time limits, quotas, charging rules, and modules on the cluster.

## Read-only checks

```bash
whoami
hostname
pwd
myquota
myprojects
myusage
qstat -Q
module list
module avail
```

Inspect project storage with `myquota -p PROJECT_ID`. Query historical usage with `myprojects -p PROJECT_ID -l -s YYYY-MM-DD -e YYYY-MM-DD`. Personal projects generally follow `personal-<userid>`; still use the project selected by the user.

Metadata scans over large trees (`find`, `du`, integrity checks across millions of files) are login-node load that administrators actively watch for; run them in a short CPU job with `xargs -P` on the allocated cores. Template and context: [scan.pbs](../assets/scan.pbs), [transfers.md](transfers.md). Historical notes described long CPU jobs routing from `normal` to `qlong`. Verify current routing, walltime and concurrency limits; do not submit directly to route-only execution queues.

## Storage and software

- `$HOME`: scripts, small reference files, and personal software. Obtain current guides through the institutional support portal.
- `/home/project/<project-id>`: shared data, software, and important results, subject to project permissions and validity.
- `$HOME/scratch`: temporary computational I/O. Theory p. 21 describes a 30-day purge policy. Verify the applicable timestamps and current policy; do not promise every file will remain for 30 days.
- AI-node `$TMPDIR`: storage local to each job and node. Distribute inputs separately and preserve outputs before job completion, when this storage is removed.

The guides list 50 GB for home and 100 TB for scratch; use actual `myquota` output. Install persistent software environments in home or project storage, not in scratch subject to purging.

Select actual software versions using `module avail`, `module show NAME`, and `module list`. The guides describe Cray as the default programming environment. Switch to confirmed modules such as `PrgEnv-gnu` as required. Avoid indiscriminate `module purge` or permanent `.bashrc` changes. Keep MPI libraries, compilers, and launchers compatible.

For Singularity, see Handbook p. 27 and Theory p. 50. Confirm modules and images exist. Run GPU containers within a PBS allocation using `singularity exec --nv IMAGE.sif COMMAND`, checking directory binds. Do not assume Docker daemon, sudo, or root access. Use current site modules and existing environments for Miniforge instead of copying obsolete version names.

## Script requirements

Place all `#PBS` directives before the first executable shell statement. Explicitly specify the project, queue, walltime, resources, and job name.

- `select=N:ncpus=C:mem=M:mpiprocs=P:ompthreads=T` requests N chunks. C/M/P/T are per-chunk values, not whole-job totals. A chunk does not guarantee exclusive use of a physical node. Verify placement options such as `place=scatter` when distribution across nodes is required.
- Walltime is a job-wide resource: `#PBS -l walltime=HH:MM:SS`.
- Use `cd "$PBS_O_WORKDIR" || exit 1` and check input files, output directories, and execution permissions.
- Wait for background processes with `wait` and collect their failure statuses; allowing the main script to exit can terminate unfinished work.
- Do not default to exporting the entire environment with `qsub -V`; configure modules explicitly in the script.
- PBS directives do not expand variables like ordinary shell commands. Write actual project and resource values before submission.

The `../assets/` directory provides small CPU, GPU, and array examples. Adapt them before submission. Advanced p. 150 describes a GPU resource hook assigning 16 CPUs and 110 GB memory per GPU. `select=1:ngpus=1` allows site assignment; specify `mpiprocs` according to the application. Check current hook behavior and the submitted job's `Resource_List`. GPU jobs do not invariably require `ai`; `normal` also accepts GPUs.

Interactive example; executing it allocates resources:

```bash
qsub -I -q normal -P PROJECT_ID -l select=1:ncpus=4:mem=8gb -l walltime=00:30:00
```

Wait for the compute-node shell before running computations, then exit to release resources. Do not execute this command when only preparing a proposal.

## Submission and verification

```bash
qsub job.pbs
qstat -u "$USER"
qstat -f FULL_JOB_ID
qstat -x -f FULL_JOB_ID
```

Save the full ID including its server suffix. Inspect `job_state`, `comment`, `Resource_List`, `resources_used`, `Output_Path`, `Error_Path`, and `Exit_status`, as well as application logs and expected outputs. History may have expired; the 12-hour retention in Advanced p. 27 is a document snapshot. An absent query result does not justify automatic resubmission.

Historical SU rules in Theory p. 39 charge CPU core-hours and 64 SU per GPU-hour. Submission may reserve an allocation and completion may return the unused portion. These are not guaranteed current rates; verify the project and current rules before large runs.
