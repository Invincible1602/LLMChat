# src/ui/chatbot.py
import streamlit as st
import requests
import uuid

# FastAPI backend URL (adjust if your backend runs on a different port/host)
API_BASE_URL = "http://localhost:8000"

def render_chatbot():
    st.title("PDF-Powered Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask me anything about the PDF..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={"message": prompt, "session_id": st.session_state.session_id}
                    )
                    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
                    bot_response = response.json().get("response", "Sorry, I couldn't get a response.")
                except requests.exceptions.RequestException as e:
                    bot_response = f"Error connecting to the chatbot service: {e}"
                except Exception as e:
                    bot_response = f"An unexpected error occurred: {e}"
            
            st.markdown(bot_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

