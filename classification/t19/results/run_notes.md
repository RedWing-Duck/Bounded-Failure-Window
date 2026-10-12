# Task 19 recorded run: notes

- Commit: 8cb8777 (artifacts). G1-G7 ran once at 06:39 UTC (results/t19_checks.json, t19_checks.log).
- Part C, first launch at 06:40:31 UTC under the session's background-command tool, whose limit (2 h) is shorter than the H-13.D
  replay (about 7 h). Both jobs were stopped at 06:41 UTC: H-6.C5 had completed (its result is kept; it is not re-run), H-9.2 had
  started and was stopped before writing anything; the H-13.D replay had reached t10_realize.py in its fresh worktree and was stopped
  before writing any result. Relaunched detached (setsid nohup) on the same commit: t19_routes.py for every ID except H-6.C5, and
  h13d_replay.py from the start.
