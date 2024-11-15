##################################################
# Brian Lesko
# 2023-10-24
# In this Low code UI, we interact with a large language transformer model (LLM) through an Application Programming Interface (API).
# Practice Coding for concise software development for engineering in the fields of robotics, AI, and automation. 

def write_stream(stream):
    text = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None: 
            text += content
            with Stream:
                st.markdown(text)
    return text

import streamlit as st
from aitools import AIClient

if "myclient" not in st.session_state:
    ai_choice = st.selectbox("Select AI Company", ['',"openai", "xai"])
    if ai_choice != "":
        st.session_state.myclient = AIClient(ai_choice)
    else:
        st.stop()

if st.session_state.myclient.api_key is None or st.session_state.myclient.api_key == "":
    Message = st.empty()
    Message.warning("Please add your API key to continue.")
    key = st.text_input("API Key")
    if key:
        st.session_state.myclient.reset_api_key(key)
        Message.info("API Key set successfully, you can now continue.")
    else:
        st.stop()

st.title("Low Code Chat Interface") 
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display all the historical messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"### {msg['content']}")
    else:
        st.markdown(msg["content"])

User = st.empty()
Stream = st.empty()

if prompt := st.chat_input("Write a message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    User.markdown('### ' + prompt)
    stream = st.session_state.myclient.get_stream(st.session_state.messages)
    text = write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": text})