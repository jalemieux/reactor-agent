from reactor.tools.tool import Tool
from tavily import TavilyClient


class TavilyTool(Tool):
    def __init__(self):
        super().__init__(
            names=["search_internet", "get_url_content"],
            description="tavily internet search tools",
        )
        self.tavily_client = TavilyClient()

    def search_internet(self, query):
        return self.tavily_client.search(query)

    def get_url_content(self, url):
        return self.tavily_client.extract(url)

    def run(self, action_name, **action_args):
        if action_name == "search_internet":
            return self.search_internet(**action_args)
        elif action_name == "get_url_content":
            return self.get_url_content(**action_args)
        else:
            raise ValueError(f"Invalid action name: {action_name}")

    def definition(self) -> list[dict]:
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
                                "description": "The query to search the internet for",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_url_content",
                    "description": "Get the content of a URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to get the content of",
                            },
                        },
                        "required": ["url"],
                    },
                },
            },
        ]
