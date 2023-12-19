import streamlit as st
import time
import openai
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
st.set_page_config(page_title="Doctor AI", page_icon="💊", layout="wide", initial_sidebar_state="collapsed")


st.header("Hello, I am Doctor AI. How can I help you?")

from dotenv import load_dotenv
load_dotenv()
import os

# ChatOpenAI class
chat = ChatOpenAI(temperature=0)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="""You are an AI Doctor assistant named Doctor AI, developed by Sailesh on December 6, 2023.

Perform the following tasks:

**Step 1: Introduction**
- Introduce yourself to the user.
- Gather basic details from the user:
  1. Name
  2. Age
  3. Gender
  Store these details for reference.

**Step 2: Symptom Input**
- Prompt the user to describe their symptoms or health concerns.
- Based on the input, inquire about the user's medical history.
  Gather medical histories one by one to facilitate diagnosis.

**Step 3: Medical Recommendation**
- Analyze the user's details and medical history.
- Suggest appropriate medication and highlight the medicine name.
- Provide guidance on how to recover quickly.

**Step 4: Concise Response**
- Respond with a brief and clear answer.

**Step 5: User Comprehension**
- Ensure that the user can easily understand the information provided.

**Step 6: Prescription**
- Prescribe medications by writing the correct medicine names.
- Highlight the medicine names for emphasis.
- Give the medicine names in this order:\
    1. Medicine name 1
    2. Medicine name 2
    3. Medicine name 3
    and go on if you have more.

**Step 7: Express Empathy and Caution**
- Express empathy and care towards the user.
- Advise the user to consult a real doctor for further assistance.

**Step 8: Handling Different Inputs**
- If the user input is unrelated to health issues, gently guide them to provide relevant health-related information.

""")
]



# Streamlit UI
with st.form(key='my_form', clear_on_submit=True):
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
                width: 100%;
                height: 100px;
            }
            .blue-text {
                color: blue;
            }
            .black-text {
                color: black;
            }
            .separator {
                border-top: 2px solid #888888;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    input_question = st.text_input("Type here.", key="input")
    submit = st.form_submit_button("Ask Doctor AI")




# Add a "Clear Chat" button next to the "Submit" button
clear_chat_button = st.button("Start a New Chat", key="clear_button")

# If the "Clear Chat" button is clicked
if clear_chat_button:
    # Clear the entire session and chat
    st.session_state['flowmessages'] = []
    
# If the "Submit" button is clicked
if submit:
    # Display loading message while processing
    with st.spinner("Analyzing..."):
        # Get Doctor AI's response
        response = get_chatmodel_response(input_question)

        if response is not None:
            # Display conversation history
            for message in st.session_state['flowmessages']:
                if isinstance(message, AIMessage):
                    st.header("Doctor AI", divider=True)
                    st.write(message.content)
                elif isinstance(message, HumanMessage):
                    st.header(":blue[You]", divider=True)
                    st.write(message.content)

            # Text-to-speech
            audio_response = openai.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=response
            )
    
            # Embed audio in the webpage without saving it
            st.audio(audio_response.content, format="audio/mp3")  


                    
        else:
            st.subheader("Error: Unable to get response. Please try again later.")


            