# Local AI Agent Harness: Specification-Driven Development (SDD)

A production-grade, modular AI agent harness engineered to execute code reviews and file adjustments using local, open-source models. This architecture transitions from standard prompt engineering into an automated, environment-aware software loop built on **Specification-Driven Development (SDD)** paradigms.

---

## Repository Architecture

The codebase is strictly structured to decouple framework orchestration from the agent's file system sandbox. This architecture enforces safe system contexts and logical state barriers:

```text
sdd-agent-harness/
│
├── core/                  # Engine Logic & Infrastructure
│   ├── __init__.py        # Package initialization
│   ├── tools.py           # Regex parsers, system tools, and sandboxing rules
│   └── engine.py          # Ollama turn loop and structural prompt contexts
│
├── workspace/             # AI Sandbox (Agent's operation directory)
│   ├── specs.md           # System requirements and product features (Read-Only)
│   └── tasks.md           # Incremental task-tracking checklist (Read-Write)
│
├── assets/                # Deployment images and runtime verification logs
├── main.py                # System bootstrap script and environment initiator
└── README.md              # Project specifications and overview
```

---

## Architectural Evolution

### 1. Static Prompt Context Wrapper (`agent.py` / Initial Phase)
The initial stage instantiated a controlled context wrapper using the local `llama3.2:3b` model. By locking the conversation history array with explicit system instructions, the framework eliminated unpredictable conversational behaviors. It successfully identified vulnerable SQL strings locally, showing high prompt-adherence capability without sending code to cloud-dependent networks.

### 2. Autonomous Tool-Calling Turn Engine (`main.py` / Current Phase)
The mature architecture abstracts tool interfaces using programmatic JSON-schema structures. The harness acts as a state router: it intercepts the local model's requests, matches them against safe system execution routines, manipulates file markers (updating `- [ ]` checklist entries to `- [x]`), and returns real-time console feedback directly to the model's memory.

---

## Quick Start Configuration

### Hardware & Stack Requirements
* **Inference Core:** Ollama Client Environment
* **Engine Model:** `llama3.2:3b` or `qwen2.5-coder:7b`
* **Programming Layer:** Python 3.14+ (or equivalent runtime environment)

### Local Launch Procedure
1. Verify your local Ollama server instance is actively hosting the engine:
   ```cmd
   ollama run llama3.2:3b
   ```
2. Run the main execution wrapper from the root path:
   ```cmd
   py main.py
   ```
