---
name: obsidian-integration
description: Generate daily summaries of Obsidian vault activity
triggers:
  - "obsidian"
  - "daily summary"
  - "vault summary"
requires_tool: obsidian_tool
---

# Obsidian Integration

This workflow invokes `tools/ObsidianTool.py` which orchestrates the daily summary generation.

The tool handles:
- Scanning vault for files created/modified today
- Extracting #open-research tags
- Calling doc_agent and research_agent with appropriate skills
- Writing the final summary to your vault