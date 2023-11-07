#from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from api.answer import create_prompt_text, create_prompt_messages
#from utils import kb_service as kb, logging
from db import db
import json
import datetime

import streamlit as st
import pandas as pd
import numpy as np
import time


click_tracker = [False, False, False]

data = [
  {'name': 'John', 'age': 30},
  {'name': 'Mary', 'age': 25},
  {'name': 'Peter', 'age': 20}
]

selected_row = None 

col1, col2 = st.columns(2)

with col1:
  for index, row in enumerate(data):
    click_tracker[index] = st.button(row['name'])

with col2:
    for index, row in enumerate(data):
       if click_tracker[index]:
        st.write(index)
