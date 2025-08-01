"""
Tavily search tool for Reactor Agent.
"""

import os
from typing import List, Dict, Any
from tavily import TavilyClient

from .tool import Tool


class TavilyTool(Tool):
    """
    Tool for performing internet searches using Tavily API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Tavily tool.
        
        Args:
            api_key: Tavily API key. If not provided, will try to get from TAVILY_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("Tavily API key is required. Set TAVILY_API_KEY environment variable or pass api_key parameter.")
        
        self.client = TavilyClient(api_key=self.api_key)
    
    def names(self) -> List[str]:
        return ["search_internet", "get_url_content"]
    
    def definition(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_internet",
                    "description": "Search the internet for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            },
                            "search_depth": {
                                "type": "string",
                                "enum": ["basic", "advanced"],
                                "description": "Search depth - basic for quick results, advanced for comprehensive search",
                                "default": "basic"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_url_content",
                    "description": "Get the content of a specific URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to fetch content from"
                            }
                        },
                        "required": ["url"]
                    }
                }
            }
        ]
    
    def tool_names_and_description(self) -> str:
        return "search_internet: Search the internet for information\nget_url_content: Get the content of a specific URL"
    
    def search_internet(self, query: str, search_depth: str = "basic", max_results: int = 5) -> str:
        """
        Search the internet for information.
        
        Args:
            query: The search query
            search_depth: Search depth ("basic" or "advanced")
            max_results: Maximum number of results
            
        Returns:
            Search results as a formatted string
        """
        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results
            )
            
            results = []
            for result in response.get("results", []):
                title = result.get("title", "No title")
                url = result.get("url", "No URL")
                content = result.get("content", "No content")
                results.append(f"Title: {title}\nURL: {url}\nContent: {content}\n")
            
            return "\n".join(results) if results else "No results found."
            
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    def get_url_content(self, url: str) -> str:
        """
        Get the content of a specific URL.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            The content of the URL
        """
        try:
            response = self.client.get_content(url)
            return response.get("content", "No content available")
        except Exception as e:
            return f"Error fetching URL content: {str(e)}" 