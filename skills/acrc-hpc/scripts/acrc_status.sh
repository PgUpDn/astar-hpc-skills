#!/bin/bash
# Read-only checks. Usage: ACRC_PROJECT_DIR=/your/project bash acrc_status.sh
set -uo pipefail
: "${ACRC_PROJECT_DIR:?Set your approved project storage path}"
[[ -d "$ACRC_PROJECT_DIR" ]] || { echo 'Project directory does not exist' >&2; exit 2; }
status=0
query() {
  printf '
%s
' "$1"
  shift
  if ! "$@"; then
    echo 'Query unavailable or failed; do not interpret this as zero usage/access.' >&2
    status=1
  fi
}
query 'Account associations' sacctmgr -nP show assoc user="${USER:?}" format=Account,Partition,QOS,DefaultQOS
query 'QoS limits (match these to your associations)' sacctmgr -nP show qos format=Name,MaxWall,MaxJobsPU,MaxSubmitPU,GrpTRES
query 'Project and home storage' df -h "$ACRC_PROJECT_DIR" "$HOME"
query 'Your jobs (array tasks expanded)' squeue -r -u "$USER" -o '%.18i %.12P %.28j %.8T %.10M %.10l %R'
query 'Visible partitions (visibility does not imply permission)' sinfo -o '%P %a %l %D %G %c %m'
query 'Unavailable nodes and reasons' sinfo -R
exit "$status"
