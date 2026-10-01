# CloudPilot — Project Brain

> Persistent source of truth for the CloudPilot project.

## Project Status

**Current Phase:** Phase 0 — Current State Audit

**Repository:** `cloudpilot`

**Branch:** `main`

**Purpose:** Build CloudPilot into a real self-service cloud/platform engineering platform.

---

## Status Legend

- **[CONFIRMED]** — verified directly from the current repository or environment
- **[HISTORICAL]** — previously implemented/verified but not yet re-verified
- **[PLANNED]** — intended future implementation
- **[ASSUMPTION]** — requires verification
- **[BLOCKED]** — cannot proceed until a dependency/problem is resolved

---

## Current Repository

**Windows path:**

`D:\Cloud-Pilot\cloudpilot`

**WSL path:**

`/mnt/d/Cloud-Pilot/cloudpilot`

**Git remote:**

`origin`

**Remote repository:**

`https://github.com/rxmbtw/cloudpilot`

---

## Core Vision

CloudPilot is intended to become a developer platform where a user can connect
a GitHub repository and automate application analysis, security checks,
containerization, infrastructure provisioning, deployment, monitoring,
troubleshooting, and operational workflows.

The goal is not merely to demonstrate technologies.

The goal is to understand and build the system end-to-end.

---

## Development Philosophy

CloudPilot should follow:

**Understand → Implement → Test → Break → Troubleshoot → Fix → Document**

For every important feature:

1. Understand why it exists.
2. Implement it.
3. Test it.
4. Test failure cases.
5. Troubleshoot failures.
6. Understand the root cause.
7. Fix it.
8. Document what was learned.

---

## Current Phase

### PHASE 0 — CURRENT STATE AUDIT

Before building new production infrastructure, verify the actual state of:

- Git
- Python
- virtual environment
- backend
- PostgreSQL
- Redis
- Docker
- Docker Compose
- Kubernetes
- Minikube
- Helm
- Terraform
- AWS
- GitHub Actions
- container registry
- monitoring
- security

Nothing should be considered operational merely because files exist.

---

## Immediate Principle

**Inspect first. Change second.**

Do not make architectural changes until the current state has been verified.

---

## Troubleshooting Method

When something breaks:

**Symptom → Evidence → Hypothesis → Verification → Root Cause → Fix → Prevention → Lesson**

---

## Definition of Done

A feature is not complete merely because the code works.

Where applicable, completion means:

- implementation
- tests
- linting
- security consideration
- documentation
- deployment verification
- failure-case understanding
- troubleshooting knowledge
- meaningful Git commit

---

## Next Action

Perform the Phase 0 current-state audit before implementing the next major feature.