# tools/obsidian_tool.py
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from urllib.parse import quote
import re

class ObsidianTool:
    """Specialized tool for Obsidian integration"""
    
    def __init__(self, vault_path: str, orchestrator):
        self.vault_path = Path(vault_path)
        self.orchestrator = orchestrator  # Reference to main orchestrator
        self.today = datetime.now().strftime("%Y-%m-%d")
    
    def get_todays_files(self) -> Tuple[List[Path], List[Path]]:
        """
        Identify files created or modified today.

        Returns: (created_today, modified_today) as lists of Path objects
        """
        created_today = []
        modified_today = []
        today_timestamp = datetime.now().date()

        for md_file in self.vault_path.rglob("*.md"):
            # Skip the daily summary files themselves
            if "Daily Summary" in md_file.name:
                continue

            stat = md_file.stat()

            # Use st_birthtime on macOS for true creation time
            # Fall back to st_ctime on other systems
            if hasattr(stat, 'st_birthtime'):
                created_date = datetime.fromtimestamp(stat.st_birthtime).date()
            else:
                created_date = datetime.fromtimestamp(stat.st_ctime).date()

            modified_date = datetime.fromtimestamp(stat.st_mtime).date()

            # A file goes in "created" if created today (even if also modified today)
            # A file goes in "modified" only if created before today but modified today
            if created_date == today_timestamp:
                created_today.append(md_file)
            elif modified_date == today_timestamp:
                modified_today.append(md_file)

        return created_today, modified_today
    
    def extract_open_research_tags(self, file_path: Path) -> List[Dict]:
        """Find #open-research tags and surrounding context"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        research_items = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if '#open-research' in line:
                # Get surrounding context
                start = max(0, i - 3)
                end = min(len(lines), i + 4)
                context = '\n'.join(lines[start:end])
                
                research_items.append({
                    'file': file_path.name,
                    'context': context,
                    'line': line
                })
        
        return research_items
    
    def execute(self, query: str, skills: List[Dict], **kwargs) -> str:
        """Main execution method called by AgentOrchestrator"""
        
        # Step 1: Gather file information
        created_files, modified_files = self.get_todays_files()
        
        file_info = {
            'created': [f.name for f in created_files],
            'modified': [f.name for f in modified_files]
        }
        
        # Step 2: Scan for research items
        research_items = []
        for file in modified_files:
            items = self.extract_open_research_tags(file)
            research_items.extend(items)
        
        # Step 3: Use doc_agent to create structure
        # Build explicit file lists with URL-encoded filenames for links
        if file_info['created']:
            created_list = '\n'.join([f"- [{name}]({quote(name)})" for name in file_info['created']])
        else:
            created_list = "None"

        if file_info['modified']:
            modified_list = '\n'.join([f"- [{name}]({quote(name)})" for name in file_info['modified']])
        else:
            modified_list = "None"

        doc_agent_query = f"""Create the daily summary for {self.today}.

Use this exact structure and content:

# {self.today} Daily Summary

## Files Created Today
{created_list}

## Files Modified Today
{modified_list}

## Open Research Topics
{('None' if len(research_items) == 0 else 'Will be added by research agent')}

IMPORTANT: Use the exact text above. Do not add extra sections or commentary."""
        
        # Find daily-summary skill
        daily_summary_skill = [s for s in skills if s['name'] == 'daily-summary']
        
        initial_summary = self.orchestrator.invoke_agent(
            'doc_agent',
            doc_agent_query,
            skills=daily_summary_skill
        )
        
        # Step 4: Use research_agent for each item with actual web search
        research_sections = []
        if research_items:
            print(f"\n📚 Found {len(research_items)} research items to process")

            # Find open-research skill
            research_skill = [s for s in skills if s['name'] == 'open-research']

            # Find web-search skill
            web_search_skill = [s for s in skills if s['name'] == 'web-search']

            for item in research_items:
                print(f"\n🔬 Researching: {item['file']}")

                # Extract search query from context (look for text around #open-research)
                context_lines = item['context'].split('\n')
                search_topic = None
                for line in context_lines:
                    if '#open-research' in line:
                        # Try to get text AFTER the tag (more likely to be the topic)
                        text_after = line.split('#open-research')[-1].strip()

                        # If text after looks promising, use it
                        if text_after and len(text_after) > 10:
                            # Remove leading "for us" or similar
                            for prefix in ['for us is to ', 'for is to ', 'for us ', 'for ']:
                                if text_after.lower().startswith(prefix):
                                    text_after = text_after[len(prefix):]
                                    break
                            search_topic = text_after

                        # Otherwise get text before the tag
                        if not search_topic:
                            text_before = line.split('#open-research')[0].strip()
                            # Look for descriptive text after keywords like "for", "about", "on"
                            for keyword in [' for ', ' about ', ' on ', ' of ']:
                                if keyword in text_before:
                                    search_topic = text_before.split(keyword)[-1].strip()
                                    break

                        # Remove markdown headers
                        if search_topic:
                            search_topic = search_topic.lstrip('#').strip()
                        break

                if not search_topic or len(search_topic) < 10:
                    # Fallback: use the file name
                    search_topic = item['file'].replace('.md', '').replace("'s", '').strip()

                print(f"   Search topic: {search_topic}")

                # Step 4a: Get actual web search results using web_search_tool
                search_query = f"Find information about: {search_topic}"
                print(f"   🌐 Calling web_search_tool...")

                try:
                    # Call the web search tool to get actual results
                    web_results = self.orchestrator.execute_tool(
                        'web_search_tool',
                        query=search_query,
                        skills=web_search_skill
                    )
                    print(f"   ✓ Got web results: {len(web_results)} chars")
                except Exception as e:
                    print(f"   ✗ Web search failed: {e}")
                    web_results = f"Web search unavailable: {e}"

                # Step 4b: Pass web results to research_agent for synthesis
                research_query = f"""Research this topic from note: {item['file']}

Context from note:
{item['context']}

Web search results:
{web_results}

Task: Synthesize the web search results into a well-organized summary with:
- Current state of the concept/technology
- Applications in different domains
- Key players (companies, researchers, institutions)
- Sources (use the URLs from the web search results)

Follow the format specified in your open-research skill."""

                print(f"   🤖 Calling research_agent to synthesize...")
                research_result = self.orchestrator.invoke_agent(
                    'research_agent',
                    research_query,
                    skills=research_skill
                )
                print(f"   ✓ Synthesis complete: {len(research_result)} chars")

                research_sections.append(f"## {item['file']}\n\n{research_result}")
        
        # Step 5: Combine into final summary
        if research_sections:
            # Replace the "Open Research Topics" section with actual research
            research_content = '\n\n'.join(research_sections)
            final_query = f"""Update the daily summary by replacing the Open Research Topics section.

Base summary:
{initial_summary}

Replace the "## Open Research Topics" section with this exact content:
## Open Research Topics
{research_content}

Keep everything else exactly the same. Output the complete updated document."""

            final_summary = self.orchestrator.invoke_agent(
                'doc_agent',
                final_query,
                skills=daily_summary_skill
            )
        else:
            # No research items, the initial summary already has "None"
            final_summary = initial_summary
        
        # Step 6: Save to vault
        output_path = self.vault_path / f"{self.today}_Daily Summary.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_summary)
        
        return f"Daily summary created at {output_path}\n\n{final_summary}"