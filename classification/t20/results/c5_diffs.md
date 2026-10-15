# Task 20 C5: checks whose verdict changed between 7855e45 and the artifacts commit

Each check's own output at both commits (timing fields removed). Attribution: `c5_attribution.yaml` (manual reading).

## T15 C1: True → False

Baseline:

```
{
 "entries": 53,
 "doi": 46,
 "verify": 0,
 "dangling": [],
 "unused": [],
 "attachments": {
  "jazwinski1970": [
   "latency"
  ],
  "simon2006": [
   "stationary-variance",
   "tau-relay-variance"
  ]
 },
 "pass": true
}
```

Artifacts:

```
{
 "entries": 60,
 "doi": 51,
 "verify": 0,
 "dangling": [],
 "unused": [
  "bosov2026",
  "gotovos2013",
  "jiang2026",
  "sinopoli2004",
  "tenne2002",
  "wu2018"
 ],
 "attachments": {
  "jazwinski1970": [
   "latency"
  ],
  "simon2006": [
   "stationary-variance",
   "tau-relay-variance"
  ]
 },
 "pass": false
}
```
