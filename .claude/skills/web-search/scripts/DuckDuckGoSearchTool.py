# tools/duckduckgo_search_tool.py
from typing import List, Dict
import json

class DuckDuckGoSearchTool:
    """Web search tool using DuckDuckGo API"""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform DuckDuckGo search and return results.

        Uses ddgs library (pip install ddgs)
        """
        try:
            from ddgs import DDGS

            results = []
            with DDGS() as ddgs:
                # Search for text results
                search_results = ddgs.text(query, max_results=max_results)

                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                    })

            return results

        except ImportError:
            return [{
                'error': 'ddgs library not installed',
                'install': 'Run: pip install ddgs (or uv sync)'
            }]
        except Exception as e:
            return [{
                'error': f'Search failed: {str(e)}'
            }]

    def format_results_for_llm(self, query: str, results: List[Dict]) -> str:
        """Format search results into a prompt for the LLM"""

        if not results or 'error' in results[0]:
            error_msg = results[0].get('error', 'Unknown error') if results else 'No results'
            return f"Search for '{query}' failed: {error_msg}"

        # Create structured context for LLM
        formatted = f"# Web Search Results for: {query}\n\n"

        for i, result in enumerate(results, 1):
            formatted += f"## Result {i}: {result['title']}\n"
            formatted += f"URL: {result['url']}\n"
            formatted += f"Summary: {result['snippet']}\n\n"

        return formatted

    def execute(self, query: str, skills: List[Dict], **kwargs) -> str:
        """
        Main execution method called by AgentOrchestrator.

        Flow:
        1. Extract search query
        2. Call DuckDuckGo API
        3. Format results
        4. Pass to LLM for synthesis
        """

        print("\n🔍 DuckDuckGoSearchTool.execute() called!")
        print(f"   Query: {query[:100]}...")

        # Step 1: Perform the search
        print("   Calling DuckDuckGo API...")
        search_results = self.search_duckduckgo(query, max_results=5)
        print(f"   Got {len(search_results)} results")

        # Step 2: Format results for LLM
        search_context = self.format_results_for_llm(query, search_results)

        # Step 3: Ask LLM to synthesize the results
        synthesis_query = f"""Based on the following web search results, provide a comprehensive answer.

{search_context}

Task: Synthesize this information into a clear, organized summary with:
1. Key findings
2. Current state/trends
3. Relevant applications
4. Important sources (with URLs)

Be specific and cite your sources."""

        # Call the research_agent to synthesize
        # Note: This assumes research_agent is available
        try:
            synthesis = self.orchestrator.invoke_agent(
                'research_agent',
                synthesis_query,
                skills=skills
            )
            return synthesis
        except Exception as e:
            # Fallback: just return the formatted results
            return f"{search_context}\n\nNote: Could not synthesize results (Error: {e})"
