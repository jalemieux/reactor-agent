I'll analyze the `reactor.py` codebase to understand what it does, how to use it, and what approach it implements.

Read file: machina/reactor.py
Now let me examine the tools to better understand the architecture:

Read file: machina/tools/tool.py
Let me also check the internet tool to see what other tools are available:

Read file: machina/tools/internet_tool.py
Now let me search for any documentation or examples to better understand the usage:

Search files...
Let me also check the usage examples to see how it's used in practice:

Read file: usage.py
Now let me search for information about the "reason+act" framework to understand the theoretical background:

Ran tool
Based on my analysis of the `reactor.py` codebase and the search results, I can now provide a comprehensive explanation of what this system does, how to use it, and the theoretical framework it implements.

## What the Reactor System Does

The `reactor.py` codebase implements a **ReAct (Reasoning + Acting) agent framework** that creates AI agents capable of iterative reasoning and tool-based actions. Here's what it does:

### Core Components:

1. **Agent Class**: A base class that handles LLM interactions with tools
2. **Reactor Class**: A specialized agent that implements the ReAct framework
3. **Tool System**: Modular tools that the agent can use to perform actions

### Key Features:

- **Iterative Reasoning Loop**: The agent goes through cycles of thought → action → observation → revised thought
- **Tool Integration**: Can use various tools (internet search, web scraping, etc.)
- **Conversation Memory**: Maintains context across reasoning cycles
- **Automatic Tool Execution**: Dynamically calls tools based on reasoning

## How to Use It

### Basic Usage:

```python
from machina.reactor import Reactor
from machina.tools.internet_tool import TavilyTool

# Initialize with tools
reactor = Reactor(tools=[TavilyTool()])

# Ask a question
response, messages = reactor.run_loop("Where in France can I find a cheap Airbnb for 1 month with a pool?")

# Get the final answer
print(response['answer'])
```

### The Reasoning Loop:

The `run_loop` method implements this cycle:

1. **Thought**: "Given this user question, what is your thought?"
2. **Action**: "Given your previous thought, what action would you take?"
3. **Observation**: "Given the previous action results, what is your observation?"
4. **Revised Thought**: "Given your previous observation, what is your next thought?"

This continues until the agent calls the `final_answer` tool or reaches the maximum iterations (10).

## Theoretical Framework: ReAct (Reasoning + Acting)

This implementation is based on the **ReAct framework** from the 2022 paper:

**"ReAct: Synergizing Reasoning and Acting in Language Models"** by Yao et al.

### Key Principles:

1. **Synergistic Reasoning and Acting**: Unlike traditional approaches that separate reasoning from action, ReAct integrates them into a unified framework.

2. **Iterative Refinement**: The agent can revise its reasoning based on observations from actions.

3. **Tool-Augmented Reasoning**: Uses external tools to gather information and perform actions.

4. **Transparent Reasoning**: The agent's thought process is explicit and traceable.

### Why This Approach Matters:

- **Reduces Hallucination**: By grounding reasoning in actual tool results
- **Improves Complex Problem Solving**: Can tackle multi-step problems requiring research
- **Enables Dynamic Information Retrieval**: Can search for information as needed
- **Provides Explainable AI**: The reasoning process is transparent

### Example Flow:
```
User: "Where in France can I find a cheap Airbnb for 1 month with a pool?"

Thought: "I need to search for information about Airbnb rentals in France with pools"
Action: search_internet(query="Airbnb France pool long term rental")
Observation: "Found several regions in France with pool rentals..."
Thought: "I should look for specific regions and check prices"
Action: get_url_content(url="specific_airbnb_listing")
Observation: "This listing shows €2000/month for a villa with pool in Provence"
Thought: "I have enough information to provide a comprehensive answer"
Action: final_answer(answer="Based on my research, you can find...")
```

This framework represents a significant advancement in AI agent capabilities, moving beyond simple question-answering to dynamic, tool-augmented reasoning systems.


I'll analyze how the ReAct framework implemented in this codebase compares to other reasoning engines, examining both the advantages and limitations.

Ran tool
Ran tool
Based on my analysis of the ReAct implementation in the codebase and research on reasoning engines, here's a comprehensive comparison:

## ReAct vs. Other Reasoning Engines

### **ReAct (Reasoning + Acting) - This Implementation**

**Pros:**
- **Tool-Augmented Reasoning**: Can use external tools (internet search, APIs, databases) to gather real-time information
- **Grounding in Reality**: Actions produce observable results that inform subsequent reasoning
- **Iterative Refinement**: Can revise reasoning based on action outcomes
- **Transparent Process**: Each step (thought → action → observation) is explicit and traceable
- **Dynamic Information Retrieval**: Can search for information as needed rather than relying on pre-trained knowledge
- **Reduces Hallucination**: Actions provide factual grounding

**Cons:**
- **Single Reasoning Path**: Follows one linear chain of reasoning (unlike Tree of Thoughts)
- **Tool Dependency**: Requires well-designed tools and reliable external services
- **Latency**: Each action takes time, making it slower than pure reasoning
- **Error Propagation**: Tool failures can break the entire reasoning chain
- **Limited Exploration**: Doesn't explore multiple reasoning paths simultaneously

### **Chain of Thought (CoT)**

**Pros:**
- **Simple and Effective**: Easy to implement and understand
- **Step-by-Step Reasoning**: Breaks complex problems into manageable steps
- **No External Dependencies**: Works with just the LLM
- **Fast Execution**: No external API calls or tool execution delays
- **Widely Supported**: Most LLMs handle CoT prompting well

**Cons:**
- **No External Verification**: Reasoning isn't grounded in real-world data
- **Hallucination Risk**: Can make up facts or reasoning steps
- **Static Knowledge**: Limited to pre-trained information
- **No Action Capability**: Can't perform real-world actions
- **Linear Reasoning**: Can't backtrack or explore alternatives

### **Tree of Thoughts (ToT)**

**Pros:**
- **Multiple Reasoning Paths**: Explores different approaches simultaneously
- **Backtracking Capability**: Can abandon failed paths and try alternatives
- **Systematic Search**: Uses search algorithms to find optimal solutions
- **Better for Complex Problems**: Excels at problems requiring exploration
- **Self-Evaluation**: Can assess the quality of different reasoning paths

**Cons:**
- **Computational Overhead**: Requires multiple LLM calls for path exploration
- **Complex Implementation**: More difficult to implement and debug
- **No External Actions**: Like CoT, lacks tool integration
- **Resource Intensive**: Can be expensive with many parallel reasoning paths
- **Still Prone to Hallucination**: No grounding in external data

## **Comparison Matrix**

| Aspect | ReAct | Chain of Thought | Tree of Thoughts |
|--------|-------|------------------|------------------|
| **External Tools** | ✅ Full support | ❌ None | ❌ None |
| **Reasoning Paths** | Single linear | Single linear | Multiple parallel |
| **Grounding** | ✅ Action-based | ❌ Internal only | ❌ Internal only |
| **Speed** | ⚠️ Tool-dependent | ✅ Fast | ⚠️ Multiple calls |
| **Complexity** | ⚠️ Medium | ✅ Simple | ❌ High |
| **Hallucination** | ✅ Reduced | ❌ High risk | ❌ High risk |
| **Exploration** | ❌ Limited | ❌ None | ✅ Extensive |

## **When to Use Each Approach**

### **Use ReAct when:**
- You need real-world information (web search, API calls)
- Tasks require multiple steps with external verification
- You want to reduce hallucination risk
- Problems need dynamic information gathering

### **Use Chain of Thought when:**
- Problems are well-defined and self-contained
- Speed is critical
- You have limited computational resources
- Tasks don't require external information

### **Use Tree of Thoughts when:**
- Problems have multiple valid solution paths
- You need to explore different strategies
- Tasks require systematic search through possibilities
- You have sufficient computational resources

## **This Implementation's Specific Advantages**

Looking at the `reactor.py` code:

```python
# The iterative loop structure
thought = self.llm_complete(self.messages, user_message)
message, tool_calls = self.llm_complete_tool(self.messages, f"Given your previous thought, what action would you take?")
observation = self.llm_complete(self.messages, "Given the previous action results, what is your observation?")
```

This implementation provides:
- **Clear separation** of reasoning phases
- **Tool integration** through the `TavilyTool` and other tools
- **Conversation memory** that persists across reasoning cycles
- **Automatic tool execution** based on reasoning
- **Graceful termination** via the `final_answer` tool

The main limitation is that it's still a single-path reasoning approach, but it compensates with real-world grounding through tools, making it particularly effective for information-seeking tasks and complex problem-solving that requires external data.
