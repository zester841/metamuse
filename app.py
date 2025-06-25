import streamlit as st
import os
import tempfile
from extraction import extract_content
from semantic_analysis import generate_metadata
import json

st.title("MetaMind - Automated Metadata Generator")
st.markdown("Upload documents to generate semantic-rich metadata automatically")

# File uploader
uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name
    
    try:
        # Extract content
        with st.spinner("Extracting content..."):
            text_content = extract_content(file_path)
        
        # Generate metadata
        with st.spinner("Analyzing content and generating metadata..."):
            metadata = generate_metadata(text_content)
        
        # Display results
        st.subheader("Extracted Text Preview")
        st.text_area("", value=text_content[:2000] + ("..." if len(text_content) > 2000 else ""), height=300)
        
        st.subheader("Generated Metadata")
        st.json(metadata)
        
        # Download button
        st.download_button(
            label="Download Metadata as JSON",
            data=json.dumps(metadata, indent=2),
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_metadata.json",
            mime="application/json"
        )
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
    finally:
        os.unlink(file_path)  # Clean up temp file
