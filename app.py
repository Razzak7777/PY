import requests
import streamlit as st

# Set up API endpoint and key directly in the code
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with your actual API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Initialize the session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to send messages to the Llama 3 API and receive a response
def call_llama_api(messages):
    payload = {
        "model": "llama3-8b-8192",
        "messages": messages
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Sidebar with a button to clear chat history
with st.sidebar:
    if st.button("Clear Chat History"):
        st.session_state["messages"] = []

# Display the chat messages
st.title("<LordsGPT 🤖>")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"*User:* {message['content']}")
    else:
        st.markdown(f"*Assistant:* {message['content']}")

# Input field for user to enter a message
if user_input := st.chat_input("Ask me anything!"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call the Llama 3 API
    try:
        response = call_llama_api(st.session_state.messages)
        assistant_response = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        # Display the latest assistant response
        st.markdown(f"*Assistant:* {assistant_response}")
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    except KeyError:
        st.error("Unexpected response structure from API.")
