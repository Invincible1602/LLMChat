# src/ui/sidebar.py
import streamlit as st
import requests
import os

def render_sidebar():
    st.sidebar.header("Configuration")

    # PDF Upload Section
    st.sidebar.subheader("Upload PDF for Knowledge Base")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Processing PDF... This might take a moment."):
            try:
                # Save the uploaded file temporarily
                temp_file_path = os.path.join("temp_uploads", uploaded_file.name)
                os.makedirs("temp_uploads", exist_ok=True)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Send the PDF to the FastAPI backend
                files = {'file': (uploaded_file.name, open(temp_file_path, 'rb'), 'application/pdf')}
                response = requests.post("http://localhost:8000/upload-pdf", files=files) # Adjust URL if needed
                
                if response.status_code == 200:
                    st.sidebar.success(response.json().get("message", "PDF uploaded and processed successfully!"))
                else:
                    st.sidebar.error(f"Error processing PDF: {response.json().get('detail', 'Unknown error')}")
                
                # Clean up the temporary file
                os.remove(temp_file_path)

            except Exception as e:
                st.sidebar.error(f"An error occurred during PDF upload: {e}")

    st.sidebar.markdown("---")
    st.sidebar.info("Upload a PDF to build the knowledge base for the chatbot.")

