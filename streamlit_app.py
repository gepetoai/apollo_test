import streamlit as st
from openai import OpenAI
from llm import generate_response

#SIDEBAR
st.sidebar.title("Inputs")
st.sidebar.write('modify these then press Start/Restart on the right')
apollo_api_key = st.sidebar.text_input("Apollo API Key", value = st.session_state.get("apollo_api_key", ""))
openai_api_key = st.sidebar.text_input("OpenAI API Key", value = st.session_state.get("openai_api_key", ""))


#MAIN PAGE
st.title("Steve")
if st.button("Start/Restart"):
    st.session_state.clear()
    st.session_state.messages = [{"role": "assistant", "content": "Let's find you some leads. I need: \n-company headcount range\n-locations\n-industry keywords\n-hard cap (default 10)."}]
    st.session_state.apollo_api_key = apollo_api_key
    st.session_state.openai_api_key = openai_api_key
    st.session_state.started = True
    st.rerun()

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

