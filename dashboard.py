import streamlit as st
import pandas as pd
from database.db import get_all_risks


def show_dashboard():
    st.header("Risk Response Dashboard")
    risks = get_all_risks()

    if not risks:
        st.info("No Risks have been recorded yet")
        return

    
    #make data into table format
    data = []
    for r in risks:
        data.append({"Risk Input": r.risk_input, 
        "Strategy": r.strategy, 
        "AI Response": r.ai_response[:100] + "..." if r.ai_response else "",
        "Rating": r.rating, 
        "Date": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""
        })

    
    df = pd.DataFrame(data)

    #display the tbale
    st.dataframe(df, use_container_width = True, hide_index = True)

   