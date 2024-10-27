from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import ToolNode


class Agent:
    """
    Agent is a class that represents a single AI agent.
    """

    def __init__(
        self,
        name: str,
        instructions: str,
        functions: dict = None,
    ):
        self.name = name
        self.instructions = instructions
        self.tool_mapping = functions
        self.functions = list((functions or {}).values())

    def __str__(self):
        return f"Agent: {self.name}\n\nInstructions:\n{self.instructions}"

    def invoke(
        self,
        llm: ChatAnthropic,
        query: str,
    ):
        tools = self.functions
        tool_node = ToolNode(tools)
        model_with_tools = llm.bind_tools(tools)
        response = tool_node.invoke({"messages": [model_with_tools.invoke(query)]})
        print(response["messages"][0].content)
