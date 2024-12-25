##################################################
# Brian Lesko
# 2024-12-24
# In this Low code UI, we interact with a large language transformer model (LLM) through an Application Programming Interface (API).

import streamlit as st
from aitools import AIClient
import base64

def write_stream(stream):
    text = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None: 
            text += content
            with Stream:
                if do_html is True:
                    st.html(f'''<p style="padding: 0; margin: 0;"> {text} </p>''')
                else: 
                    st.markdown(f"<div>{text}</div>", unsafe_allow_html=True)
    return text

st.set_page_config(page_title='LLM0',page_icon='')
hide_streamlit_style = "<style>#MainMenu, footer, header {visibility: hidden;}</style>"
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
ai_choice = st.sidebar.selectbox("Choose an API", ["xai", "openai"])
if "myai" not in st.session_state or st.session_state.myai.company_name  != ai_choice:
    st.session_state.myai = AIClient(ai_choice)

if st.session_state.myai.api_key is None:
    Message = st.empty()
    import base64
    msg="CjxkaXYgc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7IGZvbnQtZmFtaWx5OiBBcmlhbCwgc2Fucy1zZXJpZjsgbWFyZ2luOiAyMHB4OyI+CiAgICA8aDMgc3R5bGU9ImNvbG9yOiAjMzMzOyI+UGxlYXNlIGFkZCB5b3VyIEFQSSBrZXkgdG8gY29udGludWUuPC9oMz4KICAgIDxwPgogICAgICAgIEFkZCB5b3VyIGtleSBpbiA8Y29kZSBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogI2Y0ZjRmNDsgcGFkZGluZzogMnB4IDRweDsgYm9yZGVyLXJhZGl1czogNHB4OyBmb250LWZhbWlseTogJ0NvdXJpZXIgTmV3JywgQ291cmllciwgbW9ub3NwYWNlOyI+CiAgICAgICAga2V5cy5qc29uCiAgICAgICAgPC9jb2RlPiBhcyAKICAgICAgICA8Y29kZSBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogI2Y0ZjRmNDsgcGFkZGluZzogMnB4IDRweDsgYm9yZGVyLXJhZGl1czogNHB4OyBmb250LWZhbWlseTogJ0NvdXJpZXIgTmV3JywgQ291cmllciwgbW9ub3NwYWNlOyI+CiAgICAgICAgeGFpX2FwaV9rZXkKICAgICAgICA8L2NvZGU+IG9yIAogICAgICAgIDxjb2RlIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiAjZjRmNGY0OyBwYWRkaW5nOiAycHggNHB4OyBib3JkZXItcmFkaXVzOiA0cHg7IGZvbnQtZmFtaWx5OiAnQ291cmllciBOZXcnLCBDb3VyaWVyLCBtb25vc3BhY2U7Ij4KICAgICAgICBvcGVuYWlfYXBpX2tleQogICAgICAgIDwvY29kZT4uCiAgICA8L3A+CjwvZGl2Pgo="
    Message.html(base64.b64decode(msg).decode("utf-8"))
    st.stop()

st.session_state.myai._set_environment_variables()
st.session_state.myai._get_client()

st.markdown('<h1 style="text-align: center; padding-top: 60px;">My llm</h1>', unsafe_allow_html=True)
Upload = st.empty()
Chat = st.empty()
file = Upload.file_uploader("", accept_multiple_files=False)
if file: st.session_state.file = st.session_state.myai._reduce_image_size(file)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "file" in st.session_state:
    b64 = st.session_state.file
    st.html(f"""
        <div style="text-align: center; padding-top: 40px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{b64}" alt="Base64 Image" style="max-width: 100%; height: auto; border-radius: 10px;">
        </div>
    """)

do_html = st.sidebar.checkbox("Use HTML", value=False)

# Display all the historical messages
for msg in st.session_state.messages:
    if isinstance(msg["content"], str): # This is a text message
        if msg["role"] == "user":
            st.markdown(f"<h2 style='padding-top: 40px;'>{msg['content']}</h2>", unsafe_allow_html=True)
        else:
            st.html(f'''<p style="padding: 0; margin: 0;"> {msg["content"]} </p>''')
    else: # This is an image message
        url = next(item["image_url"]["url"] for item in msg["content"] if item["type"] == "image_url")
        if False: st.html(f""" <div style="text-align: center; padding-top: 40px; padding-bottom: 20px;"> <img src="{url}" alt="Base64 Image" style="max-width: 100%; height: auto;"> </div> """)
        st.markdown(f"<h2 style='padding-top: 40px;'>{msg['content'][1]['text']}</h2>", unsafe_allow_html=True)

User = st.empty()
Stream = st.empty()

prompt = st.chat_input("Write a message")

if prompt and "file" in st.session_state:
    b64 = st.session_state.file
    st.session_state.messages.append({
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}", "detail": "high"}},
            {"type": "text", "text": prompt}
        ]
    })
    st.markdown(f"<h2 style='padding-top: 40px;'>{prompt}</h2>", unsafe_allow_html=True)
    completion = st.session_state.myai.client.chat.completions.create(
        model="grok-2-vision-1212",
        messages=st.session_state.messages,
        temperature=0.01,
    )
    text = completion.choices[0].message.content
    st.markdown(text)
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.session_state.pop("file", None)
elif prompt:    # If there is only a prompt
    Upload.empty()
    st.session_state.messages.append({"role": "user", "content": prompt})
    User.markdown(f"<h2 style='padding-top: 40px;'>{prompt}</h2>", unsafe_allow_html=True)
    stream = st.session_state.myai.get_stream(st.session_state.messages)
    text = write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": text})