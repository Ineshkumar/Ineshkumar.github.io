# 2026 Drafts

Place your topic drafts for 2026 here. Use the template below to write each topic as a markdown file.

---

## How this preview works
The site can preview `README.md` and other markdown files from `year-drafts/<YEAR>/` inside a modal. The preview area is rendered on a white card (so screenshots and code blocks remain readable) — this does not change the rest of the site's dark UI.

To preview updates live, serve the site over HTTP (for example `python3 -m http.server`) and open `http://localhost:8000` in your browser. When opening `index.html` via `file://` the browser will block fetching local files and previews won't appear.

Images referenced below should be placed under `year-drafts/2026/assets/` (or adjust the image paths). Example images used in the samples: `tracing-example.png` and `terraform-drift.png`.

---

# Sample Draft 1 — Observability-first deployments

**Date:** 2026-01-05  
**Summary:** Adopted end-to-end tracing and SLO-based deploy gates.

This draft describes how observability was used to make deployment decisions and protect SLOs.

## Problem
Deployments sometimes increased error rates without immediate visibility. Teams lacked high-fidelity signals to gate rollouts and identify regressions quickly.

## Diagnosis
- Traces were sampled inconsistently across services, making end-to-end traces sparse.
- Correlation IDs were missing on many async flows, so requests could not be followed across services.
- Dashboards showed aggregated metrics but lacked fine-grained request views.

## Fixes and Steps
1. Standardized tracing libraries and sampling rules across services.
2. Ensured every request carried a correlation ID and propagated it through messaging systems.
3. Added service-level SLOs and configured deploy gates that measure error budget consumption before promoting releases.
4. Integrated traces into runbooks so on-call responders can jump straight into failing traces.

### Commands and checks
```bash
# verify tracing collector is reachable
curl -fsS http://tracing.local/api/health || echo "tracing collector unreachable"
```

### Screenshot (example tracing UI)
![Tracing UI example](assets/tracing-example.png)

### Notes
- Keep sampling rates conservative for cost control, but ensure important endpoints are sampled at higher rates.
- Document where correlation IDs are injected and how to query traces using those IDs.

---

# Sample Draft 2 — Terraform drift at scale

**Date:** 2025-06-10  
**Summary:** Lessons from managing 1000+ workspaces.

Managing Terraform at scale revealed gaps in drift detection and state hygiene.

## Problem
Drift accumulated due to manual changes, out-of-band fixes, or long-lived branches that made ad-hoc changes directly in the cloud console.

## Diagnosis
- No consistent automated scanning for drift.
- Teams sometimes used local state snapshots to apply emergency fixes, bypassing the canonical IaC pipeline.
- Lack of guardrails and policy enforcement allowed configuration drift to persist.

## Fixes and Steps
- Introduced scheduled drift scans across all workspaces and reported them into a central dashboard.
- Added automated reconciler jobs that either auto-correct or create PRs for suspected drift, depending on severity.
- Enforced policy-as-code (e.g., OPA) to block changes that violate constraints.

### Commands
```bash
# run a local plan to check for changes
terraform init && terraform plan -out=tfplan
terraform show -json tfplan | jq '.'
```

### Screenshot (drift dashboard)
![Terraform drift dashboard](assets/terraform-drift.png)

### Notes
- When introducing reconciler jobs, start with alert-only mode before enabling automatic remediation.
- Keep drift reports small by filtering to meaningful diffs and aggregating by resource kind.

---

## Template for new drafts
Copy the following front-matter into a new file named like `2026-issue-1.md` and fill in details:

```
---
title: Short descriptive title
date: 2026-01-05
summary: One-line summary of the problem and outcome
---

Write your notes, steps to reproduce, diagnosis, fixes, commands, and references in Markdown.
```

## Tips
- Use fenced code blocks (```) for commands and examples.
- Include small screenshots in `year-drafts/2026/assets/` and reference them as `assets/filename.png`.
- Keep each topic focused; create separate files for unrelated issues so they are easier to review and publish.
