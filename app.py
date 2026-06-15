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