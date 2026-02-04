---
name: open-research
description: Research and compile information on topics marked with `#open-research` tags. Provides sources, current state analysis, domain applications, and key players.
---

# Open Research Skill

This skill helps you conduct thorough research on topics identified as needing investigation.

## When to Use This
When you encounter text marked with `#open-research` tags in notes, use this skill to:
- Find 2-3 high-quality sources to jumpstart research
- Summarize the current state of the concept
- Identify how it's applied in other domains
- List key players (companies, academics, institutions)

## Instructions

**For each #open-research tag:**

1. **Create a section** with Heading 3 (###) using the research topic name
2. **Note the source**: Write which note file contained this tag
3. **Understand context**: Read the surrounding text to understand what needs research
4. **Provide comprehensive summary**: Based on your knowledge, provide thorough information about the topic including:
   - Current state of the concept/technology
   - Applications in different domains
   - Key players (companies, researchers, institutions)
   - Relevant sources or references you're aware of
5. **Note limitations**: If you need current information beyond your training data, indicate what should be searched for

## Output Format

```markdown
### [Research Topic Name]
Source: [Note filename where tag was found]

[Brief summary of current state]

**Applications:** [How it's being used in different fields]

**Key Players:** [Companies, researchers, institutions involved]

**Sources:**
- [Source 1 with link]
- [Source 2 with link]
- [Source 3 with link]
```

## Example

```markdown
## Quantum Error Correction
Source: quantum-computing.md

Quantum error correction is actively developing with surface codes showing most promise for near-term quantum computers. Current implementations achieve error rates of ~0.1% per gate.

**Applications:** Being applied in quantum computing, quantum communication, and quantum sensing systems.

**Key Players:** IBM (transmon qubits), Google (Sycamore processor), IonQ (trapped ions), academic groups at MIT, Caltech, and University of Chicago.

**Sources:**
- https://arxiv.org/abs/2023.xxxxx - Recent review of surface codes
- https://research.ibm.com/blog/quantum-error-correction - IBM's approach
- https://www.nature.com/articles/... - Experimental demonstration
```