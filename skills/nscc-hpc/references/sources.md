# Sources and page index

Source digest prepared on 2026-09-19 from the five training PDFs listed below. Page references are **one-based PDF page numbers**. Original PDFs are not redistributed here; obtain current copies from NSCC or your institutional support channel. Extract relevant pages rather than loading entire manuals. Render pages when diagrams or tables matter.

| Short name | File | Version/date | Pages | Relevant sections |
|---|---|---|---:|---|
| Quickstart | ASPIRE2A-General-Quickstart-Guide.pdf | v1.3, 2024-03-06 | 12 | Policy p. 2; access pp. 4-6; environment p. 7; PBS pp. 8-9; FAQ pp. 11-12 |
| Theory | ASPIRE2A-INTRODUCTORY-WORKSHOP-THEORY-GUIDE.pdf | No explicit version date on the cover | 59 | Login pp. 17-19; storage pp. 21-23; transfers pp. 25-27; modules pp. 29-33; SU pp. 38-39; PBS pp. 44-48; containers pp. 50-51; practices pp. 53-56 |
| Advanced | ASPIRE2A-ADVANCED-JOB-MANAGEMENT-TRAINING_GUIDE.pdf | v1.4, 2025-04-08 | 178 | States pp. 27-44; resources pp. 47-59; containers pp. 60-63; exit codes pp. 81-83; dependencies pp. 105-107; arrays pp. 117-131; GPU pp. 150-156; AI pp. 158-163; troubleshooting pp. 166-168 |
| Handbook | Workshop-Handbook-ASPIRE2A.pdf | Cover v2.0, 01-02-2025; footers still show 2024-03-06 | 28 | Connection pp. 3-5; quotas pp. 7-9; transfers p. 11; environment pp. 13-17; execution pp. 18-26; containers/Miniforge pp. 27-28 |
| Portal | aspire2a-job-portal-guide.pdf | v1.3, 2024-03-26 | 48 | Endpoints pp. 5-6; submission pp. 8-13; WebApps pp. 14-16; monitoring pp. 18-23; desktops pp. 25-35; files pp. 37-40; profiles pp. 42-45 |

```bash
pdftotext -f 150 -l 152 -layout ASPIRE2A-ADVANCED-JOB-MANAGEMENT-TRAINING_GUIDE.pdf -
pdftoppm -f 150 -l 150 -singlefile -scale-to 1600 -png ASPIRE2A-ADVANCED-JOB-MANAGEMENT-TRAINING_GUIDE.pdf /tmp/nscc-gpu-page
```

Prioritize current applicable site policies and server settings, then newer guidance specific to the topic, explaining discrepancies. Simple execution exercises in the Handbook do not authorize real workloads on login nodes; Quickstart p. 2 requires the scheduler. Old versions, quotas, time limits, and history retention are not permanent facts.

Limited live checks on 2026-09-19 confirmed a successful user shell, enabled normal/ai routing queues in qstat -Q alongside execution queues, and the presence of myquota, myprojects, and myusage. These checks **did not establish any new researcher's ai access, current balance, every resource ratio, or software version**.

For current policies or software catalogs, consult https://help.nscc.sg/ or current module and scheduler output, recording the verification date. When explaining only the supplied PDFs, cite the relevant file and page.
