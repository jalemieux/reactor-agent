#!/usr/bin/env python3
"""
Trace service demonstration and examples.

This example shows how to use the trace service for monitoring
LLM operations and reasoning cycles.
"""

from reactor.trace import SimpleTrace, TraceType

def basic_trace_demo():
    """Demonstrate basic trace service functionality."""
    print("=== Basic Trace Service Demo ===")
    
    # Create a trace service with console output
    trace_service = SimpleTrace(session_id="demo_session_001")
    
    # Simulate some tracing operations
    trace_service.trace_conversation_start("What is the weather today?")
    trace_service.trace_thought("I need to check the weather information")
    trace_service.trace_action("search_weather")
    trace_service.trace_observation("Weather data retrieved: Sunny, 75°F")
    trace_service.trace_thought("The weather is sunny and warm")
    trace_service.trace_separator()
    
    # Get trace summary
    summary = trace_service.get_session_summary()
    print(f"Session ID: {summary['session_id']}")
    print(f"Total traces: {summary['total_traces']}")
    print(f"Trace counts: {summary['trace_counts']}")
    
    # Export traces
    trace_service.export_traces("basic_trace_demo.json")
    print("Traces exported to 'basic_trace_demo.json'")

def tool_trace_demo():
    """Demonstrate tool-specific tracing."""
    print("\n=== Tool Trace Demo ===")
    
    # Create trace service without console output for cleaner demo
    trace_service = SimpleTrace(session_id="tool_demo_001", enable_console_output=False)
    
    # Simulate tool calls and executions
    trace_service.trace_tool_call("search_web", {"query": "python programming"})
    trace_service.trace_tool_check("search_web", ["search_web", "get_weather"])
    trace_service.trace_tool_execution("search_web", {"query": "python programming"})
    trace_service.trace_tool_result("search_web", "Found 1,234,567 results for python programming...")
    
    # Get traces by type
    tool_calls = trace_service.get_traces_by_type(TraceType.TOOL_CALL)
    tool_executions = trace_service.get_traces_by_type(TraceType.TOOL_EXECUTION)
    tool_results = trace_service.get_traces_by_type(TraceType.TOOL_RESULT)
    
    print(f"Tool calls: {len(tool_calls)}")
    print(f"Tool executions: {len(tool_executions)}")
    print(f"Tool results: {len(tool_results)}")
    
    # Export traces
    trace_service.export_traces("tool_trace_demo.json")
    print("Tool traces exported to 'tool_trace_demo.json'")

def trace_analysis_demo():
    """Demonstrate trace analysis capabilities."""
    print("\n=== Trace Analysis Demo ===")
    
    # Create trace service
    trace_service = SimpleTrace(session_id="analysis_demo_001")
    
    # Simulate a complex reasoning session
    trace_service.trace_conversation_start("How do I learn machine learning?")
    
    # Multiple reasoning cycles
    for i in range(3):
        trace_service.trace_thought(f"Reasoning step {i+1}: Need to research learning resources")
        trace_service.trace_action(f"search_step_{i+1}")
        trace_service.trace_observation(f"Found {10-i} relevant resources for step {i+1}")
        trace_service.trace_separator()
    
    # Analyze traces
    all_traces = trace_service.get_traces()
    thought_traces = trace_service.get_traces_by_type(TraceType.THOUGHT)
    action_traces = trace_service.get_traces_by_type(TraceType.ACTION)
    observation_traces = trace_service.get_traces_by_type(TraceType.OBSERVATION)
    
    print(f"Total traces: {len(all_traces)}")
    print(f"Thought traces: {len(thought_traces)}")
    print(f"Action traces: {len(action_traces)}")
    print(f"Observation traces: {len(observation_traces)}")
    
    # Show session summary
    summary = trace_service.get_session_summary()
    print(f"\nSession Summary:")
    for trace_type, count in summary['trace_counts'].items():
        if count > 0:
            print(f"  {trace_type}: {count}")
    
    # Export for further analysis
    trace_service.export_traces("trace_analysis_demo.json")
    print("Analysis traces exported to 'trace_analysis_demo.json'")

if __name__ == "__main__":
    basic_trace_demo()
    tool_trace_demo()
    trace_analysis_demo() 