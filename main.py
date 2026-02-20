# main.py

import streamlit as st
import asyncio
from dotenv import load_dotenv
from graph.graph import build_graph

load_dotenv()

st.title("Super/PF Call Intelligence - Demo Backend")

graph = build_graph()

transcript = st.text_input("Enter Transcript:")

if st.button("Process"):

    state = {
        "transcript": transcript,
        "intent": None,
        "entities": None,
        "member_data": None,
        "knowledge_docs": None,
        "suggestion": None
    }

    result = asyncio.run(graph.ainvoke(state))

    st.subheader("Intent")
    st.write(result["intent"])

    st.subheader("Entities")
    st.write(result["entities"])

    st.subheader("Member Data")
    st.write(result["member_data"])

    st.subheader("Knowledge Retrieved")
    st.write(result["knowledge_docs"])

    st.subheader("Suggested Response")
    st.success(result["suggestion"])
