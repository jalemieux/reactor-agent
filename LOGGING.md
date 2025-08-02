# Logging Configuration

This document describes the terminal-friendly logging configuration and best practices for the Reactor framework.

## Overview

The logging system has been redesigned to provide:
- **Colored output** for better visual scanning
- **Structured formatting** with timestamps and line numbers
- **Clear visual indicators** for different operation types
- **Configurable log levels** per agent instance
- **Truncated long messages** for readability
- **Error handling** with proper logging

## Quick Start

### Basic Usage

```python
from reactor.agent import Agent
import logging

# Create agent with default INFO level
agent = Agent(prompt="You are a helpful assistant.")

# Create agent with custom log level
agent = Agent(
    prompt="You are a helpful assistant.",
    log_level=logging.DEBUG  # More verbose
)
```

### Reactor Usage

```python
from reactor.agent import Reactor
import logging

# Create Reactor with custom logging
reactor = Reactor(
    tools=[your_tools],
    log_level=logging.INFO
)

# Run with detailed logging
result, history = reactor.run_loop("Your question here?")
```

## Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about program execution
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems

## Visual Indicators

The logging system uses colors and clear text indicators to make output more scannable:

- **Generating thought** - Agent is thinking
- **Thought** - Agent's reasoning
- **Generating action** - Agent is deciding what to do
- **Action** - Tool being called
- **Executing tool** - Tool is running
- **Tool result** - Successful tool execution
- **Tool execution failed** - Error in tool execution
- **Generating observation** - Agent is analyzing results
- **Observation** - Agent's analysis
- **Final answer reached** - Successfully completed
- **Warning** - Potential issues

## Configuration Options

### Custom Format

```python
from reactor.logging_config import setup_logging

# Custom format string
logger = setup_logging(
    level=logging.INFO,
    format_string='%(asctime)s | %(levelname)s | %(message)s'
)
```

### File Logging

```python
from reactor.logging_config import setup_logging

# Log to both console and file
logger = setup_logging(
    level=logging.INFO,
    log_file="reactor.log",
    use_colors=True  # Colors only in console, not file
)
```

### Disable Colors

```python
from reactor.logging_config import setup_logging

# Disable colored output
logger = setup_logging(
    level=logging.INFO,
    use_colors=False
)
```

## Best Practices

### 1. Choose Appropriate Log Levels

- Use **DEBUG** for development and troubleshooting
- Use **INFO** for normal operation
- Use **WARNING** for recoverable issues
- Use **ERROR** for serious problems

### 2. Structured Logging

```python
# Good - structured information
self.logger.info(f"Executing tool: {tool_name} with args: {args}")

# Avoid - unstructured
self.logger.info("Executing tool")
```

### 3. Error Handling

```python
try:
    result = tool.run(action_name, **action_args)
    self.logger.info(f"Tool result: {result_preview}")
except Exception as e:
    self.logger.error(f"Tool execution failed: {action_name} - {str(e)}")
    raise  # Re-raise to maintain error flow
```

### 4. Message Truncation

Long messages are automatically truncated for readability:

```python
# Long results are truncated
result_preview = str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
self.logger.info(f"Tool result: {result_preview}")
```

### 5. Contextual Information

Include relevant context in log messages:

```python
self.logger.info(f"Starting ReAct loop for question: {question[:100]}...")
self.logger.info(f"=== Iteration {iteration}/{max_iterations} ===")
```

## Demo

Run the logging demo to see the improvements in action:

```bash
python examples/logging_demo.py
```

## Dependencies

The logging system requires:
- `colorama==0.4.6` - For cross-platform colored output

This is automatically included in `requirements.txt`.

## Migration from Old Logging

The old logging setup:
```python
logging.basicConfig(level=logging.INFO)
self.logger = logging.getLogger(__name__)
```

Is replaced with:
```python
from reactor.logging_config import setup_logging, get_logger

setup_logging(level=log_level, use_colors=True)
self.logger = get_logger(__name__)
```

The new system provides better visual feedback and more structured output while maintaining the same API. 