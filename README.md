# SubSkills

> A high-performance, dynamic skill orchestration pipeline for the Gemini CLI.

[![SubSkills Banner](assets/subskills.jpg)](https://github.com/hassenhamdi/subskills)

**SubSkills** is an advanced engineering extension designed to manage, discover, and generate specialized skills for the Gemini CLI. It enables the efficient use of large-scale technical libraries (800+ capabilities) without context degradation, using a persistent caching system to ensure optimal retrieval and execution.

## 🚀 Key Features

- **Sequential Skill Discovery:** Intelligent analysis of objectives to find matching technical signatures, preventing context bloat in the main session.
- **Automated Skill Generation:** Automatically creates standard-compliant skills (`SKILL.md`, scripts, and tests) when a required capability is missing.
- **Persistent Skill Cache:** A long-term memory system (`.subskills_cache.json`) that maps objectives to capabilities for instantaneous retrieval.
- **Context-Isolated Execution:** A multi-stage pipeline that keeps the main conversation history clean while executing complex tasks through specialized agents.
- **Deterministic Lifecycle Management:** A singular entry point (`subskills_pipeline.py`) manages the entire process from initial discovery to final execution reporting.

---

## 🏗 System Architecture

The orchestrator utilizes a decoupled architecture to separate discovery from execution.

| Component | Function | Description |
| :--- | :--- | :--- |
| **Discovery Engine** | `skill_search.py` | Analyzes requirements and searches the library for relevant capabilities. |
| **Pipeline Controller** | `subskills_pipeline.py` | Orchestrates the sequential flow between discovery and execution phases. |
| **Skill Generator** | `skill_forge.py` | Scaffolds new, standard-compliant skills for novel engineering requirements. |
| **Skill Cache** | `.subskills_cache.json` | A persistent mapping of project objectives to specific skill sets. |
| **Internal Manifest** | `.manifest.json` | A transient communication bridge between discovery and execution phases. |
| **Skill Library** | `skills/` | The central repository of specialized, loadable capabilities. |

---

## 🔄 Operational Lifecycle

To execute complex engineering tasks, the system follows a structured protocol:

1.  **Analysis & Discovery:** The system parses the objective and identifies the required technical capabilities within the library.
2.  **On-Demand Generation:** If matching skills are not found, the system generates new, standard-compliant components.
3.  **Cache Synchronization:** The objective-to-skill mapping is persisted in the local cache for future use.
4.  **Task Execution:** A specialized execution agent is initialized with the identified skill set to perform the work.

---

## 📦 Installation & Setup

### Automated Installation
```bash
git clone https://github.com/hassenhamdi/subskills.git
cd subskills
chmod +x install.sh && ./install.sh
```

### Manual Configuration
1. **Link Extension:** `gemini extensions link .`
2. **Enable Features:** Ensure `experimental.enableAgents: true` and `experimental.enableHooks: true` are enabled in your Gemini configuration.

---

## 🛠 Usage

Execute high-complexity tasks using the singular pipeline tool:

```bash
python3 scripts/subskills_pipeline.py "Implement a secure JWT authentication flow with Redis session management"
```

---

## 🛡 Technical Integrity
- **Context Management:** Strict isolation between discovery and execution phases to maintain session performance.
- **Persistent Mastery:** Every generated skill is stored and cataloged, building an ever-growing library of capabilities.
- **Standardized Workflows:** Enforces consistent patterns across all generated and discovered skills.
