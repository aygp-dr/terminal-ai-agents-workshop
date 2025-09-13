"""Web search tool for agents"""
import os
import requests
from typing import List, Dict

class WebSearchTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SEARCH_API_KEY")
        self.base_url = "https://api.search.engine/v1"
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web and return results"""
        response = requests.get(
            f"{self.base_url}/search",
            params={"q": query, "limit": max_results},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Search failed: {response.status_code}")
        
        results = response.json()["results"]
        return [{
            "title": r["title"],
            "url": r["url"],
            "snippet": r["snippet"]
        } for r in results]
    
    def fetch_content(self, url: str) -> str:
        """Fetch and extract content from URL"""
        response = requests.get(url)
        # Simple extraction - in practice use BeautifulSoup
        return response.text[:1000] + "..."
