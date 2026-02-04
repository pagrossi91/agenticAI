---
name: daily-summary
description: Create well-formatted daily summary documents from lists of created and modified files. Use when generating daily activity summaries or digests.
---

# Daily Summary Skill

Create clear, organized daily summaries of document activity.

## Document Structure

**Always use this exact format:**

```markdown
# YYYY-MM-DD Daily Summary

## Files Created Today
- [File Name](file%20name.md)
- [Another File](another%20file.md)
or
None

## Files Modified Today
- [File Name](filename.md)
or
None

## Open Research Topics
None
or
[Content from research agent]
```

## Formatting Rules

1. **Title**: Format as `# YYYY-MM-DD Daily Summary`
2. **File links**: MUST use markdown format `[Display Name](filename.md)` for Obsidian compatibility
   - Files with spaces are URL-encoded: `[My File](My%20File.md)`
3. **Bullet points**: Use `-` (dash with space) for each file
4. **Empty sections**: Write exactly "None" if no files (not "no files", not "empty", just "None")
5. **No extra sections**: Only use the three sections shown above
6. **No commentary**: Don't add summaries, descriptions, or extra text
7. **Exact output**: When given exact content to use, output it exactly as provided
