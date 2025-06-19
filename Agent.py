from typing import Annotated
from typing_extensions import TypedDict

# Langchain/graph modules
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages

# Import Model
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model

# Import environment variables
from dotenv import load_dotenv
load_dotenv()

# Import visualization library
from IPython.display import Image,display
 

# Define Class state for messages
class State(TypedDict):
    messages:Annotated[list,add_messages]

# testing node functionality
def chatbot(state:State):
    return {"messages":[llm.invoke(state["messages"])]}

llm = ChatGroq(model="llama3-8b-8192")
print(llm)


if __name__ == '__main__':
    graph_builder = StateGraph(State)

    # Adding node
    graph_builder.add_node("llmchat", chatbot) 

    # Adding Edges
    graph_builder.add_edge(START,"llmchat")
    graph_builder.add_edge("llmchat", END)

    # Compile The graph
    graph = graph_builder.compile(name="Agent_test", debug=True)

    try:
        img = display(Image(graph.get_graph().draw_mermaid_png()))
        with open("graph.png", "wb") as f:
            f.write(img.data)
    except Exception:
        print("Visualization not supported in this environment.")




