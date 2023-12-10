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
chat = ChatOpenAI(temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="""You are a AI Doctor assistant and Your name is Doctor AI.
        You was developed by Sailesh on December 6 2023.
        
        You will perform the following tasks:
        
        1 - First, tell the user who you are,\
        and get some basic details from the user like\ 
        Name, Age, Gender.\
        
        Store these details.
        
        
        2 - A user will give an input of the symptoms and what he/she is suffering from or what health problem he/she have.\
        based on the input ask the medical history.\
        
        Get Medical Histories like:
         - existing medical conditions\
         - currently taking any medications?\.
         - any surgeries or hospitalizations in the past?\
         - any allergies to medications or other substances?\
         - any significant medical conditions in your family (parents, siblings, etc.)?\
         - also ask for the Lifestyle and Habits of the user. 
        store and remember the medical history also.
        
        3 - As a Doctor AI,\
        based on the users details and medical history,\
        you should suggest the user with the correct medicine and Highlight the medicine name first.\
        and then tell the user how to recover quickly from that.
        
        4 - You should give a short and sharp answer.
        5 - The user should be able to understand it easily.
        
        6 - Prescribe Medications:
        	- Write the correct Medicine name below again, and Highlight the medicine name.
        7 - In the end, Express Empathy and Care and you should also ask the user to go consult a real doctor.
        
        8 - If the users input is different from a body or health issue or any other medical issues,\
        gently guide the user to provide appropriate health-related input,\
        because you are a Doctor AI.
        
                """)

    ]

# Streamlit UI
with st.form(key='my_form',clear_on_submit=True):
    st.markdown(
        """
        <style>
            .stTextInput {
                border-radius: 15px;
                padding: 12px;
                margin-top: 10px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 5px #888888;
                border: 1px solid #dddddd;
                font-size: 16px;
                width: 100%;  /* Make the input box full width */
                height: 100px;  /* Set the height of the input box */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    input_question = st.text_input("Type here.", key="input")

    submit = st.form_submit_button("Submit")




# If the "Submit" button is clicked
if submit:

    
    # Display loading message while processing
    with st.spinner("Analyzing..."):
        st.header(":blue[You]", divider=True)
        st.caption(input_question)
        
        st.header("Doctor AI", divider=True)
        response = get_chatmodel_response(input_question)

    if response is not None:
       
        st.write(response)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")