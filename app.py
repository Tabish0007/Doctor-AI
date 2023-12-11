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
st.set_page_config(page_title="Doctor AI", page_icon="💊", layout="centered", initial_sidebar_state="collapsed")


st.header("Hello, I am Doctor AI. How can I help you?")

from dotenv import load_dotenv
load_dotenv()
import os

# ChatOpenAI class
chat = ChatOpenAI(temperature=0.1)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="""You are a AI Doctor assistant and Your name is Doctor AI.\
            Sailesh developed you on December 6, 2023.
            
            You will perform the following tasks:
            
            1 - First, tell the user who you are,\
            and get some basic details from the user like\ 
            get one by one:
                1. Name,
                2. Age, 
                3. Gender.
            
            Store these details.
            
            
            2 - A user will give an input of the symptoms and what he/she is suffering from or what health problem he/she have.\
            based on the input ask for the medical history.\
            
            Get the Medical Histories of the user One by One. it will be easy to Diagnose.
             
            
            3 - As a Doctor AI,\
            based on the user's details and medical history,\
            
            suggest the user with the correct medicine and Highlight the medicine name first.\
            
            and then tell the user how to recover quickly from that.
            
            4 - You should give a short and sharp answer.
            
            5 - The user should be able to understand it easily.
            
            6 - Prescribe Medications:
            	- Write the correct Medicine name below again, and Highlight the medicine name.
            7 - In the end, Express Empathy and Care, and you should also ask the user to consult a real doctor.
            
            8 - If the user input is different from a body or health issue or any other medical issues,\
            gently guide the user to provide appropriate health-related input,\
            because you are a Doctor AI.
            """)

    ]


# Display conversation history
for message in reversed(st.session_state['flowmessages']):
    if isinstance(message, AIMessage):
        st.header("Doctor AI", divider=True)
        st.write(message.content)
    elif isinstance(message, HumanMessage):
        st.header(":blue[You]", divider=True)
        st.write(message.content)

# Input box and form at the bottom
with st.form(key='my_form', clear_on_submit=True):
    input_question = st.text_input("Type here.")
    submit = st.form_submit_button("Ask Doctor AI")
    # Use st.empty() to create an empty space to the right of the form
    placeholder = st.empty()
    # Add a "Clear Chat" button to the right of the form
    clear_chat_button = placeholder.button("Clear Chat")

# If the "Clear Chat" button is clicked
if clear_chat_button:
    # Clear the entire session and chat
    st.session_state['flowmessages'] = []

# If the "Submit" button is clicked
if submit:
    # Get Doctor AI's response
    response = get_chatmodel_response(input_question)

    if response is not None:
        # Display conversation history
        for message in reversed(st.session_state['flowmessages']):
            if isinstance(message, AIMessage):
                st.header("Doctor AI", divider=True)
                st.write(message.content)
            elif isinstance(message, HumanMessage):
                st.header(":blue[You]", divider=True)
                st.write(message.content)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")