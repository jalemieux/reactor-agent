from machina.tools.tool import Tool
from bs4 import BeautifulSoup
import requests
import os


class WebDocTool(Tool):
    def __init__(self, name, description, url):
        super().__init__(names=[name], description=description)
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def get_text_segments_for_keyword(self, keyword: str) -> str:
        content = self.get_fmp_api_doc()

        # Find all occurrences of the keyword and extract surrounding text
        keyword_positions = [
            i for i in range(len(content)) if content.startswith(keyword, i)
        ]
        surrounding_texts = []
        for pos in keyword_positions:
            start = max(0, pos - 1000)  # Get 1000 characters before the keyword
            end = min(len(content), pos + 1000)  # Get 1000 characters after the keyword
            surrounding_texts.append(content[start:end])

        return "\n\n".join(surrounding_texts)

    def get_web_doc(self) -> str:
        file_path = self.name + ".txt"
        if not os.path.exists(file_path):
            content = self._fetch_and_clean_url_content(self.url)
            with open(file_path, "w") as file:
                file.write(content)
        else:
            with open(file_path, "r") as file:
                content = file.read()
        return content

    def _fetch_and_clean_url_content(self) -> str:
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the URL: {self.url}")

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove all script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get text
        text = soup.get_text()

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)

        return text

    def fmp_api_doc(self, keyword: str):
        # return self.get_text_segments_for_keyword(keyword)
        return self.get_fmp_api_doc()

    def definition(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "keyword to search for in the documentation",
                            }
                        },
                        "required": ["keyword"],
                    },
                },
            }
        ]
