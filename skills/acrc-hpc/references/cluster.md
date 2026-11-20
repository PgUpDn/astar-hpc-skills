# Connection and environment discovery

Configure an SSH alias such as `acrc` with the approved login hostname, your username and your institution's authentication method. Do not copy another researcher's private addresses, identity files or aliases. Verify host-key fingerprints through an institutional channel; do not disable host-key checks.

Before using an existing terminal, verify its host, user, working directory and idle state. Reuse an authorized connection where possible. Distinguish routing errors from authentication rejection; use bounded diagnostics rather than repeated login attempts.

```bash
ssh acrc
whoami
hostname
pwd
sinfo -s
sacctmgr -nP show assoc user="$USER" format=Account,Partition,QOS,DefaultQOS
sacctmgr -nP show qos format=Name,MaxWall,MaxJobsPU,MaxSubmitPU,GrpTRES
module avail
```

Diagnose a rejected key with one verbose, non-interactive attempt: `ssh -v -o BatchMode=yes acrc true`. If the key is offered and the server answers with the same `Authentications that can continue` list, the key is not installed for that host. After the researcher logs in with the approved password flow, `ssh-copy-id -i KEY.pub ALIAS` installs it; verify with `ssh -o ControlPath=none -o BatchMode=yes ALIAS true` so a multiplexed master does not mask the result.

## More than one ACRC system

Observed 2026-11-20. Besides Orion, ACRC operates an older, separate Slurm cluster ("HPC") with its own login host. Its home directory path string matched Orion's, but it was a different filesystem: keys, dotfiles and project directories on Orion were not present there, and Orion project scratch paths did not exist. Treat each system as a separate account setup.

Snapshot of that cluster from `slurm.conf` and `sinfo` (verify before use): Slurm 20.02; 112 CPU nodes with 2 x 24 cores and about 187 GB (111 in the batch partitions, 1 interactive); 2 large-memory nodes with 4 x 28 cores and about 6 TB; 5 GPU nodes with 2 x 24 cores, about 187 GB and 8 GPUs each. Short probe jobs showed Intel Xeon Platinum 8268 (2.9 GHz) in the CPU and GPU nodes, Xeon Platinum 8276M (2.2 GHz) in the large-memory nodes, and 8 x Tesla V100-SXM2-32GB with NVLink per GPU node; Slurm itself labels the GPUs only as type `tesla`.

That cluster ran without cgroup confinement (`TaskPlugin=task/none`): a one-GPU job had `CUDA_VISIBLE_DEVICES` set, yet `nvidia-smi` listed every GPU on the node, and cores were not pinned. Do not override `CUDA_VISIBLE_DEVICES`, and match thread counts to the cores requested, or the job uses other researchers' resources. Partitions `interactive` (8 h), `express` (1 h), `normal` (3 days, default), `long` (14 days), `largemem`/`largememlong`, and `gpuexpress`/`gpu`/`gpulong`, each paired with a QoS that limits running and submitted jobs per user. PBS-style `qstat`/`qsub` exist there as Perl wrappers around Slurm; use native Slurm commands. Modules included `apptainer`, `singularity` and Python 3.11.

## Non-interactive shells and cron

`ssh acrc 'COMMAND'` runs a non-login shell that may lack module-provided tools and Slurm on `PATH`. Use `ssh acrc 'bash -lc "COMMAND"'` or absolute paths. Under cron, Slurm clients may also need `SLURM_CONF`; copy its value from an interactive login (`scontrol show config | grep -i slurm_conf`). On Orion in November 2026 `scrontab` was disabled while the user crontab worked; keep cron entries light and let them submit jobs rather than compute.

Association visibility may be restricted. Use current institutional instructions when scheduler queries are unavailable; do not guess the account.

## Historical partition examples

September 2026 source notes mention `testqueue`, `h200n`, `h200n-long`, `l40sn`, `cpun` and `ioqueue`, plus restricted partitions. These names are discovery hints, not an entitlement list. Determine current walltime, GPU type, CPU/memory ratios and QoS from:

```bash
sinfo -o '%P %a %l %D %G %c %m'
scontrol show partition REPLACE_PARTITION
scontrol show node REPLACE_NODE
sinfo -R
```

GPU nodes in those notes included H200 and L40S, with different driver versions across nodes. Inspect the allocated node's actual hardware and software before relying on compatibility. Counts, driver versions and queue availability are deliberately not frozen here.

## Storage and software

Set `ACRC_PROJECT_DIR` to your actual project storage root and inspect `df -h "$ACRC_PROJECT_DIR" "$HOME"`. On the WekaFS setup described in the source notes, querying the project directory exposes the relevant quota, while querying `/scratch` reports the entire volume. Confirm the current site's quota reporting, including file/inode limits where applicable.

Use `module avail`, `module show NAME` and `module list` to select versions. Some source environments required sourcing `/etc/profile.d/modules.sh` to expose `module`; only do so if that file exists. A CUDA module may set `CUDAROOT` without updating `CUDA_HOME`: inspect both, verify `nvcc`, and set `CUDA_HOME="$CUDAROOT"` only when that is the chosen toolkit. Avoid inheriting a stale toolkit path.

Keep project environments and caches in approved storage. Do not replace existing cache directories or shell startup files as a side effect of routine job preparation. Diagnose slow shell startup by inspecting costly module or environment initialization; apply changes only to the affected configuration.
