# https://youtu.be/Dh0sWMQzNH4
# my_pdf_processor.py
from dotenv import load_dotenv
import os
from flask import request
import tempfile
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

load_dotenv()

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def process_pdf_query(pdf_path, query):
    text = read_pdf(pdf_path)

    # split into chunks
    char_text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, 
                                          chunk_overlap=200, length_function=len)

    text_chunks = char_text_splitter.split_text(text)
    
    # create embeddings
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(text_chunks, embeddings)
    
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")


    # process user query
    docs = docsearch.similarity_search(query)
    
    response = chain.run(input_documents=docs, question=query)
    return response

def save_pdf_to_tmp(pdf_data):
    try:
        # Create a temporary file in the /tmp directory
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(pdf_data)  # Write the PDF data to the temporary file

            # Get the temporary file path
            tmp_file_path = tmp_file.name

        # At this point, the temporary file has been created and written to.
        # You can use the 'tmp_file_path' variable to access the file location.

        return tmp_file_path

    except OSError as e:
        print(f"Error: {e}")
        return None