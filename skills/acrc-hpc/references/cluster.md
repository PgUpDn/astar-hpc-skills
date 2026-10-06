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
