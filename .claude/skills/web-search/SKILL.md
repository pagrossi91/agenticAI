---
name: web-search
description: Search the web for information on any topic. Provides current information from online sources.
triggers:
  - "search"
  - "find online"
  - "look up"
  - "web search"
requires_tool: web_search_tool
---

# Web Search Skill

Use this skill to search the internet for current information, facts, and sources.

## When to Use This

When you need to:
- Find recent information not in your training data
- Look up facts, statistics, or current events
- Find authoritative sources on a topic
- Research companies, technologies, or concepts

## Instructions

**When conducting a web search:**

1. **Formulate query**: Extract the core search terms from the request
2. **Execute search**: Use the web search tool to find relevant sources
3. **Evaluate results**: Assess source quality and relevance
4. **Synthesize information**: Combine information from multiple sources
5. **Cite sources**: Always include links to sources used

## Output Format

```markdown
**Search Query:** [What you searched for]

**Summary:** [Brief overview of findings]

**Key Points:**
- [Important finding 1]
- [Important finding 2]
- [Important finding 3]

**Sources:**
- [Source 1 Title](URL)
- [Source 2 Title](URL)
- [Source 3 Title](URL)
```

## Example

```markdown
**Search Query:** Latest developments in quantum computing error correction

**Summary:** Recent breakthroughs in quantum error correction have focused on surface codes and topological qubits, with error rates improving to ~0.1% per gate operation in leading systems.

**Key Points:**
- Google achieved quantum error correction milestone with 49 qubits in 2023
- IBM developing modular quantum computers with error-corrected logical qubits
- Significant progress in real-time error decoding algorithms

**Sources:**
- [Google's quantum error correction milestone](https://blog.google/technology/research/quantum-error-correction-2023/)
- [IBM Quantum Development Roadmap](https://www.ibm.com/quantum/roadmap)
- [Nature: Advances in quantum error correction](https://www.nature.com/articles/quantum-ecc-2023)
```
