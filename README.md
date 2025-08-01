# Reactor Agent

A ReAct (Reasoning + Acting) agent framework for AI-powered reasoning and tool execution.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Does

Reactor Agent implements the ReAct framework (Reasoning + Acting) that lets AI agents perform iterative reasoning cycles with tool integration. The agent can:

- Think through problems step by step
- Use tools to gather information or perform actions
- Analyze results and refine its reasoning
- Continue until it reaches a final answer

## Key Features

- **Iterative Reasoning**: Multi-step reasoning with tool integration
- **Tool Support**: Easy integration with external tools (web search, APIs, etc.)
- **Conversation Memory**: Maintains context across reasoning cycles

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/jalemieux/reactor-agent.git
cd reactor-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
# venv\Scripts\activate  # On Windows

# Install in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt
```

### From PyPI (when published)

```bash
pip install reactor-agent
```

## Quick Start

### Basic Usage

```python
from reactor import Reactor
from reactor.tools.tavily_tool import TavilyTool

# Initialize the Reactor with internet search capability
reactor = Reactor(tools=[TavilyTool()])

# Ask a complex question that requires research
response, messages = reactor.run_loop(
    "Where in France can I find a cheap Airbnb for 1 month with a pool?"
)

# Get the final answer
print(response['answer'])
```

### Advanced Usage

```python
from reactor import Agent, Reactor
from reactor.tools.tavily_tool import TavilyTool

# Create a custom agent with specific behavior
custom_prompt = """
You are a travel planning expert. Always provide detailed, 
practical advice with specific recommendations.
"""

agent = Agent(prompt=custom_prompt, tools=[TavilyTool()])

# Use for direct chat
response = agent.llm_chat("Help me plan a 3-day trip to Tokyo")

# Use Reactor for complex reasoning tasks
reactor = Reactor(tools=[TavilyTool()])
final_answer, conversation = reactor.run_loop(
    "Find the best budget hotels in Tokyo for a 5-day trip, "
    "considering proximity to public transport and tourist attractions"
)
```

## How It Works

### The ReAct Framework

The Reactor implements the ReAct (Reasoning + Acting) framework:

1. **Thought**: "Given this user question, what is your thought?"
2. **Action**: "Given your previous thought, what action would you take?"
3. **Observation**: "Given the previous action results, what is your observation?"
4. **Revised Thought**: "Given your previous observation, what is your next thought?"

This cycle continues until the agent reaches a final answer or hits the maximum iterations (10).

### Example Reasoning Process

```
User: "Where in France can I find a cheap Airbnb for 1 month with a pool?"

Thought: "I need to search for information about Airbnb rentals in France with pools"
Action: search_internet(query="Airbnb France pool long term rental")
Observation: "Found several regions in France with pool rentals..."
Thought: "I should look for specific regions and check prices"
Action: get_url_content(url="specific_airbnb_listing")
Observation: "This listing shows €2000/month for a villa with pool in Provence"
Thought: "I have enough information to provide a comprehensive answer"
Action: final_answer(answer="Based on my research, you can find...")
```

## API Reference

### Agent Class

Base class for creating AI agents with tool integration.

```python
class Agent:
    def __init__(self, prompt: str, tools: list[Tool] = None)
    
    def llm_chat(self, user_input: str) -> str
    def llm_complete(self, messages, iterative_message: str) -> str
    def llm_complete_tool(self, messages, iterative_message: str) -> tuple[str, list[dict]]
```

### Reactor Class

Specialized agent that implements the ReAct framework.

```python
class Reactor(Agent):
    def __init__(self, tools: list[Tool] = None)
    
    def run_loop(self, question: str) -> tuple[dict, list]
```

## Configuration

### Environment Variables

Set your API keys:

```bash
# OpenAI API key (required)
export OPENAI_API_KEY="your-openai-api-key-here"

# Tavily API key (required for internet search)
export TAVILY_API_KEY="your-tavily-api-key-here"
```

Or create a .env file:

```bash
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
echo "TAVILY_API_KEY=your-tavily-api-key-here" >> .env
```

### Available Tools

The framework includes several built-in tools:

- **TavilyTool**: Internet search capabilities using Tavily API
- **FinalAnswer**: Built-in tool for ending reasoning cycles
- **Custom Tools**: Create your own tools by extending the Tool class

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py -v
```

### Code Quality

```bash
# Format code
black reactor/ tests/ examples/

# Lint code
flake8 reactor/ tests/ examples/
```

### Building the Package

```bash
# Install build tools
pip install build

# Build distribution
python -m build

# This creates:
# - dist/reactor_agent-0.1.0.tar.gz
# - dist/reactor_agent-0.1.0-py3-none-any.whl
```

## Project Structure

```
reactor/
├── setup.py              # Package configuration
├── pyproject.toml        # Modern Python packaging
├── requirements.txt      # Dependencies
├── README.md            # This file
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
├── MANIFEST.in          # Package manifest
├── reactor/             # Main package
│   ├── __init__.py      # Package initialization
│   └── agent.py         # Core Agent and Reactor classes
├── examples/            # Usage examples
│   └── basic_usage.py   # Basic usage example
└── tests/              # Test suite
    ├── __init__.py
    └── test_agent.py    # Unit tests
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on the ReAct framework from "ReAct: Synergizing Reasoning and Acting in Language Models" by Yao et al.
- Built with OpenAI's GPT models
- Internet search powered by Tavily API

## Support

If you run into issues or have questions:

1. Check the [examples](examples/) directory for usage patterns
2. Review the [tests](tests/) for implementation details
3. Open an issue on GitHub

---

**Reactor Agent** - Empowering AI agents with reasoning and action capabilities.
