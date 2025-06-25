import streamlit as st
from extraction import extract_content
from metadata import generate_metadata
import json

st.set_page_config(
    page_title="Metamuse Pro",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Metamuse Pro - Intelligent Metadata Extraction")
st.markdown("Upload documents to generate rich semantic metadata automatically")

# File upload with drag-and-drop
uploaded_file = st.file_uploader("Drag & drop a document", 
                                 type=["pdf", "docx", "txt"],
                                 accept_multiple_files=False)

if uploaded_file:
    with st.spinner("Analyzing document..."):
        # Process document
        text_content = extract_content(uploaded_file)
        metadata = generate_metadata(text_content)
        
    st.success("Metadata generated successfully!")
    
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["Metadata", "Document Preview", "Raw Metadata"])
    
    with tab1:
        st.subheader("Core Metadata")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Title", metadata.get("title", "Untitled"))
            st.metric("Author", metadata.get("author", "Unknown"))
            st.metric("Date", metadata.get("date", "Undated"))
            
        with col2:
            st.metric("Sentiment", metadata.get("sentiment", "Neutral"))
            st.metric("Readability", metadata.get("readability", "Standard"))
            st.metric("Word Count", metadata["stats"]["word_count"])
        
        st.divider()
        st.subheader("Semantic Analysis")
        st.markdown("**Key Phrases:** " + ", ".join(metadata["keyphrases"]))
        st.markdown("**Topics:** " + ", ".join(metadata["topics"]))
        
        st.subheader("Summary")
        st.info(metadata["summary"])
    
    with tab2:
        st.subheader("Document Preview")
        st.text_area("Extracted Text", 
                    value=text_content[:3000] + ("..." if len(text_content) > 3000 else ""), 
                    height=400)
    
    with tab3:
        st.subheader("Raw Metadata")
        st.json(metadata)
    
    # Download button
    st.download_button(
        label="Download Full Metadata (JSON)",
        data=json.dumps(metadata, indent=2),
        file_name=f"{uploaded_file.name.split('.')[0]}_metadata.json",
        mime="application/json"
    )
