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
                    st.markdown(f"""<div style="height: 80vh; background-color: white;" class="flex flex-col"> <div>{text}</div>""", unsafe_allow_html=True)
    return text
 # {"Original" if i == len(messages) else "Iteration" + str(len(messages) - i)}
def write_recursive_stream(stream, messages):
    tab_name = "Most concise"
    past_tabs = " ".join(f'''
    <input type="radio" name="my_tabs_2" role="tab" class="tab p-2 m-2" aria-label="tabn" /> 
    <label for="tab_{i}" class="p-2 m-2 tab-label"><!-- This is the visible text -->{ "Original" if i == len(messages) else f"Iteration {len(messages) - i}" }
    </label>
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6 m-6">
        <div style="padding: 10px; margin: 10px;">
            {s}
        </div>
    </div>''' for i, s in enumerate(reversed(messages)))
    text = "\n"
    for chunk in stream:
        chunk_text = chunk.choices[0].delta.content
        if chunk_text is not None:
            text += chunk_text
            # build our HTML
            my_html = f"""
                <div role="tablist" class="tabs tabs-lifted p-6">
                    <input type="radio" name="my_tabs_2" role="tab" class="tab" aria-label="{tab_name}" checked="checked" />
                    <label for="tab" class="p-2 m-2 tab-label"> 
                        <!-- This is the visible text -->
                        Most Concise
                    </label>
                    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6 m-6">
                        <div style = "padding: 10px; margin: 10px;">
                        {text}
                        </div>
                    </div>{past_tabs}
                </div>
            """
            # Display in Streamlit
            # (If you only want to show the final result once all chunks have arrived)
            with Stream:
                if do_html:
                    st.html(f"""<p>{text}</p>""")
                else:
                    st.markdown(f"""<div style="min-height: 80vh; background-color: white;" class="flex flex-col">{my_html}</div>""",unsafe_allow_html=True)
    return text

st.set_page_config(page_title='LLM0',page_icon='')
tailwind_cdn = """
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.23/dist/full.min.css" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
"""
st.markdown(tailwind_cdn, unsafe_allow_html=True)
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

st.session_state.myai.setup()

Title = st.empty()
Title.markdown('<h1 style="text-align: center; padding-top: 60px;">My llm</h1>', unsafe_allow_html=True)
Upload = st.empty()
Chat = st.empty()

file = Upload.file_uploader("", accept_multiple_files=False)
if file: st.session_state.file = st.session_state.myai._reduce_image_size(file)
if "file" in st.session_state:
    b64 = st.session_state.file
    st.html(f"""
        <div style="text-align: center; padding-top: 40px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{b64}" alt="Base64 Image" style="max-width: 100%; height: auto; border-radius: 10px;">
        </div>
    """)

if "messages" not in st.session_state:
    st.session_state["messages"] = []
else:
    Title.empty()
    Upload.empty()

do_html = st.sidebar.checkbox("Use HTML", value=False)
recursion = st.sidebar.checkbox("Recursion", value=True)
recursion_instances = 0
if recursion:
    recursion_instances = st.sidebar.number_input("Recursion Instances", value=3)
    recursion_prompt = st.sidebar.text_input("Recursion Prompt", value="Be more terse.")

# Display all the historical messages
def write_history(messages):
    to_write = [""]
    for msg in messages:
        if msg["role"] == "system":
            continue  # Skip system messages
        if msg["role"] == "user":
            to_write.append("\n ##  " + msg["content"])
        else: 
            to_write.append(msg["content"])
    History.markdown(f"<div style='padding-top: 40px;'>{"\n".join(to_write)}</div>", unsafe_allow_html=True)


def write_mixed_content_history(messages):
    # Similar to the unified approach, but specifically assumes
    # each user message has a list with image + text blocks
    to_write = [""]
    for msg in messages:
        if msg["role"] == "system":
            continue

        content_str = ""
        for block in msg["content"]:
            if block["type"] == "image_url":
                image_url = block["image_url"]["url"]
                content_str += f"![User image]({image_url})\n\n"
            elif block["type"] == "text":
                content_str += block["text"]

        if msg["role"] == "user":
            to_write.append(f"\n ##  {content_str}")
        else:
            to_write.append(content_str)

    History.markdown(
        f"<div style='padding-top: 40px;'>{'\n'.join(to_write)}</div>",
        unsafe_allow_html=True
    )

def write_msg(msg):
    if isinstance(msg["content"], str):  # This is a text message
        if msg["role"] == "user":
            st.markdown(f"<h2 style='padding-top: 40px;'>{msg['content']}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f'''<p style="padding: 0; margin: 0;"> {msg["content"]} </p>''', unsafe_allow_html=True)
    else:  # This is an image message
        url = next(item["image_url"]["url"] for item in msg["content"] if item["type"] == "image_url")
        st.markdown(f"<h2 style='padding-top: 40px;'>{msg['content'][1]['text']}</h2>", unsafe_allow_html=True)

History = st.empty()
if recursion: write_history(st.session_state.messages)
else: write_mixed_content_history(st.session_state.messages)
User = st.empty()
Stream = st.empty()

prompt = st.chat_input("Write a message")

count = 0 
messages = []
while prompt:
    # If there is a prompt and an image
    if "file" in st.session_state:
        b64 = st.session_state.file
        st.session_state.messages.append({
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}", "detail": "high"}}, # add the upload every time we send a new query
                {"type": "text", "text": prompt}
            ]
        })
        User.markdown(f""" ##  {prompt} """, unsafe_allow_html=True)
        completion = st.session_state.myai.client.chat.completions.create(
            model="grok-2-vision-1212",
            messages=st.session_state.messages,
            temperature=0.01,
        )
        text = completion.choices[0].message.content
        st.markdown(text)
        st.session_state.messages.append({"role": "assistant", "content": [{"type": "text", "text": text}]})
        st.session_state.pop("file", None)
        break
    # If there is only a prompt
    else:
        if count == 0: st.session_state.messages.append({"role": "user", "content": prompt})
        Stream.html("""<div style="height: 80vh; background-color: white;"></div>""")
        
        User.markdown(f""" ##  {prompt} """, unsafe_allow_html=True)
        stream = st.session_state.myai.get_stream(st.session_state.messages+messages+ ([{"role": "system", "content": recursion_prompt}] if recursion and count>0 else []))

        if not recursion: 
            text = write_stream(stream)
        else: 
            strings = [message["content"] for message in messages if "content" in message]
            text = write_recursive_stream(stream, strings)
            messages.append({"role": "assistant", "content": text})
        #st.session_state.messages.append({"role": "assistant", "content": text})

        if count >= recursion_instances or not recursion:
            # add the last message to the history
            if recursion: 
                st.session_state.messages.append(messages[-1])
            else: 
                st.session_state.messages.append({"role": "assistant", "content": text})
            break
        else: 
            count = count + 1
messages = []