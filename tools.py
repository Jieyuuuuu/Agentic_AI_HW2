import os
from duckduckgo_search import DDGS

def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Returns a concatenated string of search result snippets.
    """
    try:
        with DDGS() as ddgs:
            # Get top 3 search results
            results = list(ddgs.text(query, max_results=3))
            
            if not results:
                return "No results found."
            
            snippets = []
            for r in results:
                snippets.append(f"Source: {r.get('title', '')} - {r.get('body', '')}")
            
            return "\n".join(snippets)
    except Exception as e:
        return f"Search API error: {str(e)}"

# Example usage for testing
if __name__ == "__main__":
    print(search_web("Japan population 2025"))
