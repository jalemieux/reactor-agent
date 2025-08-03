# Reactor Agent

**EXPERIMENTAL CODE - NOT PRODUCTION READY**

A ReAct (Reasoning + Acting) agent framework for AI-powered reasoning and tool execution. This is experimental research code implementing the ReAct framework described in "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022).

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](https://github.com/jalemieux/reactor-agent)

## Important Notice

This is **experimental research code** and is **NOT intended for production use**. The framework is provided as-is for research and educational purposes. Use at your own risk.

## Research Background

Reactor Agent implements the ReAct framework introduced in the paper:

**"ReAct: Synergizing Reasoning and Acting in Language Models"** (Yao et al., 2022)
- **Paper**: [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- **Authors**: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao

The ReAct framework synergizes reasoning and acting capabilities in language models, building upon earlier work on Chain-of-Thought prompting (Wei et al., 2022) and extending it to include tool use and interactive decision-making.

### Related Research

This implementation draws from several key papers in interactive language model research:

1. **Chain-of-Thought Prompting** (Wei et al., 2022)
   - [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
   - Establishes the foundation for step-by-step reasoning in LLMs

2. **ReAct Framework** (Yao et al., 2022)
   - [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
   - Combines reasoning with tool use and action planning

3. **Interactive Language Models**
   - Recent work on tool-using LLMs and interactive reasoning
   - Survey: [Prompt4ReasoningPapers](https://github.com/zjunlp/Prompt4ReasoningPapers)

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

### 3. Examples

See the `examples/` directory for complete usage examples:

- **`examples/basic_example.py`** - Basic usage without tools
- **`examples/tool_example.py`** - Usage with tools
- **`examples/tools/tavily_tool.py`** - Custom tool implementation

Run an example:

```bash
python examples/basic_example.py
```

## What This Does

Reactor Agent implements the ReAct framework (Reasoning + Acting) that lets AI agents perform iterative reasoning cycles with tool integration. The agent can:

- **Think through problems step by step** using Chain-of-Thought reasoning
- **Use tools to gather information** or perform actions
- **Analyze results and refine its reasoning** based on new information
- **Continue iteratively** until it reaches a final answer

This follows the ReAct paradigm where the agent alternates between:
1. **Reasoning**: Generating thoughts and plans
2. **Acting**: Using tools to gather information or perform actions
3. **Observing**: Analyzing results and updating its understanding

## Key Features

- **Iterative Reasoning**: Multi-step reasoning with tool integration following ReAct principles
- **Tool Support**: Easy integration with external tools (web search, APIs, etc.)
- **Conversation Memory**: Maintains context across reasoning cycles
- **Structured Tracing**: Comprehensive tracing system for debugging and analysis
- **Research-Ready**: Designed for experimentation and analysis of reasoning patterns

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


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **ReAct Framework**: Based on "ReAct: Synergizing Reasoning and Acting in Language Models" by Yao et al. (2022)
- **Chain-of-Thought**: Building on "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" by Wei et al. (2022)
- **OpenAI GPT Models**: Powered by OpenAI's language models
- **Tavily API**: Internet search capabilities provided by Tavily

## References

1. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. *arXiv preprint arXiv:2210.03629*.

2. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., ... & Le, Q. V. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems*, 35, 24824-24837.

3. For a comprehensive survey of reasoning in language models, see: [Prompt4ReasoningPapers](https://github.com/zjunlp/Prompt4ReasoningPapers)

---

**Reactor Agent** - Experimental implementation of the ReAct framework for AI reasoning and action research.
