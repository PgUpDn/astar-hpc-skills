# Storage, containers and transfers

Job-local `/tmp`, `/var/tmp` and `/dev/shm` were private and removed at job end in the source Orion configuration. Treat them as ephemeral and confirm current behavior. `/dev/shm` consumes memory. Where supported, `localtmp` GRES reserves node-local space for scheduling but does not necessarily enforce a per-job filesystem quota; `df` may show the whole device.

For large datasets, request suitable local storage, stage only required inputs, verify transferred files and copy durable outputs back before exit. Preserve transfer failures in the job exit status. Large scans and copies should use site-approved compute or data-movement facilities. Do not remove other researchers' files to make room.

Apptainer and Pyxis/Enroot were available in the source environment; Docker daemon access was not. Verify currently supported runtimes and run containers inside allocations.

```bash
# Inside a suitable allocation; set real paths and image first.
apptainer exec --bind "$ACRC_PROJECT_DIR:$ACRC_PROJECT_DIR" "$IMAGE" COMMAND
# Add --nv for a GPU allocation when appropriate.
```

If Pyxis importing an image fails because a temporary squashfs path is missing, pre-import an image into approved project storage and use that local image. A missing site task-prolog inside the container can require a read-only bind of the relevant site directory; use administrator guidance and the exact error, not a blanket host-filesystem bind. The original workaround was CPU-tested, not evidence that every GPU container works.

Use an approved SSH alias for transfers:

```bash
rsync -av --partial -e 'ssh -o ClearAllForwardings=yes' ./input/ acrc:relative/project/input/
```

Disable irrelevant forwarding per connection instead of modifying shared SSH settings. Avoid `--delete` unless explicitly intended. Verify checksums for important files; counts and byte sizes alone are insufficient. Network reachability and DNS behavior differ between login and compute nodes. Use bounded retries and distinguish lookup, connection, TLS and authentication failures. Do not hard-code resolver addresses or bypass institutional network controls.
