"""
Tests for the Agent and Reactor classes.
"""

import pytest
from unittest.mock import Mock, patch
from reactor.agent import Agent, Reactor


class TestAgent:
    """Test cases for the Agent class."""

    def test_agent_initialization(self):
        """Test that Agent initializes correctly."""
        agent = Agent("Test prompt")
        assert agent.prompt == "Test prompt"
        assert agent.tools == []
        assert len(agent.messages) == 1
        assert agent.messages[0]["role"] == "system"
        assert agent.messages[0]["content"] == "Test prompt"

    def test_agent_with_tools(self):
        """Test that Agent initializes correctly with tools."""
        mock_tool = Mock()
        mock_tool.tool_names_and_description.return_value = "test_tool: A test tool"

        agent = Agent("Test prompt", tools=[mock_tool])
        assert len(agent.tools) == 1
        assert "test_tool: A test tool" in agent.prompt

    def test_tools_definition(self):
        """Test that tools_definition returns correct format."""
        mock_tool = Mock()
        mock_tool.definition.return_value = [{"name": "test_tool"}]

        agent = Agent("Test prompt", tools=[mock_tool])
        definitions = agent.tools_definition()
        assert definitions == [{"name": "test_tool"}]

    def test_tools_match(self):
        """Test that tools_match works correctly."""
        mock_tool = Mock()
        mock_tool.names.return_value = ["test_tool"]

        agent = Agent("Test prompt", tools=[mock_tool])

        mock_tool_call = Mock()
        mock_tool_call.function.name = "test_tool"

        assert agent.tools_match(mock_tool_call) is True

        mock_tool_call.function.name = "nonexistent_tool"
        assert agent.tools_match(mock_tool_call) is False


class TestReactor:
    """Test cases for the Reactor class."""

    def test_reactor_initialization(self):
        """Test that Reactor initializes correctly."""
        reactor = Reactor()
        assert "reason+act framework" in reactor.prompt
        assert len(reactor.tools) >= 1  # Should have at least FinalAnswer tool

    def test_reactor_with_tools(self):
        """Test that Reactor initializes correctly with additional tools."""
        mock_tool = Mock()
        mock_tool.tool_names_and_description.return_value = "test_tool: A test tool"

        reactor = Reactor(tools=[mock_tool])
        assert len(reactor.tools) >= 2  # Should have mock_tool + FinalAnswer

    @patch("reactor.agent.OpenAI")
    def test_llm_complete(self, mock_openai):
        """Test that llm_complete works correctly."""
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response

        agent = Agent("Test prompt")
        result = agent.llm_complete([], "Test message")

        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
