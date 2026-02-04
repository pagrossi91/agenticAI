---
name: markdown-processing
description: Format, structure, and organize markdown documents following best practices. Use when creating or editing markdown files, especially for note-taking and documentation.
---

# Markdown Processing Skill

This skill helps you work with markdown documents following Obsidian best practices.

## When to Use This
Use this skill when you need to:
- Format markdown documents properly
- Combine or merge markdown content
- Structure notes with appropriate headings
- Create well-organized markdown files

## Markdown Best Practices

### 1. Heading Structure
- **Always start with H1 (#)** for the main title
- **Use H2 (##) for major sections**
- **Use H3 (###) for subsections**
- Don't skip heading levels (don't go from H1 to H3)

### 2. Links and Backlinks
- **Internal links**: Use markdown format `[Display Text](filename.md)`
- **External links**: Use markdown format `[Display Text](https://url.com)`
- Make link text descriptive, not just "click here"

### 3. Lists
- Use `-` for unordered lists (bullet points)
- Use `1.` for ordered lists (numbered)
- Indent nested lists with 2 spaces

### 4. Formatting
- **Bold**: Use `**text**` for important terms
- *Italic*: Use `*text*` for emphasis
- `Code`: Use backticks for code, filenames, commands
- Code blocks: Use triple backticks with language tag
  ````markdown
  ```python
  def example():
      pass
  ```
  ````

### 5. Organization
- Keep one main idea per note
- Use clear, descriptive headings
- Add blank lines between sections for readability
- Use horizontal rules (`---`) sparingly to separate major sections

## Common Tasks

### Combining Sections
When merging content from multiple sources:
1. Preserve the H1 title
2. Make each source an H2 section
3. Maintain consistent formatting
4. Remove duplicate information

### Creating Structured Documents
1. Start with clear H1 title
2. Add H2 sections for main topics
3. Use bullet points or numbered lists for details
4. Add links where content references other notes

## Example Structure

```markdown
# Main Topic Title

Brief introduction or summary.

## Section One
Content for first section with [links to related notes](related.md).

- Bullet point one
- Bullet point two

## Section Two
More content here.

### Subsection 2.1
Detailed information.

## References
- [External Source](https://example.com)
- [Another Note](another-note.md)
```

## Important Notes
- **Always validate markdown syntax** (properly closed formatting, valid links)
- **Be consistent** with formatting choices throughout the document
- **Use whitespace** to make documents scannable
- Remember this is for **Obsidian**, so internal links use `.md` extension
