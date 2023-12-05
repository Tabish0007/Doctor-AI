import streamlit as st
import time
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI


def get_chatmodel_response(question):
    # Retry logic
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            st.session_state['flowmessages'].append(HumanMessage(content=question))
            answer = chat(st.session_state['flowmessages'])
            st.session_state['flowmessages'].append(AIMessage(content=answer.content))
            return answer.content
        except Exception as e:
            print(f"Error: {e}")
            if "Rate limit" in str(e):
                print(f"Rate limit exceeded. Waiting and retrying...")
                time.sleep(5)  # Adjust the waiting time as needed
                retries += 1
            else:
                print("Unhandled exception. Please try again later.")
                break

    print("Exceeded the maximum number of retries. Please try again later.")
    return None

# Streamlit app setup
st.set_page_config(page_title="Doctor AI")
st.header("Hello, I'm a Doctor AI. how can I help you?")

from dotenv import load_dotenv
load_dotenv()
import os

# ChatOpenAI class
chat = ChatOpenAI(temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="Your are an AI Doctor assistant. A user will give an input of what he is suffering from or what health problem he has, you should suggest the user with correct medicine and tell the user how to recover fastly from it. Gve a short and sharp answer. If the input is different from a body or health issue or any other medical issues, tell the user who you are and ask the user to provide the appropriate input.")
    ]

# Streamlit UI
input_question = st.text_input("Type here.", key="input")
submit = st.button("Submit")

# If the "Ask" button is clicked
if submit:
    response = get_chatmodel_response(input_question)

    if response is not None:
        # st.subheader("Here you go,")
        st.write(response)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")