import streamlit as st
from openai import OpenAI
from llm import generate_response

st.title("Steve")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's find you some leads. I need a company headcount range, locations, industry keywords, and a hard cap (default is 10)."}]

if st.session_state.get("started", False) == True:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Input here"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        response = generate_response(messages)
        print(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if st.sidebar.button("Start/Restart"):
    #clear the entire session state
    st.session_state.clear()
    st.session_state['started'] = True
    #rerun
    st.rerun()

# if not st.session_state.get('Apollo API Key'):
#     st.session_state.apollo_api_key = ""

# if not st.session_state.get('chunks'):
#     st.session_state.chunks = ""



# st.sidebar.text_input("Apollo API Key", value = st.session_state.summary)


# st.sidebar.text_input("Chunks", value = st.session_state.chunks)