#!/usr/bin/env python3
"""Test script to verify DuckDuckGo search is working"""

import sys
from pathlib import Path

# Add tool paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / '.claude' / 'skills' / 'web-search' / 'scripts'))

from DuckDuckGoSearchTool import DuckDuckGoSearchTool

def test_duckduckgo_directly():
    """Test DuckDuckGo search directly"""
    print("=" * 60)
    print("Testing DuckDuckGo Search API Directly")
    print("=" * 60)

    # Create tool
    tool = DuckDuckGoSearchTool(orchestrator=None)

    # Test search
    query = "stock market technical analysis indicators"
    print(f"\n🔍 Searching for: {query}\n")

    results = tool.search_duckduckgo(query, max_results=3)

    if not results:
        print("❌ No results returned")
        return False

    if 'error' in results[0]:
        print(f"❌ Error: {results[0]['error']}")
        if 'install' in results[0]:
            print(f"   {results[0]['install']}")
        return False

    print(f"✅ Got {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet'][:100]}...")
        print()

    return True

def test_formatting():
    """Test result formatting"""
    print("\n" + "=" * 60)
    print("Testing Result Formatting")
    print("=" * 60)

    tool = DuckDuckGoSearchTool(orchestrator=None)
    query = "quantum computing"

    results = tool.search_duckduckgo(query, max_results=2)

    if results and 'error' not in results[0]:
        formatted = tool.format_results_for_llm(query, results)
        print("\nFormatted output (first 500 chars):")
        print("-" * 60)
        print(formatted[:500])
        print("...")
        print("-" * 60)
        return True

    return False

if __name__ == "__main__":
    print("\n🧪 DuckDuckGo Search Test Suite\n")

    success = True

    # Test 1: Direct search
    if not test_duckduckgo_directly():
        success = False
        print("\n⚠️  Direct search failed. Make sure you've installed:")
        print("   pip install duckduckgo-search")

    # Test 2: Formatting
    if not test_formatting():
        success = False

    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed! DuckDuckGo search is working.")
        print("\nYou can now run: python3 main.py")
    else:
        print("❌ Some tests failed. See errors above.")
    print("=" * 60)
