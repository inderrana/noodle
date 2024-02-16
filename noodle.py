import streamlit as st
import secrets
from hugchat import hugchat

# App title
st.set_page_config(page_title="noodle", page_icon="🍜")


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
def generate_response(prompt_input, access_token, web_search=False):
    # Create ChatBot
    cookies = {"hf_token": access_token}
    chatbot = hugchat.ChatBot(cookies=cookies)
    return chatbot.chat(prompt_input, web_search=web_search)

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
st.sidebar.title("Noodley Options🍜🍜")

st.sidebar.write("---")

# Start/reset conversation button
if st.sidebar.button("Start/Reset Conversation"):
    st.session_state.access_token = generate_access_token()
    st.session_state.conversation_id = None
    st.sidebar.success("Conversation Started")


st.sidebar.write("---")


if st.sidebar.checkbox("What does this button do?", key="show_giphy"):
    st.sidebar.image("https://media.giphy.com/media/3ov9jQX2Ow4bM5xxuM/giphy.gif", caption="😇", use_column_width=True)


