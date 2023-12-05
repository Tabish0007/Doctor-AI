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



st.header("Hello, I'm a Doctor AI. How can I help you?")

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
# Streamlit UI
with st.form(key='my_form'):
    input_question = st.text_input("Type here.", key="input")

    # Apply custom HTML and CSS for styling
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
                width: 650px;
                /* Add any additional styling here */
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
        # st.subheader("Here you go,")
        st.write(response)
    else:
        st.subheader("Error: Unable to get response. Please try again later.")