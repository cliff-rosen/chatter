#from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from api.answer import create_prompt_text, create_prompt_messages
#from utils import kb_service as kb, logging
from db import db
import json
import datetime

import streamlit as st

# Initialize session state to persist history across app reruns 
if 'history' not in st.session_state:
    st.session_state['history'] = []

history = st.session_state['history'] 

st.title("Chat App")

message = st.chat_input("Enter your message: ")

if message:
    history.append(message) 

for cm in history:
    message = st.chat_message("user")
    message.write(cm)

print(history)
