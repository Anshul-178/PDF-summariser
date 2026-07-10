from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import time
import fitz
import streamlit as st
load_dotenv() 
st.title("PDF summariser")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""
    for page in pdf:
        text += page.get_text()

       
if st.button("Submit"):
    model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite",temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        (
        "system",
        "You are an expert document summarizer."
    ),
    (
        "human",
        """Summarize the following document in simple language.

Document:
{text}
"""
    )
])


    chain = prompt | model | StrOutputParser()
    if text is not None:
        result = chain.invoke({"text": text})
        with st.spinner("processing pdf"):
            time.sleep(5)
        st.success("completed")
        st.write(result)