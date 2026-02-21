# SubSkills

A dynamic skill-orchestration pipeline for Gemini CLI.

## The Architecture: Sequential Pipeline

This project handles databases of 800+ skills by enforcing a **Sequential Pipeline** instead of Nested Agents.

### Execution Phases
*   **Discovery Engine:** The Discovery Phase. Analyzes requirements and identifies or generates matching skills.
*   **Dynamic Executor:** The Execution Phase. Loaded after the Discovery Phase finishes to perform the actual engineering tasks.

### Persistent Skill Cache
To handle large-scale skill sets efficiently, the system utilizes a **Persistent Skill Cache** (`.subskills_cache.json`).
*   **Recollection:** Before searching, the orchestrator checks if the objective matches a previously cached skill set.
*   **Synchronization:** Successful discovery or generation is recorded in the Cache, making future sessions instantaneous.
*   **Persistence:** The system builds a semantic map of objectives to capabilities over time.

## Usage Pipeline

**Step 1: Preparation Phase**
Instruct the main agent to identify the required skills:
> "Identify the necessary skills for: [Your Complex Task]"

**Step 2: Execution Phase**
Once the skills are identified, initialize the dynamic executor:
> "Initialize the Dynamic Executor.
> Prompt:
> REQUIRED SKILLS: [List from Step 1]
> TASK: [Execution Brief]"

## Setup
Ensure `scripts/skill_search.py` is executable.
```bash
chmod +x scripts/skill_search.py
```
