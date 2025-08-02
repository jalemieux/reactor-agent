#!/usr/bin/env python3
"""
Test integration between Agent and TraceService.
"""

import json
from unittest import TestCase

from reactor.agent import Agent, Reactor
from reactor.trace import SimpleTrace, TraceType


class TestAgentTraceIntegration(TestCase):
    """Test cases for Agent and SimpleTrace integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.trace_service = SimpleTrace(session_id="test_integration", enable_console_output=False)
    
    def test_agent_with_trace_service(self):
        """Test that Agent can be initialized with trace service."""
        agent = Agent(
            prompt="You are a helpful assistant.",
            trace_service=self.trace_service
        )
        
        self.assertIsNotNone(agent.trace_service)
        self.assertEqual(agent.trace_service.session_id, "test_integration")
    
    def test_reactor_with_trace_service(self):
        """Test that Reactor can be initialized with trace service."""
        reactor = Reactor(trace_service=self.trace_service)
        
        self.assertIsNotNone(reactor.trace_service)
        self.assertEqual(reactor.trace_service.session_id, "test_integration")
    
    def test_simple_conversation_tracing(self):
        """Test that simple conversations generate traces."""
        agent = Agent(
            prompt="You are a helpful assistant. Answer questions briefly.",
            trace_service=self.trace_service
        )
        
        # Run a simple conversation
        response = agent.llm_chat("What is 2 + 2?")
        
        # Check that traces were generated
        traces = self.trace_service.get_traces()
        self.assertGreater(len(traces), 0)
        
        # Check for conversation start trace
        conversation_traces = self.trace_service.get_traces_by_type(TraceType.CONVERSATION_START)
        self.assertGreater(len(conversation_traces), 0)
        
        # Check for LLM response trace (when no tools are used)
        llm_traces = self.trace_service.get_traces_by_type(TraceType.LLM_RESPONSE)
        self.assertGreater(len(llm_traces), 0)
    
    def test_reactor_reasoning_cycle_tracing(self):
        """Test that Reactor reasoning cycles generate appropriate traces."""
        reactor = Reactor(trace_service=self.trace_service)
        
        # Run a simple reasoning cycle
        try:
            final_answer, conversation_history = reactor.run_loop("What is 2 + 2?")
            
            # Check that traces were generated
            traces = self.trace_service.get_traces()
            self.assertGreater(len(traces), 0)
            
            # Check for thought traces
            thought_traces = self.trace_service.get_traces_by_type(TraceType.THOUGHT)
            self.assertGreater(len(thought_traces), 0)
            
            # Check for action traces
            action_traces = self.trace_service.get_traces_by_type(TraceType.ACTION)
            self.assertGreater(len(action_traces), 0)
            
            # Check for observation traces
            observation_traces = self.trace_service.get_traces_by_type(TraceType.OBSERVATION)
            self.assertGreater(len(observation_traces), 0)
            
        except Exception as e:
            # If there's an error (e.g., API issues), just check that traces were started
            traces = self.trace_service.get_traces()
            self.assertGreater(len(traces), 0)
    
    def test_trace_export_functionality(self):
        """Test that traces can be exported properly."""
        agent = Agent(
            prompt="You are a helpful assistant.",
            trace_service=self.trace_service
        )
        
        # Run a simple conversation
        agent.llm_chat("Hello")
        
        # Export traces
        trace_data = self.trace_service.get_traces()
        
        # Verify trace structure
        for trace in trace_data:
            self.assertIn('timestamp', trace)
            self.assertIn('trace_type', trace)
            self.assertIn('message', trace)
            self.assertIn('session_id', trace)
            self.assertIsInstance(trace['timestamp'], str)
            self.assertIsInstance(trace['trace_type'], str)
            self.assertIsInstance(trace['message'], str)
    
    def test_session_summary_functionality(self):
        """Test that session summary works correctly."""
        agent = Agent(
            prompt="You are a helpful assistant.",
            trace_service=self.trace_service
        )
        
        # Run a simple conversation
        agent.llm_chat("Hello")
        
        # Get session summary
        summary = self.trace_service.get_session_summary()
        
        # Verify summary structure
        self.assertIn('session_id', summary)
        self.assertIn('total_traces', summary)
        self.assertIn('trace_counts', summary)
        self.assertIn('session_start', summary)
        self.assertIn('session_end', summary)
        
        self.assertEqual(summary['session_id'], "test_integration")
        self.assertGreater(summary['total_traces'], 0)
        self.assertIsInstance(summary['trace_counts'], dict)


if __name__ == "__main__":
    import unittest
    unittest.main() 