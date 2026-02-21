---
name: subskills
description: Advanced skill for large-scale skill discovery, automated generation, and context-efficient agent orchestration.
---

# Unlimited Skill Orchestration (SubSkills)

This skill provides high-performance orchestration protocols designed to manage extensive technical libraries (800+ specialized skills) without session context degradation.

## Operational Sequence

Complex engineering tasks are executed through a deterministic multi-stage pipeline:

`python3 scripts/subskills_pipeline.py "[Objective]"`

### Architectural Phases:
1.  **Analysis & Discovery:** Systematic identification of existing technical capabilities relevant to the objective.
2.  **Automated Generation:** Dynamic synthesis of new, standard-compliant skills when no matching capability is found.
3.  **Knowledge Persistence:** Instant retrieval of previously mapped or generated capabilities via a local knowledge cache.
4.  **Coordinated Orchestration:** Managed communication between specialized agents (Discovery and Execution) via isolated manifests.

## Key Principles
- **Context Efficiency:** The main session remains clean, receiving only high-level status reports.
- **Validation-Driven:** All generated skills include standardized test structures for reliability.
- **Scalability:** Optimized for thousands of skills through sequential, targeted discovery rather than broad context injection.

**Status:** System initialized. Ready for orchestration.
