import streamlit as st
from extraction import extract_content
from metadata import generate_metadata
import json
import time

# Initialize session state
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'text_content' not in st.session_state:
    st.session_state.text_content = None

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
                                 accept_multiple_files=False,
                                 key="file_uploader")

# Process document only when new file is uploaded
if uploaded_file and (not st.session_state.processing_done or 
                     st.session_state.uploaded_file_name != uploaded_file.name):
    with st.spinner("Analyzing document..."):
        # Process document
        st.session_state.text_content = extract_content(uploaded_file)
        st.session_state.metadata = generate_metadata(st.session_state.text_content)
        st.session_state.processing_done = True
        st.session_state.uploaded_file_name = uploaded_file.name
        
    st.success("Metadata generated successfully!")

# Display results if processing is done
if st.session_state.processing_done:
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["Metadata", "Document Preview", "Raw Metadata"])
    
    with tab1:
        st.subheader("Core Metadata")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Title", st.session_state.metadata.get("title", "Untitled"))
            st.metric("Author", st.session_state.metadata.get("author", "Unknown"))
            st.metric("Date", st.session_state.metadata.get("date", "Undated"))
            
        with col2:
            st.metric("Sentiment", st.session_state.metadata.get("sentiment", "Neutral"))
            st.metric("Readability", st.session_state.metadata.get("readability", "Standard"))
            st.metric("Word Count", st.session_state.metadata["stats"]["word_count"])
        
        st.divider()
        st.subheader("Semantic Analysis")
        st.markdown("**Key Phrases:** " + ", ".join(st.session_state.metadata["keyphrases"]))
        st.markdown("**Topics:** " + ", ".join(st.session_state.metadata["topics"]))
        
        st.subheader("Summary")
        st.info(st.session_state.metadata["summary"])
    
    with tab2:
        st.subheader("Document Preview")
        st.text_area("Extracted Text", 
                    value=st.session_state.text_content[:3000] + ("..." if len(st.session_state.text_content) > 3000 else ""), 
                    height=400,
                    key="preview_text")
    
    with tab3:
        st.subheader("Raw Metadata")
        st.json(st.session_state.metadata)
    
    # Download button with fragment to prevent reload
    @st.fragment
    def download_fragment():
        st.download_button(
            label="Download Full Metadata (JSON)",
            data=json.dumps(st.session_state.metadata, indent=2),
            file_name=f"{st.session_state.uploaded_file_name.split('.')[0]}_metadata.json",
            mime="application/json",
            key="download_button"
        )
    
    download_fragment()
