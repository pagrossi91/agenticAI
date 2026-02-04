import sys
from pathlib import Path

# Add tool paths to system path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / '.claude' / 'skills' / 'obsidian-integration' / 'scripts'))
sys.path.insert(0, str(project_root / '.claude' / 'skills' / 'web-search' / 'scripts'))

# main.py - Simple setup for non-developers
from orchestrator.AgentOrchestrator import AgentOrchestrator
from ObsidianTool import ObsidianTool
from WebSearchTool import WebSearchTool
from DuckDuckGoSearchTool import DuckDuckGoSearchTool

def setup_orchestrator(vault_path: str):
    """One function to set everything up"""
    
    # Create main orchestrator with correct skills path
    orchestrator = AgentOrchestrator(
        config_path="agents/agents.yaml",
        skills_dir=".claude/skills"
    )

    # Register tools
    obsidian_tool = ObsidianTool(vault_path, orchestrator)
    orchestrator.register_tool('obsidian_tool', obsidian_tool)

    # Use DuckDuckGo for actual web search (requires: pip install duckduckgo-search)
    # Comment out this line and uncomment the next one to use placeholder WebSearchTool
    ddg_search_tool = DuckDuckGoSearchTool(orchestrator)
    orchestrator.register_tool('web_search_tool', ddg_search_tool)

    # Alternative: Placeholder web search tool (no actual search)
    # web_search_tool = WebSearchTool(orchestrator)
    # orchestrator.register_tool('web_search_tool', web_search_tool)
    
    return orchestrator


# Usage - just change your vault path!
if __name__ == "__main__":
    # Configure your vault path here
    MY_VAULT_PATH = "/Users/paulgrossi/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault"
    
    # Setup
    orchestrator = setup_orchestrator(MY_VAULT_PATH)
    
    # Use it
    result = orchestrator.orchestrate("Generate my obsidian daily summary")
    print(result)