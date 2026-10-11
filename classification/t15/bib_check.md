# Task 15 bibliography check (from the recorded C1 run, results/t15_checks.json, artifacts commit 41d5e43)

| Item | Value |
|---|---|
| Entries in `references.bib` | 53 |
| Entries with a DOI | 46 |
| Entries marked VERIFY | 0 |
| Dangling keys (cited, not in the bib) | none |
| Unused entries (in the bib, never attached or cited) | none |
| `jazwinski1970` attached to | latency |
| `simon2006` attached to | stationary-variance, tau-relay-variance |

C1: PASS. The bibliography is the author-verified file committed at 6fb2386 (identical to the Task 15 input). This resolves
the Task 14 C9 failure (two entries unattached; DOIs not resolvable from the session): both entries are now attached and
the DOIs are the author's own checked values. DOIs were not resolved from this session.
