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

def basic_usage_example():
    """Demonstrate basic Reactor usage with tracing."""
    print("=== Basic Usage Example ===")
    
    # Initialize trace service for monitoring
    trace_service = SimpleTrace(session_id="basic_usage_demo", enable_console_output=True)
    
    # Create a Reactor instance with tracing
    reactor = Reactor(trace_service=trace_service)
    
    # Ask a question that requires reasoning
    question = "What is the current weather in New York City?"
    
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

def advanced_usage_example():
    """Demonstrate advanced usage with custom tools and detailed tracing."""
    print("\n=== Advanced Usage Example ===")
    
    # Initialize trace service with console output disabled for cleaner output
    trace_service = SimpleTrace(session_id="advanced_demo")
    
    # Create a Reactor instance
    reactor = Reactor(trace_service=trace_service)
    
    # Ask a complex question
    question = "What are the latest developments in quantum computing?"
    
    print(f"Question: {question}")
    print("Running Reactor with detailed tracing...")
    
    try:
        # Run the reasoning loop
        final_answer, conversation_history = reactor.run_loop(question)
        
        print(f"\nFinal Answer: {final_answer}")
        
        # Get session summary
        summary = trace_service.get_session_summary()
        print(f"\nSession Summary:")
        print(f"  Total traces: {summary['total_traces']}")
        print(f"  Trace types: {summary['trace_counts']}")
        
        # Export traces
        trace_service.export_traces("advanced_usage_traces.json")
        print("Traces exported to 'advanced_usage_traces.json'")
        
    except Exception as e:
        print(f"Error: {e}")
        print("This is expected if no API key is set or if there are API issues.")

if __name__ == "__main__":
    basic_usage_example()
    advanced_usage_example() 