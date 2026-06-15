#1. importing all the required stuff
import streamlit as st
from graphs.graph import graph_app

#2. configuring the page layout
st.set_page_config(page_title="Risk Agent", page_icon="🛡️")
st.title("Project Risk Response Agent")

#3. initialising session state
if "current_state" not in st.session_state:
    st.session_state.current_state = None




#4. building screen 1
if st.session_state.current_state is None:
    user_input = st.text_area("Describe the Project Risk")
     

    if st.button("Analyze Risk"):
        if user_input:
            with st.spinner("Analysing the Risk"):
                result = graph_app.invoke({"user_input": user_input})
                st.session_state.current_state = result
                st.rerun()


#5. building screen 2a 
#invalid risk
if st.session_state.current_state is not None and st.session_state.current_state.get("is_valid_risk") == False:
    st.error("This is not a Valid Project Risk. Please Try Again")

    #button to restart
    if st.button("Start Over"):
        st.session_state.current_state = None
        st.rerun()


#6. building screen 2b
#more details screen
if st.session_state.current_state is not None and st.session_state.current_state.get("is_valid_risk") == True and st.session_state.current_state.get("is_detailed") == False:
    st.warning("This is a Valid Risk. Provide more details to generate a strategy.")

    #looping through the qs
    st.write("Please Answer this Questions:")
    for questions in st.session_state.current_state.get("followup_questions", []):
        st.write(f"- {questions}")
    
    additional_details = st.text_area("Add More Details Here")

    if st.button("Submit Details"):
        if additional_details:
            with st.spinner("Re-Analyzing your Risk"):
                combined_input = f"{st.session_state.current_state['user_input']}. Additional Details: {additional_details}"

                result = graph_app.invoke({"user_input": combined_input})
                st.session_state.current_state = result
                st.rerun()


#7. bulding screen 3
#strategy selection for the user
if st.session_state.current_state is not None and st.session_state.current_state.get("is_valid_risk") == True and st.session_state.current_state.get("is_detailed") == True and not st.session_state.current_state.get("strategy"):
    st.success("That is a Valid Detailed Risk")
    st.write("Choose a Response Strategy")

    #two columns for 2x2 grid
    col1, col2  = st.columns(2)
    with col1:
        if st.button("Mitigate (Reduce Impact)", use_container_width = True):
            with st.spinner("Generating Action Plan"):
                st.session_state.current_state["strategy"] = "Mitigate"
                result = graph_app.invoke(st.session_state.current_state)
                st.session_state.current_state = result
                st.rerun()
        
        if st.button("Accept (Monitor)", use_container_width = True):
            with st.spinner("Generating Action Plan"):
                st.session_state.current_state["strategy"] = "Accept"
                result = graph_app.invoke(st.session_state.current_state)
                st.session_state.current_state = result
                st.rerun()

    with col2:
        if st.button("Transfer (Shift to Third Party)", use_container_width = True):
            with st.spinner("Generating Action Plan"):
                st.session_state.current_state["strategy"] = "Transfer"
                result = graph_app.invoke(st.session_state.current_state)
                st.session_state.current_state = result
                st.rerun()
        
        if st.button("Avoid (Change Plan)", use_container_width = True):
            with st.spinner("Generating Action Plan"):
                st.session_state.current_state["strategy"] = "Avoid"
                result = graph_app.invoke(st.session_state.current_state)
                st.session_state.current_state = result
                st.rerun()


#8. building screen 4
#final ai response
if st.session_state.current_state is not None and st.session_state.current_state.get("ai_response"):
    st.success(f"Strategy Selected: {st.session_state.current_state.get('strategy')}")
    st.write("AI Recommended Action Plan")

    #display 5 step action that ai generated
    st.write(st.session_state.current_state.get("ai_response"))
    st.divider()

    #option to start again
    if st.button("Evaluate Another Risk", type="primary"):
        st.session_state.current_state = None
        st.rerun()