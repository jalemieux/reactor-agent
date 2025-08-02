import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum


class TraceType(Enum):
    """Types of traces that can be recorded."""
    TOOL_CALL = "tool_call"
    TOOL_EXECUTION = "tool_execution"
    TOOL_RESULT = "tool_result"
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    SEPARATOR = "separator"
    LLM_RESPONSE = "llm_response"
    CONVERSATION_START = "conversation_start"


@dataclass
class TraceEntry:
    """A single trace entry with metadata."""
    timestamp: str
    trace_type: TraceType
    message: str
    metadata: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace entry to dictionary."""
        data = asdict(self)
        data['trace_type'] = self.trace_type.value
        return data


class TraceService(ABC):
    """
    Abstract base class for tracing LLM operations and reasoning cycles.
    
    This service provides structured tracing capabilities for:
    - Tool calls and executions
    - Reasoning cycles (thought, action, observation)
    - LLM responses
    - Conversation flow
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize the trace service.
        
        Args:
            session_id: Optional session identifier for grouping traces
        """
        self.session_id = session_id or f"session_{int(time.time())}"
    
    @abstractmethod
    def _add_trace(self, trace_type: TraceType, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a trace entry. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_traces(self) -> List[Dict[str, Any]]:
        """Get all traces as dictionaries. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_traces_by_type(self, trace_type: TraceType) -> List[Dict[str, Any]]:
        """Get traces filtered by type. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def clear_traces(self):
        """Clear all traces. Must be implemented by subclasses."""
        pass
    
    def trace_tool_call(self, action_name: str, action_args: Dict[str, Any]):
        """Trace a tool call."""
        self._add_trace(
            TraceType.TOOL_CALL,
            f"Tool call detected with action name: {action_name} and arguments: {action_args}",
            {"action_name": action_name, "action_args": action_args}
        )
    
    def trace_tool_check(self, action_name: str, tool_names: List[str]):
        """Trace tool matching check."""
        self._add_trace(
            TraceType.TOOL_EXECUTION,
            f"Checking if action '{action_name}' matches tools: {tool_names}",
            {"action_name": action_name, "available_tools": tool_names}
        )
    
    def trace_tool_execution(self, action_name: str, action_args: Dict[str, Any]):
        """Trace tool execution start."""
        self._add_trace(
            TraceType.TOOL_EXECUTION,
            f"Executing action '{action_name}' with arguments: {action_args}",
            {"action_name": action_name, "action_args": action_args}
        )
    
    def trace_tool_result(self, action_name: str, result: str):
        """Trace tool execution result."""
        # Truncate result for display if too long
        display_result = result[:100] + "..." if len(result) > 100 else result
        self._add_trace(
            TraceType.TOOL_RESULT,
            f"Result of action '{action_name}': {display_result}",
            {"action_name": action_name, "result": result, "result_length": len(result)}
        )
    
    def trace_no_tool_call(self):
        """Trace when no tool call is detected."""
        self._add_trace(
            TraceType.LLM_RESPONSE,
            "No tool call detected, appending response to messages"
        )
    
    def trace_thought(self, thought: str):
        """Trace a reasoning thought."""
        self._add_trace(
            TraceType.THOUGHT,
            f"thought: {thought}",
            {"thought": thought}
        )
    
    def trace_action(self, action_name: str):
        """Trace an action."""
        self._add_trace(
            TraceType.ACTION,
            f"action: {action_name}",
            {"action_name": action_name}
        )
    
    def trace_observation(self, observation: str):
        """Trace an observation."""
        self._add_trace(
            TraceType.OBSERVATION,
            f"observation: {observation}",
            {"observation": observation}
        )
    
    def trace_separator(self):
        """Trace a separator line."""
        self._add_trace(TraceType.SEPARATOR, "--------------------------------")
    
    def trace_conversation_start(self, user_input: str):
        """Trace the start of a conversation."""
        self._add_trace(
            TraceType.CONVERSATION_START,
            f"Starting conversation with user input: {user_input}",
            {"user_input": user_input}
        )
    
    def export_traces(self, filepath: str):
        """Export traces to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.get_traces(), f, indent=2)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the tracing session."""
        traces = self.get_traces()
        trace_counts = {}
        for trace_type in TraceType:
            trace_counts[trace_type.value] = len(self.get_traces_by_type(trace_type))
        
        return {
            "session_id": self.session_id,
            "total_traces": len(traces),
            "trace_counts": trace_counts,
            "session_start": traces[0]["timestamp"] if traces else None,
            "session_end": traces[-1]["timestamp"] if traces else None
        }


class SimpleTrace(TraceService):
    """
    Simple implementation of TraceService that stores traces in memory and optionally prints to console.
    
    This is the original implementation moved to a concrete class.
    """
    
    def __init__(self, session_id: Optional[str] = None, enable_console_output: bool = True):
        """
        Initialize the simple trace service.
        
        Args:
            session_id: Optional session identifier for grouping traces
            enable_console_output: Whether to also print traces to console
        """
        super().__init__(session_id)
        self.traces: List[TraceEntry] = []
        self.enable_console_output = enable_console_output
        
    def _add_trace(self, trace_type: TraceType, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a trace entry."""
        trace = TraceEntry(
            timestamp=datetime.now().isoformat(),
            trace_type=trace_type,
            message=message,
            metadata=metadata,
            session_id=self.session_id
        )
        self.traces.append(trace)
        
        if self.enable_console_output:
            self._print_trace(trace)
    
    def _print_trace(self, trace: TraceEntry):
        """Print trace to console with formatting."""
        if trace.trace_type == TraceType.SEPARATOR:
            print("--------------------------------")
        else:
            prefix = f"[{trace.trace_type.value.upper()}]"
            print(f"{prefix}: {trace.message}")
    
    def get_traces(self) -> List[Dict[str, Any]]:
        """Get all traces as dictionaries."""
        return [trace.to_dict() for trace in self.traces]
    
    def get_traces_by_type(self, trace_type: TraceType) -> List[Dict[str, Any]]:
        """Get traces filtered by type."""
        return [trace.to_dict() for trace in self.traces if trace.trace_type == trace_type]
    
    def clear_traces(self):
        """Clear all traces."""
        self.traces.clear() 