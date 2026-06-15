#1. importing all stuff
from langgraph.graph import StateGraph
from langgraph.graph import END
from graphs.state import RiskState
from graphs.nodes import validate_risk
from graphs.nodes import generate_response


#2.  conditional routing function
def route_after_validation(state:RiskState):
    if not state.get("is_valid_risk"):
        return END
    elif state.get("strategy"):
        return "generate_response"
    elif not state.get( "is_detailed"):
        return END

    else:
        return END

#3. building the graph
#a. initialise the graph with state dictionary to get the starting point
workFlow = StateGraph(RiskState)

#b. adding the two check points
workFlow.add_node("validate_risk", validate_risk)
workFlow.add_node("generate_response", generate_response)

workFlow.set_entry_point("validate_risk")

workFlow.add_conditional_edges("validate_risk", route_after_validation)

workFlow.add_edge("generate_response", END)

graph_app = workFlow.compile()


#4. testing the connection
if __name__ == "__main__":
    print("Test 1 - Invalid Risk")
    #should stop after validation and out is false
    state_1 = {"user_input": "what's the weather like?"}
    print(graph_app.invoke(state_1))


    print("Test 2 - Valid but not detailed")
    #should stop after validation and output will be followup questions
    state_2 = {"user_input": "server might crash"}
    print(graph_app.invoke(state_2))

    print("Test 3 - Valid and has Strategy")
    #should run validation and generate response after it
    state_3 = {"user_input": "server might crash", "strategy": "mitigate"}
    print(graph_app.invoke(state_3))