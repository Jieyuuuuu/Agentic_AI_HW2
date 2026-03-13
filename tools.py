import os
from tavily import TavilyClient

def search_web(query: str) -> str:
    """
    Search the web using Tavily.
    Returns a concatenated string of search result snippets.
    """
    try:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key or api_key == "your_tavily_api_key_here":
            return "Search API error: TAVILY_API_KEY environment variable not set. Please get a free API key from tavily.com and add it to your .env file."
            
        client = TavilyClient(api_key=api_key)
        
        # Get top 3 search results
        response = client.search(query=query, max_results=3)
        results = response.get("results", [])
        
        if not results:
            return "No results found."
        
        snippets = []
        for r in results:
            snippets.append(f"Source: {r.get('title', '')} - {r.get('content', '')}")
        
        return "\n".join(snippets)
    except Exception as e:
        return f"Search API error: {str(e)}"

# Example usage for testing
if __name__ == "__main__":
    print(search_web("Japan population 2025"))
