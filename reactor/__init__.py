"""
Reactor Agent - A ReAct (Reasoning + Acting) agent framework for AI-powered reasoning and tool execution.

This package implements a ReAct agent that can perform iterative reasoning cycles
with tool integration for dynamic information gathering and action execution.
"""

from .agent import Agent, Reactor
from .trace import SimpleTrace, TraceType, TraceEntry

__version__ = "0.1.0"
__author__ = "Jac Lemieux"
__email__ = "jalemieux@gmail.com"

__all__ = ["Agent", "Reactor", "SimpleTrace", "TraceType", "TraceEntry"]
