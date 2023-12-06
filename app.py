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
# # Set page background
# st.markdown(
#     """
#     <style>
#         body {
#             background-color: #f0f0f0;  /* Set your desired background color */
#         }
#         .stTextInput, .stButton {
#             border-radius: 50px;  /* Add border-radius for a nicer input bar */
#             padding: 50px;  /* Adjust padding for better spacing */
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



st.header("Hello, I am Doctor AI. How can I help you?")

from dotenv import load_dotenv
load_dotenv()
import os

# ChatOpenAI class
chat = ChatOpenAI(temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="You are an AI Doctor assistant. Your name is Doctor AI. A user will give input of what they are suffering from or what health problem they have. As a Doctor AI, suggest the user with the correct medicine and Highlight the medicine name first. and then tell them how to recover quickly from it. Give a short and sharp answer. If the input is different from a body or health issue or any other medical issues, gently guide the user to provide appropriate health-related input.")

    ]

# Streamlit UI
with st.form(key='my_form'):
    input_question = st.text_input("Type here.", key="input")

    # Apply custom HTML and CSS for styling
    st.markdown(
        """
        <style>
            /* Add any additional styling here */
            .stTextInput {
                border-radius: 15px;
                padding: 12px;
                margin-top: 10px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 5px #888888;
                border: 1px solid #dddddd;
                font-size: 16px;
                height:100%;
                width: 40%;
                box-sizing: border-box;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    

    submit = st.form_submit_button("Submit")




# If the "Ask" button is clicked
if submit:

    
    # Display loading message while processing
    with st.spinner("Analyzing..."):
        response = get_chatmodel_response(input_question)

    if response is not None:
       
        st.write(response)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")