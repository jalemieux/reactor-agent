#!/usr/bin/env python3
"""
Basic usage example for the Reactor Agent framework.

This example demonstrates:
1. Basic Reactor initialization and usage
2. Trace service integration
3. Tool execution and reasoning cycles
4. CodeInterpreter tool usage
"""

import os
import sys
from pathlib import Path

# Add the examples directory to the Python path so we can import from tools
sys.path.append(str(Path(__file__).parent))

from reactor import Reactor, SimpleTrace
from tools.tavily_tool import TavilyTool

# Set your OpenAI API key
#os.environ["OPENAI_API_KEY"] = "your-api-key-here"

"""Demonstrate basic Reactor usage with tracing and CodeInterpreter tool."""
print("=== Basic Usage Example with CodeInterpreter ===")

# Initialize trace service for monitoring
trace_service = SimpleTrace(session_id="code_interpreter_demo", enable_console_output=True)

# Create CodeInterpreter tool

# Create a Reactor instance with tracing and CodeInterpreter tool
reactor = Reactor(tools=[ TavilyTool(api_key=os.getenv("TAVILY_API_KEY"))], trace_service=trace_service)

# Ask a question that requires code execution
question = "Search the internet for the latest news on the stock market."

print(f"Question: {question}")
print("Running Reactor with CodeInterpreter...")

# Run the reasoning loop
final_answer, conversation_history = reactor.run_loop(question)

print(f"\nFinal Answer: {final_answer}")
print(f"Conversation length: {len(conversation_history)} messages")

# Export traces for analysis
trace_service.export_traces("code_interpreter_traces.json")
print("Traces exported to 'code_interpreter_traces.json'")
