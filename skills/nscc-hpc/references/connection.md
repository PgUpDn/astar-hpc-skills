# Connections and small transfers

Use your approved institutional/VPN access and configure an SSH alias such as `nscc` with your own username and the host supplied by NSCC. Confirm the current authentication method. Historical source sessions required passwords; this is not a permanent statement of server policy.

```bash
ssh nscc
```

Let the researcher authenticate in a visible terminal or approved credential flow; never request a password in chat or store it in the skill. Verify host keys through the institution. Before reusing a terminal, check target host, user, directory and whether the shell is idle. Do not inject commands into an editor, prompt or running program.

A pre-authentication reset does not establish a bad password or VPN failure. Authentication rejection means the server was reached. A forwarding conflict can often be avoided with `-o ClearAllForwardings=yes` for the particular transfer. Do not terminate shared forwards. Broken pipes/timeouts require checking whether the session is still alive before continuing.

```bash
# Use the intended remote destination and real local paths.
ssh -o ClearAllForwardings=yes nscc 'mkdir -p ~/incoming'
scp -o ClearAllForwardings=yes './guide.pdf' nscc:incoming/
rsync -av --partial -e 'ssh -o ClearAllForwardings=yes' ./input/ nscc:incoming/input/
```

Avoid destructive synchronization options by default. Verify SHA-256 checksums for important transfers. A successful connection or started upload is not transfer completion. For large datasets, repeated connections and verification scans, read [transfers.md](transfers.md).
