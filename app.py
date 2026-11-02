import streamlit as st

st.set_page_config(page_title="SpendEasy", page_icon="💰", layout="wide")

st.title("Welcome to SpendEasy! 💰")    
st.subheader("Your personal Expense Tracker and Management System!")
st.write("Welcome!, Let's get a leash on your expenses! ")
st.sidebar.title("Navigation")

menu=st.sidebar.radio("Go to",["Dashboard","Add Expense","View Expenses"])

if menu=="Dashboard":
    st.header("Dashboard")
    st.write("Your Financial Overview")

elif menu=="Add Expense":
    st.header("Add Expense")
    st.write("Add your expenses.")
    
elif menu=="View Expenses":
    st.header("View Expenses")
    st.write(" View your Transactions and Expenses.")
