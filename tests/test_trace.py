#!/usr/bin/env python3
"""
Tests for the trace service functionality.
"""

import json
import tempfile
import os
from unittest import TestCase

from reactor.trace import SimpleTrace, TraceType, TraceEntry


class TestTraceService(TestCase):
    """Test cases for the SimpleTrace class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.trace_service = SimpleTrace(session_id="test_session")
    
    def test_trace_service_initialization(self):
        """Test trace service initialization."""
        self.assertIsNotNone(self.trace_service.session_id)
        self.assertEqual(len(self.trace_service.traces), 0)
        self.assertTrue(self.trace_service.enable_console_output)
    
    def test_trace_tool_call(self):
        """Test tracing tool calls."""
        action_name = "test_action"
        action_args = {"param1": "value1", "param2": 42}
        
        self.trace_service.trace_tool_call(action_name, action_args)
        
        self.assertEqual(len(self.trace_service.traces), 1)
        trace = self.trace_service.traces[0]
        self.assertEqual(trace.trace_type, TraceType.TOOL_CALL)
        self.assertIn(action_name, trace.message)
        self.assertEqual(trace.metadata["action_name"], action_name)
        self.assertEqual(trace.metadata["action_args"], action_args)
    
    def test_trace_thought(self):
        """Test tracing thoughts."""
        thought = "This is a test thought"
        
        self.trace_service.trace_thought(thought)
        
        self.assertEqual(len(self.trace_service.traces), 1)
        trace = self.trace_service.traces[0]
        self.assertEqual(trace.trace_type, TraceType.THOUGHT)
        self.assertIn(thought, trace.message)
        self.assertEqual(trace.metadata["thought"], thought)
    
    def test_trace_action(self):
        """Test tracing actions."""
        action_name = "test_action"
        
        self.trace_service.trace_action(action_name)
        
        self.assertEqual(len(self.trace_service.traces), 1)
        trace = self.trace_service.traces[0]
        self.assertEqual(trace.trace_type, TraceType.ACTION)
        self.assertIn(action_name, trace.message)
        self.assertEqual(trace.metadata["action_name"], action_name)
    
    def test_trace_observation(self):
        """Test tracing observations."""
        observation = "This is a test observation"
        
        self.trace_service.trace_observation(observation)
        
        self.assertEqual(len(self.trace_service.traces), 1)
        trace = self.trace_service.traces[0]
        self.assertEqual(trace.trace_type, TraceType.OBSERVATION)
        self.assertIn(observation, trace.message)
        self.assertEqual(trace.metadata["observation"], observation)
    
    def test_get_traces_by_type(self):
        """Test getting traces filtered by type."""
        # Add different types of traces
        self.trace_service.trace_thought("thought1")
        self.trace_service.trace_action("action1")
        self.trace_service.trace_thought("thought2")
        self.trace_service.trace_observation("observation1")
        
        # Get traces by type
        thought_traces = self.trace_service.get_traces_by_type(TraceType.THOUGHT)
        action_traces = self.trace_service.get_traces_by_type(TraceType.ACTION)
        observation_traces = self.trace_service.get_traces_by_type(TraceType.OBSERVATION)
        
        self.assertEqual(len(thought_traces), 2)
        self.assertEqual(len(action_traces), 1)
        self.assertEqual(len(observation_traces), 1)
        
        # Check trace content
        self.assertIn("thought1", thought_traces[0]["message"])
        self.assertIn("thought2", thought_traces[1]["message"])
        self.assertIn("action1", action_traces[0]["message"])
        self.assertIn("observation1", observation_traces[0]["message"])
    
    def test_export_traces(self):
        """Test exporting traces to JSON file."""
        # Add some traces
        self.trace_service.trace_thought("test thought")
        self.trace_service.trace_action("test action")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Export traces
            self.trace_service.export_traces(temp_file)
            
            # Read and verify the exported file
            with open(temp_file, 'r') as f:
                exported_data = json.load(f)
            
            self.assertEqual(len(exported_data), 2)
            self.assertEqual(exported_data[0]["trace_type"], "thought")
            self.assertEqual(exported_data[1]["trace_type"], "action")
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_get_session_summary(self):
        """Test getting session summary."""
        # Add traces
        self.trace_service.trace_thought("thought1")
        self.trace_service.trace_action("action1")
        self.trace_service.trace_thought("thought2")
        
        summary = self.trace_service.get_session_summary()
        
        self.assertEqual(summary["session_id"], "test_session")
        self.assertEqual(summary["total_traces"], 3)
        self.assertEqual(summary["trace_counts"]["thought"], 2)
        self.assertEqual(summary["trace_counts"]["action"], 1)
        self.assertIsNotNone(summary["session_start"])
        self.assertIsNotNone(summary["session_end"])
    
    def test_clear_traces(self):
        """Test clearing traces."""
        # Add some traces
        self.trace_service.trace_thought("test thought")
        self.trace_service.trace_action("test action")
        
        self.assertEqual(len(self.trace_service.traces), 2)
        
        # Clear traces
        self.trace_service.clear_traces()
        
        self.assertEqual(len(self.trace_service.traces), 0)
    
    def test_trace_entry_to_dict(self):
        """Test TraceEntry to_dict method."""
        trace = TraceEntry(
            timestamp="2023-01-01T00:00:00",
            trace_type=TraceType.THOUGHT,
            message="test message",
            metadata={"key": "value"},
            session_id="test_session"
        )
        
        trace_dict = trace.to_dict()
        
        self.assertEqual(trace_dict["timestamp"], "2023-01-01T00:00:00")
        self.assertEqual(trace_dict["trace_type"], "thought")
        self.assertEqual(trace_dict["message"], "test message")
        self.assertEqual(trace_dict["metadata"]["key"], "value")
        self.assertEqual(trace_dict["session_id"], "test_session")


if __name__ == "__main__":
    import unittest
    unittest.main() 