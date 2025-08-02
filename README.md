# Reactor Agent

A ReAct (Reasoning + Acting) agent framework for AI-powered reasoning and tool execution.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Start

Get up and running in minutes with Reactor Agent:

### 1. Install

```bash
pip install reactor-agent
```

### 2. Set up API Keys

```bash
# Required: OpenAI API key
export OPENAI_API_KEY="your-openai-api-key"

# Optional: Tavily API key for internet search
export TAVILY_API_KEY="your-tavily-api-key"
```

### 3. Basic Usage

```python
from reactor import Reactor
from reactor.tools.internet_tool import TavilyTool

# Create agent with internet search capability
reactor = Reactor(tools=[TavilyTool()])

# Ask a complex question
response, messages = reactor.run_loop(
    "What's the best time to visit Japan for cherry blossoms?"
)

print(response['answer'])
```

### 4. With Tracing (Recommended)

```python
from reactor import Reactor, SimpleTrace
from reactor.tools.internet_tool import TavilyTool

# Enable tracing for debugging and analysis
trace_service = SimpleTrace(session_id="my_session")
reactor = Reactor(tools=[TavilyTool()], trace_service=trace_service)

# Run the agent
response, messages = reactor.run_loop(
    "Find budget hotels in Paris near the Eiffel Tower"
)

# Get session summary
summary = trace_service.get_session_summary()
print(f"Generated {summary['total_traces']} traces")

# Export for analysis
trace_service.export_traces("session_traces.json")
```

### 5. Custom Configuration

```python
from reactor import Reactor, SimpleTrace
from reactor.tools.internet_tool import TavilyTool

# Configure agent with custom settings
reactor = Reactor(
    tools=[TavilyTool()],
    model_name="gpt-4o",           # Use different model
    log_level="DEBUG",              # Enable debug logging
    max_iterations=15               # Allow more reasoning steps
)

response, messages = reactor.run_loop(
    "What are the latest developments in quantum computing?"
)
```

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
- **Structured Tracing**: Comprehensive tracing system for debugging and analysis

## Installation

### From PyPI (Recommended)

```bash
pip install reactor-agent
```

### From Source (Development)

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
```


## Examples

Check out the example files to see Reactor Agent in action:

- **`examples/basic_usage.py`** - Simple usage without tools
- **`examples/tracing_examples.py`** - Comprehensive tracing demonstrations
- **`examples/logging_demo.py`** - Logging configuration examples

Run an example:

```bash
python examples/basic_usage.py
```

## Configuration

### API Keys

Set your API keys as environment variables:

```bash
# Required: OpenAI API key
export OPENAI_API_KEY="your-openai-api-key"

# Optional: Tavily API key for internet search
export TAVILY_API_KEY="your-tavily-api-key"
```

Or create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-openai-api-key" > .env
echo "TAVILY_API_KEY=your-tavily-api-key" >> .env
```



### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py -v

# Run trace service tests
pytest tests/test_trace.py -v

# Run integration tests
pytest tests/test_agent_trace_integration.py -v
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


**Reactor Agent** - Empowering AI agents with reasoning and action capabilities.
