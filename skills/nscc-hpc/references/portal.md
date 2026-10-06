# Job and Visualization Portals

Source: Portal v1.3, 2024-03-26. URLs and fields reflect that version; inspect the actual page and do not assume authentication state.

| Network | Job Portal | Visualization Portal |
|---|---|---|
| A*STAR | https://astarjobportal.nscc.sg | https://astarvisual.nscc.sg |
| NSCC VPN | https://jobportal.nscc.sg | https://visual.nscc.sg |

Other institutional endpoints appear on pp. 5-6. Let the user authenticate on the page.

- **Submission, pp. 8-13:** use an input file's Process with action, an existing Profile, or the Job Submission Form. Supply the project, walltime, resources, and paths, then act within the user's submission authorization.
- **WebApps/Jupyter, pp. 14-16:** select an available template and wait for allocation and Ready state before opening. Queued does not mean available.
- **Monitoring, pp. 18-23:** inspect Job Information and input/output files under Jobs. Completion still requires checking application logs.
- **Desktops, pp. 25-35:** create, wait for, and open a session in the Visualization Portal. Release allocations when no longer needed. Share desktops only when explicitly requested.
- **Files, pp. 37-40:** navigate Files or enter the destination path, create folders, and upload the specified files. Verify names, sizes, and hashes when appropriate.
- **Profile/App Composer, pp. 42-45:** create reusable definitions when requested, preserving required fields such as project and walltime.

Both portal submission and qsub create real PBS jobs. Do not submit another copy through SSH merely to verify a portal submission.
