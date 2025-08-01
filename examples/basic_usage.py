#!/usr/bin/env python3
"""
Basic usage example for the Reactor agent.

This example demonstrates how to create and use a Reactor agent
with internet search capabilities.
"""

from reactor import Reactor
from reactor.tools.internet_tool import TavilyTool


def main():
    """Run a basic example with the Reactor agent."""
    
    # Initialize the Reactor with internet search tool
    reactor = Reactor(tools=[TavilyTool()])
    
    # Ask a question that requires research
    question = "Where in France can I find a cheap Airbnb for 1 month with a pool?"
    
    print(f"Question: {question}")
    print("=" * 50)
    
    # Run the reasoning loop
    response, messages = reactor.run_loop(question)
    
    print("\n" + "=" * 50)
    print("Final Answer:")
    print(response['answer'])
    
    

if __name__ == "__main__":
    main() 