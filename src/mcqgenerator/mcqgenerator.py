import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utills import read_file,get_table_data
from src.mcqgenerator.logger import logging

## importing langchain packages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import PyPDF2

load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

TEMPLATE="""
TEXT: {text}
You are an expert MCQ maker. Given the above text, your jsob is to \
create a quiz of {number} multiple-choice questions for {subject} students in a {tone} tone. 
Make sure the questions are not repeated and are strictly based on the given text.
Format your response like the RESPONSE_JSON shown below and use it as a guide. \
Ensure to generate exactly {number} MCQs.
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt= PromptTemplate(
    input_variable=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, \
You need to evaluate the complexity of the questions and provide a concise analysis of the quiz (maximum 50 words). 
If any questions are not appropriate for the students'. \
cognitive and analytical level, update them accordingly. 
Also adjust the tone to better suit the students.
Quiz_MCQs:
{quiz}
Expert feedback from an English writer:
"""
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],output_variables=["quiz", "review"], verbose=True)
