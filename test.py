# from langgraph.graph import StateGraph, END
# from langchain_ollama import ChatOllama
# from langchain_core.runnables import Runnable
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.tools import tool

# # ✅ Define arithmetic tools
# @tool
# def addition(x: int, y: int) -> int:
#     return x + y

# @tool
# def subtraction(x: int, y: int) -> int:
#     return x - y

# @tool
# def multiplication(x: int, y: int) -> int:
#     return x * y

# @tool
# def division(x: int, y: int) -> float:
#     return x / y if y != 0 else float('inf')

# # ✅ Init Ollama
# llm = ChatOllama(model="llama3", temperature=0)

# # ✅ Define the prompt
# system_message = SystemMessage(content="""
# You are a math agent. Use one of the following tools to answer the question:
# - addition(x, y)
# - subtraction(x, y)
# - multiplication(x, y)
# - division(x, y)
# Reply with ONLY the tool call needed to solve the problem.
# """)

# # ✅ Make an LLM Runnable Node
# def llm_node(state):
#     question = state["query"]
#     messages = [system_message, HumanMessage(content=question)]
#     response = llm.invoke(messages).content.lower()

#     # Very basic parser
#     if "add" in response or "+" in response:
#         state["tool"] = "addition"
#     elif "subtract" in response or "-" in response:
#         state["tool"] = "subtraction"
#     elif "multiply" in response or "*" in response:
#         state["tool"] = "multiplication"
#     elif "divide" in response or "/" in response:
#         state["tool"] = "division"
#     else:
#         state["tool"] = None

#     return state

# # ✅ Tool Executor Node
# def tool_executor(state):
#     x, y = state["x"], state["y"]
#     tool_name = state["tool"]

#     tool_map = {
#         "addition": addition,
#         "subtraction": subtraction,
#         "multiplication": multiplication,
#         "division": division
#     }

#     if tool_name and tool_name in tool_map:
#         result = tool_map[tool_name].invoke({"x": x, "y": y})
#         state["result"] = result
#     else:
#         state["result"] = "Unknown operation"

#     return state

# # ✅ Build the graph
# builder = StateGraph(dict)
# builder.add_node("router_llm", llm_node)
# builder.add_node("exec_tool", tool_executor)
# builder.set_entry_point("router_llm")
# builder.add_edge("router_llm", "exec_tool")
# builder.add_edge("exec_tool", END)

# graph = builder.compile()

# # ✅ Run it
# if __name__ == "__main__":
#     tests = [
#         {"query": "What is 3 + 5?", "x": 3, "y": 5},
#         {"query": "Multiply 7 by 6", "x": 7, "y": 6},
#         {"query": "Divide 10 by 2", "x": 10, "y": 2},
#         {"query": "Subtract 9 from 12", "x": 12, "y": 9},
#     ]

#     for i, test in enumerate(tests, 1):
#         print(f"\n🔢 Test {i}: {test['query']}")
#         result = graph.invoke(test)
#         print("✅ Result:", result["result"])
