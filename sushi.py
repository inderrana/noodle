import streamlit as st
import secrets
from hugchat import hugchat

# App title
st.set_page_config(page_title="Sushi", page_icon="🖖")



st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.markdown(
    """
   <style>
   [data-testid="stSidebar"][aria-expanded="true"]{
       max-width: 768px;
   }
   """,
    unsafe_allow_html=True,
)

padding = 0
st.markdown(f"""
<style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style>
    """, unsafe_allow_html=True)

# Function to generate a random access token (cookie)
def generate_access_token():
    return secrets.token_hex(16)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Function for generating LLM response
def generate_response(prompt_input, access_token):
    # Create ChatBot
    cookies = {"hf_token": access_token}
    chatbot = hugchat.ChatBot(cookies=cookies)
    return chatbot.chat(prompt_input)

# User-provided prompt
if prompt := st.chat_input(disabled="access_token" not in st.session_state):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new access token (cookie) if not provided
if "access_token" not in st.session_state:
    st.session_state.access_token = generate_access_token()

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, st.session_state.access_token)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


# Sidebar options
st.sidebar.title("Session Options")
if st.sidebar.button("Start Session", key="start_session"):
    st.session_state.access_token = generate_access_token()
    st.sidebar.success("Session Started")
