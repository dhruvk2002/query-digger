from dotenv import load_dotenv
load_dotenv() ## Load all the environment variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

#Configue our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load google gemini model

def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0], question])
    return response.text

## Function to retrive query from database

def read_sql_query(sql, db):
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION and MARKS \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Creating streamlit app

st.set_page_config(page_title="I can retrive any SQL query",page_icon="logo.png", layout="wide")
st.header("Application to retrieve SQL data using Google Gemini")

question=st.text_input("Enter the question: ",key="input")

submit=st.button("Ask the question")

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response, "student.db")
    st.subheader("The response is:")
    for row in data:
        print(row)
        st.header(row)
