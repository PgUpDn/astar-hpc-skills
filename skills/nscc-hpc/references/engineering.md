# Engineering workloads: relayed access, headless CAD/meshing, crash solvers

Patterns recorded from live engineering work in October and November 2026. Paths are placeholders; verify that every binary, image and directory you rely on still exists (`ls`, `sha256sum`) before use.

## Relayed access through another cluster

When the workstation cannot hold an NSCC password session (sleeping laptop, unstable VPN, automation that must not prompt), keep one authenticated ControlMaster on another cluster that the workstation reaches with keys, and run commands through it. The researcher opens that master once, in a visible terminal on the relay host.

```bash
ssh -o BatchMode=yes RELAY_ALIAS "ssh -o ControlPath=\$HOME/.ssh/REPLACE_SOCKET -o BatchMode=yes -o ClearAllForwardings=yes -o ConnectTimeout=30 REPLACE_USER@REPLACE_NSCC_HOST 'COMMAND'"
```

- `BatchMode=yes` on both hops makes a dead master fail fast instead of prompting. A dead master needs the researcher to re-authenticate; do not retry in a loop.
- Multi-line scripts: `... "bash -s" < script.sh`. A nested `ssh` inside a script fed through `bash -s` consumes the rest of stdin. Copy such a script to the host first and run it with `< /dev/null`.
- Files: push with `cat local | ssh RELAY_ALIAS "ssh ... 'cat > remote && sha256sum remote'"`; pull with `ssh RELAY_ALIAS "ssh ... 'tar czf - -C DIR .'" > out.tgz`. For large data, stage to the relay once and push relay -> NSCC; check which direction is reachable (NSCC login nodes may be unable to connect back). Send only what changed.
- When every command times out, check the VPN before blaming the clusters: on macOS, `route -n get INTERNAL_HOST` should name a tunnel interface (`utun*`), not the physical interface.
- From macOS, create tarballs with `COPYFILE_DISABLE=1 tar --no-xattrs ...` so AppleDouble `._*` files do not land on the cluster.
- Sandboxed agent shells may be unable to open port 22; run these commands from an unsandboxed shell.

## PBS habits

- With `#PBS -j oe` and `#PBS -o FILE`, the output file appears only when the job ends. Watch progress through application logs in the work directory and `qstat -x -u "$USER"` (`F` means finished).
- Always set `#PBS -P` (see [capacity.md](capacity.md)); routing follows the requested resources.
- Progress watchers: a single poller every 60-120 seconds that recognizes every terminal state. Avoid tight loops and parallel pollers.
- For gated submission from automation, `qsub -h` (held) records a job ID first; release it with `qrls JOBID` after recording. A held job still occupies the per-user submission count.

## FreeCAD and gmsh without a display

- Prefer the official FreeCAD Linux x86_64 AppImage, extracted (`--appimage-extract`), when results must match a desktop FreeCAD of the same version. A conda-forge build of the same FreeCAD release pulled a different OCCT version, which changes geometry kernels.
- Run `freecadcmd` through the AppImage's own environment (the variables set by `AppRun`: prefix, `PYTHONHOME`, library path, CA bundle, `QT_QPA_PLATFORM=offscreen`, a private `HOME`). Invoked bare, `freecadcmd` printed its banner and silently ran nothing.
- `freecadcmd` opens positional arguments as documents. Pass inputs through environment variables, print tracebacks, and end scripts with an explicit `raise SystemExit(rc)`: an uncaught exception could still exit 0.
- The AppImage bundles gmsh (binary, `libgmsh.so` and the Python module importable inside `freecadcmd`); use it for shell and solid meshing on compute nodes.
- Compute nodes had no usable OpenGL; Qt offscreen GUI rendering segfaulted. Render images with numpy (for example a z-buffer) instead.
- Copy before editing any FCStd that must stay unchanged. A plain headless open + `saveAs` rewrote most BREP payloads and dropped `GuiDocument.xml`; compose archives at zip level when byte identity matters.
- If tools pin absolute workstation paths, an unprivileged bubblewrap sandbox can bind a staged tree at the same path. Bind order matters: system directories read-only first, then the job home (on scratch, not under `/var`), and the staged tree last. Binding the job home before `--ro-bind /var` shadowed the PBS `TMPDIR` under `/var/tmp` and FreeCAD failed with "Read-only file system". Self-test the exact wrapper before batch use.

## Explicit crash solver (OpenRadioss family)

- As observed on 2026-10-10, the official OpenRadioss GitHub repository and release downloads returned 404 and openradioss.org redirected to a commercial product page. Check current availability and licences yourself.
- Community forks such as OpenCourant (AGPL) publish CI-built x86_64 Linux archives and Apptainer images. Verify downloads against the release digests and record the version, commit and SHA-256 you use.
- Before production, cross-check each new deck version on a short run against a trusted reference build: cycle count, minimum time step, added mass and energy histories should agree closely; contact and wall forces typically scatter by a few percent across platforms.
- Shared-memory run on one node: [crash_openmp.pbs](../assets/crash_openmp.pbs). Environment used by the solver family:

```bash
D=REPLACE_SOLVER_DIR   # unpacked distribution containing exec/, hm_cfg_files/, extlib/
export RAD_CFG_PATH=$D/hm_cfg_files OPENRADIOSS_PATH=$D
export OMP_NUM_THREADS=$NCPUS OMP_STACKSIZE=400m KMP_STACKSIZE=400m
export LD_LIBRARY_PATH=$D/extlib/hm_reader/linux64:$D/extlib/h3d/lib/linux64:${LD_LIBRARY_PATH:-}
ulimit -s unlimited
$D/exec/starter_linux64_gf -i deck.k -np 1           # -np RANKS decomposes for MPI
$D/exec/engine_linux64_gf -i deck_0001.rad -nt "$NCPUS"
$D/exec/th_to_csv_linux64_gf deckT01
```

- MPI engines need a matching Open MPI (`module avail openmpi`); check `ldd ENGINE | grep -i mpi`, run the starter with `-np RANKS`, then `mpirun -np RANKS ENGINE -i deck_0001.rad -nt THREADS_PER_RANK` inside a multi-node allocation. The container image is an alternative where Apptainer modules exist. The MPI path had not been exercised on ASPIRE2A when this was recorded.

## Agents and model APIs

Check site and project policy before running LLM agents or calling model APIs from login or compute nodes. Network reachability does not establish permission. Some projects keep agents and orchestrators on another system and submit to ASPIRE2A for computation only.
