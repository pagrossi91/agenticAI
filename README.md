# Agentic AI - Multi-Agent Orchestration System

A multi-agent orchestration system for local LLMs with web search integration. Built for analyzing stock market data and generating Obsidian vault summaries with real-time research.

## What This Does

- 📝 **Generates daily Obsidian summaries** of created/modified notes
- 🔍 **Researches topics** marked with `#open-research` tags using real web search
- 🤖 **Orchestrates multiple specialized agents** to keep context windows small
- 💰 **Free & Local** - runs on local LLMs (llama3.2) with DuckDuckGo search

## Quick Start

```bash
# Install dependencies
uv sync

# Configure your vault path in main.py (line 43)
# Then run:
.venv/bin/python main.py
```

**Output**: Creates `YYYY-MM-DD_Daily Summary.md` in your Obsidian vault with:
- List of files created/modified today
- Research summaries for any `#open-research` tags (with real web sources!)

## Architecture Overview

```
User Query
    ↓
AgentOrchestrator (routes to appropriate agent/tool)
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│  doc_agent      │  research_agent  │  general_agent  │
│  (formatting)   │  (research)      │  (fallback)     │
└─────────────────┴──────────────────┴─────────────────┘
         ↓                  ↓
    ┌─────────┐      ┌─────────────┐
    │ Skills  │      │   Tools     │
    └─────────┘      └─────────────┘
      - daily-summary   - ObsidianTool
      - markdown        - DuckDuckGoSearchTool
      - open-research
      - web-search
```

**Key Innovation**: Small, focused context windows
- doc_agent only sees formatting instructions
- research_agent only sees research + web search results
- Each agent specialized → better performance with 3B models

## Directory Structure

```
agenticAI/
├── .claude/
│   └── skills/                      # Agent Skills (Claude-compatible)
│       ├── daily-summary/
│       │   └── SKILL.md
│       ├── markdown-processing/
│       │   └── SKILL.md
│       ├── open-research/
│       │   └── SKILL.md
│       ├── web-search/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       ├── DuckDuckGoSearchTool.py
│       │       └── WebSearchTool.py
│       └── obsidian-integration/
│           ├── SKILL.md
│           └── scripts/
│               └── ObsidianTool.py
├── agents/
│   └── agents.yaml                  # Agent definitions
├── orchestrator/
│   └── AgentOrchestrator.py         # Main routing logic
├── main.py                          # Entry point
├── test_search.py                   # Test DuckDuckGo integration
└── pyproject.toml                   # Dependencies
```

## Current Agents

### doc_agent (llama3.2:3b)
**Purpose:** Format and organize markdown documents
**Skills:** daily-summary, markdown-processing
**Triggers:** document, markdown, format

Creates structured daily summaries with Obsidian-compatible links.

### research_agent (llama3.2:3b)
**Purpose:** Research topics and synthesize web search results
**Skills:** open-research, web-search
**Triggers:** research, search, investigate

Synthesizes information from DuckDuckGo search results into organized summaries with sources.

### general_agent (llama3.2:3b)
**Purpose:** Fallback for general queries
**Skills:** None
**Triggers:** None (default)

## How It Works: Obsidian Daily Summary

```
1. User: "Generate my obsidian daily summary"
   ↓
2. Orchestrator: Detects "daily summary" → obsidian-integration workflow
   ↓
3. ObsidianTool executes:
   ├─ Scans vault for files created/modified today
   ├─ Finds #open-research tags
   │
   ├─ For each tag:
   │  ├─ Calls DuckDuckGoSearchTool
   │  │  └─ Gets 5 real search results from DuckDuckGo API
   │  └─ Calls research_agent
   │     └─ Synthesizes search results into summary
   │
   └─ Calls doc_agent
      └─ Formats final document
   ↓
4. Result: Saves to vault with:
   - File lists
   - Research summaries with REAL web sources
   - Obsidian-compatible markdown links
```

## Usage
### Simply Run

```bash
# Make sure your vault path is set in main.py
.venv/bin/python main.py
```

### Testing Web Search

```bash
# Test DuckDuckGo integration
.venv/bin/python test_search.py
```

## Dependencies

**Core:**
- Python 3.10+
- ollama (local LLM inference)
- PyYAML (config parsing)
- Pydantic (validation)

**Web Search:**
- ddgs (DuckDuckGo search API)

**Optional:**
- anthropic (for Claude API integration)

### Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .

# For Claude API support (optional)
pip install -e .[claude]
```

## Configuration

### Setting Your Obsidian Vault Path

Edit `main.py` line 43:
```python
MY_VAULT_PATH = "/path/to/your/vault"
```

### Upgrading LLM for Better Quality

Edit `agents/agents.yaml`:
```yaml
research_agent:
  model: "llama3.2:7b"  # Upgrade from 3b to 7b
  skills:
    - open-research
    - web-search
```


## Extending the System

### Add a New Agent

Edit `agents/agents.yaml`:
```yaml
agents:
  financial_agent:
    model: "llama3.2:7b"
    skills:
      - financial-analysis
      - web-search
    triggers:
      - stock
      - earnings
      - financial
    system_prompt: |
      You are a financial analysis agent.
      You analyze stocks, earnings, and market data.
```

### Add a New Skill

1. Create directory: `.claude/skills/my-skill/`
2. Create `SKILL.md`:
   ```markdown
   ---
   name: my-skill
   description: What it does
   ---

   # Instructions

   Step-by-step guide...
   ```
3. Add to agent in `agents.yaml`

### Add a New Tool

1. Create `.claude/skills/my-tool/scripts/MyTool.py`:
   ```python
   class MyTool:
       def __init__(self, orchestrator):
           self.orchestrator = orchestrator

       def execute(self, query: str, skills: List[Dict], **kwargs) -> str:
           # Your logic here
           return result
   ```
2. Register in `main.py`:
   ```python
   my_tool = MyTool(orchestrator)
   orchestrator.register_tool('my_tool', my_tool)
   ```
