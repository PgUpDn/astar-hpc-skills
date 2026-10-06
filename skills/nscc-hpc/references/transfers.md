# Bulk transfers and reusable SSH sessions

Large data movement and metadata scans should use approved transfer facilities or scheduler allocations. Historical operational notes found institutional cluster-to-cluster routes more reliable than home/VPN routes for large transfers. Test authorized reachability in the required direction; do not assume symmetry or embed private IP addresses.

## Reuse authentication

Where OpenSSH multiplexing is permitted, create a master in a visible terminal and let the researcher authenticate. Keep the socket in a private directory:

```bash
mkdir -p "$HOME/.ssh/control"
chmod 700 "$HOME/.ssh/control"
ssh -M -N -f -o 'ControlPath=~/.ssh/control/%C' -o ControlPersist=600 \
  -o ClearAllForwardings=yes nscc
ssh -o 'ControlPath=~/.ssh/control/%C' -o BatchMode=yes \
  -o ClearAllForwardings=yes nscc true
```

Socket existence alone does not prove authentication or responsiveness. Check a bounded remote command. Reauthenticate if the connection is dead; avoid repeated password attempts. Use the same local alias and options for subsequent commands and transfers. Respect the server's concurrent-session limit and leave room for monitoring. Do not terminate a master shared by another task.

## Transfer method

Use resumable `rsync` for ordinary directory transfers. For millions of small files, tar streams grouped into independent batches can reduce per-file protocol overhead. Choose concurrency based on site policy and measured load, not a fixed maximum. Quote paths, preserve relative paths and use `set -o pipefail` so local archive failures are not hidden by a successful remote extraction. Tar extraction can overwrite files: use a dedicated destination or review conflicts first.

Keep separate error logs and exit statuses for every stream. Explicitly wait for background workers. An exact completion marker may help monitoring, but it is not integrity verification. Avoid whitespace-splitting loops such as `for f in $(ls)`; use null-delimited file lists.

macOS and Linux may ship different rsync implementations; check supported flags locally. Do not assume GNU `timeout` is installed on macOS.

## Verification

For small or critical datasets, compare relative paths, sizes and cryptographic hashes. For huge datasets, run a staged manifest comparison under allocations: exact path/count checks, sizes, then hashes as required. File counts and approximate directory sizes cannot prove identical contents. Report unreadable or missing files explicitly rather than claiming a complete copy.

The [scan template](../assets/scan.pbs) produces a deterministic per-entry inventory and fails on unreadable trees. It is a metadata check, not a checksum comparison. Run intensive scans in PBS; do not start duplicate full-tree scans on login nodes.
