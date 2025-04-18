import json
import pandas as pd
import traceback
from src.mcqgenerator.utills import read_file,get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain

# json file
with open('response.json','r') as file:
    RESPONSE_JSON= json.load(file)

st.title("MCQ Generator App with LangChain")

with st.form("user_inputs"):
    uploaded_file= st.file_uploader("Upload a file", type=["txt", "pdf"])

    mcq_count=st.number_input("Number of MCQs to generate", min_value=1, max_value=10)
    
    subject=st.text_input("Insert Subject",max_chars=20)

    tone=st.text_input("Complexity level of MCQs", max_chars=20,placeholder="simple")

    button=st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text=read_file(uploaded_file)
                response=generate_evaluate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                    }
                )
                
            except Exception as e:
                logging.error(f"Error: {e}")
                traceback.print_exc()
                st.error("An error occurred while generating MCQs.")

            else:
                if isinstance(response, dict):

                    quiz=response.get("quiz")
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review",value=response.get("review"), height=300)
                        else:
                            st.error("No quiz data found in the response.")

                else:
                    st.write(response)