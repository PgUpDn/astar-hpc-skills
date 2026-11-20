# Capacity, queues, routing and charging

Observations from `qstat -Q`, `qstat -Qf QUEUE`, `pbsnodes -a`, `myprojects` and `qstat -x -f JOBID` on 2026-10-10. They are a dated snapshot, not current limits or an entitlement. Re-measure before planning a large campaign. Limits are per job unless noted.

```bash
qstat -Q
qstat -Qf REPLACE_QUEUE | grep -E 'resources_(min|max)|max_run|from_route_only|enabled|started'
pbsnodes -a | grep -E 'resources_available\.(ncpus|mem|ngpus)' | sort | uniq -c
myprojects
myprojects -p REPLACE_PROJECT_ID
```

## Hardware snapshot

| Nodes | Cores per node | Memory per node | Notes |
|---:|---:|---|---|
| ~784 | 128 (AMD EPYC Milan) | ~440 GB | standard CPU nodes, RHEL 8.10 |
| 64 | 64 | not recorded | likely the GPU partition (not verified) |
| ~16 | 128 | 2-4 TB | large-memory nodes |

Login and compute nodes are **x86_64**. Binaries built for aarch64 (for example `linuxa64` builds made in Docker on Apple-silicon Macs) do not run here; obtain or build x86_64 binaries.

## CPU execution queues reached through `normal`

| Queue | Cores per job | Walltime | Max running per user | Typical use |
|---|---|---|---:|---|
| q1 | 1 | >2 h to 24 h | 20 | serial |
| q2 | 2-64 | >2 h to 24 h | 100 | part of one node |
| q3 | 65-127 | >2 h to 24 h | 25 | |
| q4 | exactly 128 | >2 h to 24 h | 25 | one full node |
| q5 | 129-2048 | up to 24 h | 20 | multi-node MPI |
| q6 | 2049-98304 | up to 24 h | 10 | very large MPI |
| qlong | up to 128 | >24 h to 120 h | 5 | long single-node work, no GPUs |
| qdev | up to 128 | up to 2 h | shared core cap | short tests and debugging |
| l1, l2, l3 | up to 128 | 24 h | 2 | likely the large-memory nodes (not verified) |

GPU queues and `ai` are listed separately by `qstat -Q`; confirm project access before using them.

**Routing follows the requested resources, not the `-q` you write.** Several execution queues are `from_route_only = True`. In the October 2026 observation, a script with `#PBS -q q2` and walltime of 2 h or less ran in `qdev`, while the same script with a 3 h walltime ran in `q2`. Submit to `normal` (or omit `-q`), choose `ncpus` and `walltime` for the queue you want, and confirm placement:

```bash
qstat -x -f REPLACE_JOB_ID | grep -E 'queue|Resource_List|project'
```

## Charging

`myprojects` prints granted, used and remaining SU per project. The training guides and the October 2026 observation agree on CPU core-hour = 1 SU and GPU-hour = 64 SU; verify current rules. **A job without `#PBS -P` was charged to the personal project `personal-<user>`**, not to a research project. Always write the intended project explicitly, and check `qstat -x -f` once for a new script.

## Sizing guidance

- Embarrassingly parallel work (meshing many parts, geometry checks, parameter sweeps): many single-node jobs, one block of items per job, so one failure does not sink the batch. Respect the per-user running limits above.
- Explicit crash finite-element runs: a 0.5-1M element model scaled to a few hundred MPI ranks; below roughly 1000-2000 elements per rank, communication and contact search dominate. Run a short scaling test (for example 128/256/512/1024 cores) before choosing a size. Very large jobs cost more SU and wait longer without speeding up a model of this size.
- Single-threaded CAD kernels (for example OCCT boolean operations in FreeCAD) do not get faster with more cores. Run independent builds in parallel and give each enough memory; one large B-spline surface build took about 71 minutes in a job that requested 160 GB.
