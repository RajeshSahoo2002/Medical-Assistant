import streamlit as st
from utils.api import ask_question

def render_chat():
    st.subheader("💬 Chat with HealthSage")
    
    # Below function is to show the previous messages to the user. Adding the session state to store the messages in the chat history and if there are no messages then it will initialize an empty list to store the messages in the chat history. This is important to maintain the context of the conversation and to show the previous messages to the user.
    if "messages" not in st.session_state:
        st.session_state.messages=[]

    # render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # input and response
    user_input=st.chat_input("Enter you query....")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})

        response=ask_question(user_input)
        if response.status_code==200:
            data=response.json()
            answer=data["response"]
            sources=data.get("sources",[])
            st.chat_message("assistant").markdown(answer)
            # if sources:
            #     st.markdown("📄 **Sources: **")
            #     for src in sources:
            #         st.markdown(f"- `{src}`")
            st.session_state.messages.append({"role":"assistant","content":answer})
        else:
            st.error(f"Error: {response.text}")