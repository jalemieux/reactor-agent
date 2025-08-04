#!/usr/bin/env python3
"""
Basic usage example for the Reactor Agent framework.

This example demonstrates:
1. Basic Reactor initialization and usage
2. Trace service integration
3. Tool execution and reasoning cycles
"""

import os
from reactor import Reactor, SimpleTrace

# Set your OpenAI API key
#os.environ["OPENAI_API_KEY"] = "your-api-key-here"

"""Demonstrate basic Reactor usage with tracing."""
print("=== Basic Usage Example ===")

# Initialize trace service for monitoring
trace_service = SimpleTrace(session_id="basic_usage_demo", enable_console_output=True)

# Create a Reactor instance with tracing
reactor = Reactor(trace_service=trace_service)

# Ask a question that requires reasoning
question = "What’s the current time, and how many seconds are left until midnight in my time zone?"

print(f"Question: {question}")
print("Running Reactor...")

try:
    # Run the reasoning loop
    final_answer, conversation_history = reactor.run_loop(question)
    
    print(f"\nFinal Answer: {final_answer}")
    print(f"Conversation length: {len(conversation_history)} messages")
    
    # Export traces for analysis
    trace_service.export_traces("basic_usage_traces.json")
    print("Traces exported to 'basic_usage_traces.json'")
    
except Exception as e:
    print(f"Error: {e}")
    print("This is expected if no API key is set or if there are API issues.")
