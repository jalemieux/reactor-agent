"""
Tavily search tool for Reactor Agent.
"""

import os
from typing import List, Dict, Any
from tavily import TavilyClient

from reactor.tools.tool import Tool


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
            # Validate inputs
            if not query or not query.strip():
                return "Error: Search query cannot be empty."
            
            # Make the API call
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results
            )
            print("****", response)
            # Handle different response formats
            if isinstance(response, dict):
                results_data = response.get("results")
            elif isinstance(response, list):
                results_data = response
            else:
                raise ValueError(f"Unexpected response format from Tavily API: {str(response)[:200]}")
            
            if not results_data:
                raise "No search results found for the given query."
            
            return results_data
            
        except Exception as e:
            error_msg = f"Error performing search: {str(e)}"
            return error_msg
    
    def get_url_content(self, url: str) -> str:
        """
        Get the content of a specific URL.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            The content of the URL
        """
        try:
            # Use the search method with a specific URL query
            response = self.client.search(
                query=f"site:{url}",
                max_results=1,
                search_depth="basic"
            )
            
            # Check if response is None or empty
            if not response:
                return "No response received from Tavily API. Please check your API key and try again."
            
            # Handle different response formats
            if isinstance(response, dict):
                results_data = response.get("results")
            elif isinstance(response, list):
                results_data = response
                
            if not results_data:
                return "No content available for this URL."
            
            # Get the first result
            result = results_data[0] if results_data else None
            if not result or not isinstance(result, dict):
                return "No content available for this URL."
            
            return result
            
        except Exception as e:
            return f"Error fetching URL content: {str(e)}" 
        

    def run(self, action_name, **action_args):
        if action_name == "search_internet":
            return self.search_internet(**action_args)
        elif action_name == "get_url_content":
            return self.get_url_content(**action_args)
        else:
            raise ValueError(f"Invalid action name: {action_name}")