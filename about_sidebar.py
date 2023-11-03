# about_sidebar.py
import streamlit as st

##################################################
# About Brian Lesko
def about():
    with st.sidebar:

        st.subheader("About")
        st.write('  ') 
        col1, col2, = st.columns([1,5], gap="medium")

        with col1:
            st.image('docs/bl.png')

        with col2:
            st.write(""" 
            Hey it's Brian,
                    
            This is a [Low-Code Python](https://github.com/BrianLesko/Low-Code-Chat/blob/main/low-code-chat.py) UI for ChatGPT.
                     
            It's written with less than 100 lines of code.
                    
            You'll need an OpenAI key to use this app, paste it below.
            """)

        col1, col2, col3, col4, col5, col6 = st.columns([1.1,1,1,1,1,1.5], gap="medium")
        with col2:
            # TWITTER
            "[![X](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/x-logo-blue.svg)](https://twitter.com/BrianJosephLeko)"
        with col3:
            # GITHUB
            "[![Github](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/github-mark-blue.svg)](https://github.com/BrianLesko)"
        with col4:
            # LINKEDIN
            "[![LinkedIn](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/linkedin-icon-blue.svg)](https://www.linkedin.com/in/brianlesko/)"
        with col5:
            # YOUTUBE
            "."
            #"[![LinkedIn](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/yt-logo-blue.svg)](https://www.linkedin.com/in/brianlesko/)" 
        with col6:
            # BLOG Visual Study Code
            "."
            #"[![VSC]()](https://www.visualstudycode.com/)"
