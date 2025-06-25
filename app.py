import streamlit as st
import tempfile
import os
from extraction import extract_content
from semantic_analysis import generate_metadata
import json

st.set_page_config(page_title="MetaMind", page_icon="🧠")
st.title("🧠 MetaMind: Automated Metadata Generator")
st.markdown("Upload your document (PDF, DOCX, or TXT) to generate semantic-rich metadata.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner("Extracting text..."):
            text = extract_content(tmp_path)
        with st.spinner("Analyzing and generating metadata..."):
            metadata = generate_metadata(text)
        st.success("Metadata generated successfully!")

        st.subheader("Document Preview")
        st.text_area("Extracted Text", value=text[:2000] + ("..." if len(text) > 2000 else ""), height=300)

        st.subheader("Metadata")
        st.json(metadata)

        st.download_button(
            label="Download Metadata (JSON)",
            data=json.dumps(metadata, indent=2),
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_metadata.json",
            mime="application/json"
        )
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        os.unlink(tmp_path)
