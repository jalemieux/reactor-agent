import json
import logging
from openai import OpenAI

from reactor.tools.tool import Tool, FinalAnswer


class Agent:
    """
    Base Agent class that handles LLM interactions with tools.

    This class provides the foundation for creating AI agents that can
    interact with external tools and maintain conversation context.
    """

    def __init__(self, prompt: str, tools: list[Tool] = None):
        """
        Initialize the Agent with a system prompt and optional tools.

        Args:
            prompt: The system prompt that defines the agent's behavior
            tools: Optional list of tools the agent can use
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.tools = []
        self.client = OpenAI()
        if tools:
            self.tools = tools
            self.prompt = (
                prompt
                + "\n\n"
                + "You have access to the following tools:\n"
                + "\n".join(
                    [f"{tool.tool_names_and_description()}" for tool in self.tools]
                )
            )
        self.messages = [{"role": "system", "content": self.prompt}]

    def tools_definition(self) -> list[dict]:
        """Get the tool definitions for the OpenAI API."""
        tools_definition = []
        for tool in self.tools:
            tools_definition.extend(tool.definition())
        return tools_definition

    def tools_match(self, tool_call: dict) -> bool:
        """Check if a tool call matches any available tools."""
        return tool_call.function.name in [tool.names() for tool in self.tools]

    def llm_chat(self, user_input) -> str:
        """
        Perform a chat interaction with the LLM, handling tool calls automatically.

        Args:
            user_input: The user's input message

        Returns:
            The final response from the LLM
        """
        self.messages.append({"role": "user", "content": user_input})
        while True:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                tool_choice="auto",
                tools=self.tools_definition(),
            )
            if response.choices[0].message.tool_calls:
                self.messages.append(response.choices[0].message)

                for tool_call in response.choices[0].message.tool_calls:
                    action_name = tool_call.function.name
                    action_args = json.loads(tool_call.function.arguments)
                    self.logger.info(
                        "Tool call detected with action name: "
                        + action_name
                        + " and arguments: "
                        + str(action_args)
                    )

                    for tool in self.tools:
                        self.logger.info(
                            f"Checking if action '{action_name}' matches tool '{tool.names()}'"
                        )
                        if action_name in tool.names():
                            self.logger.info(
                                f"Executing action '{action_name}' with arguments: {action_args}"
                            )
                            result = getattr(tool, action_name)(**action_args)
                            self.logger.info(
                                f"Result of action '{action_name}': {result[:100]}"
                            )
                            self.messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": str(result),
                                }
                            )
            else:
                self.logger.info(
                    "No tool call detected, appending response to messages"
                )
                self.messages.append(response.choices[0].message)
                break

        return self.messages[-1]

    def llm_complete(self, messages, iterative_message) -> str:
        """
        Complete a conversation with a simple LLM call (no tools).

        Args:
            messages: The conversation history
            iterative_message: The message to append

        Returns:
            The LLM's response
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages + [{"role": "user", "content": iterative_message}],
        )
        return response.choices[0].message.content

    def llm_complete_tool(self, messages, iterative_message) -> tuple[str, list[dict]]:
        """
        Complete a conversation with tool support.

        Args:
            messages: The conversation history
            iterative_message: The message to append

        Returns:
            Tuple of (response_message, tool_calls)
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages + [{"role": "user", "content": iterative_message}],
            tools=self.tools_definition(),
        )
        tool_calls = response.choices[0].message.tool_calls
        return response.choices[0].message, tool_calls


class Reactor(Agent):
    """
    A ReAct (Reasoning + Acting) agent that implements iterative reasoning cycles.

    This agent follows the ReAct framework:
    - Thought: Analyze the problem
    - Action: Perform an action using available tools
    - Observation: Analyze the results
    - Repeat until final answer is reached
    """

    def __init__(self, tools: list[Tool] = None):
        """
        Initialize the Reactor agent with optional tools.

        Args:
            tools: Optional list of tools the agent can use
        """
        self.prompt = """
You are an AI assistant uses the reason+act framework.
- **thought**: You think carefully about the user's question or task. Do not assume you already know the answer.
- **action**: You perform an action based on your thought. You have access to various tools.
- **observation**: You read the result of that action
- **thought**: You revise your reasoning based on the observation.
"""
        if not tools:
            tools = []
        super().__init__(prompt=self.prompt, tools=tools + [FinalAnswer()])

    def run_loop(self, question):
        """
        Run the ReAct reasoning loop for a given question.

        Args:
            question: The user's question to answer

        Returns:
            Tuple of (final_answer, conversation_history)
        """
        counter = 0
        while counter < 10:  # don't run more than 10 times
            if counter == 0:
                user_message = (
                    f'Given this user question "{question}", what is your thought?'
                )
            else:
                user_message = (
                    f"Given your previous observation, what is your next thought?"
                )

            thought = self.llm_complete(self.messages, user_message)
            self.messages.append({"role": "assistant", "content": thought})
            self.logger.info("--------------------------------")
            self.logger.info("thought: " + thought)

            message, tool_calls = self.llm_complete_tool(
                self.messages,
                f"Given your previous thought, what action would you take?",
            )

            self.messages.append(message)

            for tool_call in tool_calls:
                action_name = tool_call.function.name
                action_args = json.loads(tool_call.function.arguments)

                self.logger.info("--------------------------------")
                self.logger.info("action: " + action_name)

                if action_name == "final_answer":
                    self.messages.append(message)
                    return action_args, self.messages

                else:
                    for tool in self.tools:
                        if action_name in tool.names():
                            self.logger.info(
                                f"Executing action '{action_name}' with arguments: {action_args}"
                            )
                            result = tool.run(action_name, **action_args)
                            self.logger.info(
                                f"Result of action '{action_name}': {result}"
                            )
                            self.messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": str(result),
                                }
                            )

            observation = self.llm_complete(
                self.messages,
                "Given the previous action results, what is your observation?",
            )
            self.messages.append({"role": "assistant", "content": observation})
            self.logger.info("--------------------------------")
            self.logger.info("observation: " + observation)

            counter += 1
