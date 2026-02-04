# Agent Orchestrator

A multi-agent system for orchestrating local LLMs with specialized skills. Keeps context windows small by routing queries to focused agents.

## Architecture Overview

```
User Query → AgentOrchestrator → Routes to specialized agents → Agents use skills → Result
```

**Key Components:**
- **Agents** (agents.yaml): Define specialized LLMs with specific skills
- **Skills** (skills/*/SKILL.md): Instructions following Anthropic's Agent Skills format
- **Tools** (tools/*.py): Python code for complex operations agents can't do alone
- **Orchestrator** (orchestrator/AgentOrchestrator.py): Routes queries and manages agents

## Directory Structure

```
agenticAI/
├── agents/
│   ├── agents.yaml              # Agent definitions (models, skills, triggers)
│   ├── skills/                  # Agent Skills (following agentskills.io spec)
│   │   ├── daily-summary/
│   │   │   └── SKILL.md
│   │   ├── markdown-processing/
│   │   │   └── SKILL.md
│   │   ├── open-research/
│   │   │   └── SKILL.md
│   │   └── obsidian-integration/
│   │       └── SKILL.md
│   ├── tools/
│   │   └── ObsidianTool.py      # Obsidian vault integration
│   └── orchestrator/
│       └── AgentOrchestrator.py # Main routing logic
├── main.py                      # Entry point
└── pyproject.toml              # Dependencies
```

## Current Agents

**doc_agent** (llama3.2:3b)
- Skills: daily-summary, markdown-processing
- Purpose: Format and organize markdown documents
- Triggers: document, markdown, format

**research_agent** (gpt-oss:2b)
- Skills: open-research
- Purpose: Research topics and find sources
- Triggers: research, search, investigate

**general_agent** (llama3.2:3b)
- Skills: None
- Purpose: Fallback for general queries
- Triggers: None (default)

## Current Skills

**daily-summary**: Create formatted daily summaries with Obsidian-compatible links
**markdown-processing**: Format and structure markdown documents
**open-research**: Research topics marked with #open-research tags
**obsidian-integration**: Workflow coordinator (calls ObsidianTool)

## How It Works

### Example: Obsidian Daily Summary

1. **User**: "Generate my obsidian daily summary"
2. **Orchestrator**: Detects "obsidian" trigger → loads obsidian-integration skill
3. **ObsidianTool** executes workflow:
   - Scans vault for today's files
   - Extracts #open-research tags
   - Calls **doc_agent** with daily-summary skill → Creates document structure
   - Calls **research_agent** with open-research skill → Researches each topic
   - Calls **doc_agent** again → Combines into final document
4. **Result**: Saves `YYYY-MM-DD_Daily Summary.md` to vault

### Why Multiple Agents?

**Small context windows = Better performance with local LLMs**
- doc_agent only sees formatting instructions (not research methods)
- research_agent only sees research instructions (not formatting details)
- Each agent is focused and efficient

## Usage

```python
from agents.orchestrator.AgentOrchestrator import AgentOrchestrator
from agents.tools.ObsidianTool import ObsidianTool

# Setup
orchestrator = AgentOrchestrator(
    config_path="agents/agents.yaml",
    skills_dir="agents/skills"
)

# Register Obsidian tool
obsidian_tool = ObsidianTool("/path/to/vault", orchestrator)
orchestrator.register_tool('obsidian_tool', obsidian_tool)

# Use it
result = orchestrator.orchestrate("Generate my obsidian daily summary")
print(result)
```

Or simply run:
```bash
python main.py
```

## Agent Skills Format

Skills follow the [Anthropic Agent Skills specification](https://agentskills.io/specification):

```markdown
---
name: skill-name
description: What this skill does and when to use it
---

# Skill Title

Instructions for the agent...
```

**Benefits:**
- Portable across different agent systems
- Self-documenting
- Progressive disclosure (load only when needed)

## Adding New Agents

Edit `agents/agents.yaml`:

```yaml
agents:
  my_new_agent:
    model: "llama3.2:3b"
    skills:
      - skill-name
    triggers:
      - keyword
      - phrase
    system_prompt: |
      You are a specialized agent...
```

## Adding New Skills

1. Create directory: `agents/skills/my-skill/`
2. Create `SKILL.md` with frontmatter:
   ```markdown
   ---
   name: my-skill
   description: What it does and when to use it
   ---

   # Instructions

   Step-by-step guide for the agent...
   ```
3. Add skill name to appropriate agent in `agents.yaml`

## Dependencies

- Python 3.10+
- ollama (for local LLM inference)
- PyYAML
- Pydantic

Install:
```bash
pip install -e .
```

## Future Extensions

- FastAPI server for remote access
- n8n integration for scheduled workflows
- Additional tools (GitHub, web search, etc.)
- More specialized agents
