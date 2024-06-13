import streamlit as st
import requests
import pandas as pd
from io import StringIO

st.title("CSV Data Visualization")

# Upload file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Text input for file name
file_name = st.text_input("Enter the file name", value="Sample")

# Dropdown to select file encoding
encoding = st.selectbox(
    "Select the file encoding",
    options=["utf-8", "iso-8859-1", "latin1", "windows-1252"]
)

if uploaded_file is not None and file_name:
    try:
        # Read the file with the selected encoding
        stringio = StringIO(uploaded_file.getvalue().decode(encoding))
        df = pd.read_csv(stringio)
        
        # Display the dataframe
        st.write("### DataFrame")
        st.dataframe(df)
        
        # Display summary statistics
        st.write("### Summary Statistics")
        st.write(df.describe())
        
        # Visualization (example: histogram of the first column)
        st.write("### Histogram of the first column")
        st.bar_chart(df.iloc[:, 0])

        # Send the file and file name to the FastAPI backend
        files = {"file": uploaded_file.getvalue()}
        data = {"file_name": file_name}
        response = requests.post("http://localhost:8000/upload-csv/", files=files, data=data)
        
        if response.status_code == 200:
            st.write("File successfully uploaded to the backend")
            st.json(response.json())
        else:
            st.write("Failed to upload file")
    
    except UnicodeDecodeError:
        st.error(f"Could not decode the file with {encoding} encoding. Please try a different encoding.")
    except requests.ConnectionError:
        st.error("Failed to connect to the FastAPI backend. Please ensure the server is running.")
