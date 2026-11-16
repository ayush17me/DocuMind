import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from core import build, chat_model, run

load_dotenv()
st.title("DocuMind")
st.session_state.setdefault("history", [])
uploads = st.sidebar.file_uploader("Study PDFs",type=["pdf"],accept_multiple_files=True)
if st.sidebar.button("Process documents",disabled=not uploads):
    try:
        pages = []
        for number,upload in enumerate(uploads,1):
            upload.seek(0)
            for page_index,page in enumerate(PdfReader(upload).pages,1):
                pages.append((f"D{number}-p{page_index}",page.extract_text() or ""))
        st.session_state.index = build(pages)
        st.session_state.names = [u.name for u in uploads]
        st.session_state.history = []
    except Exception as exc:
        st.error(f"Indexing failed ({type(exc).__name__}).")
for i,name in enumerate(st.session_state.get("names",[]),1):
    st.sidebar.text(f"D{i}: {name}")
verify = st.sidebar.checkbox("Check answer against passages")
if st.sidebar.button("Clear conversation"):
    st.session_state.history = []
for question,answer in st.session_state.history:
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(answer)
if q := st.chat_input("Ask about the indexed PDFs",disabled="index" not in st.session_state):
    st.chat_message("user").write(q)
    try:
        answer,trace = run(st.session_state.index,chat_model(),q,st.session_state.history,verify)
        st.session_state.history.append((q,answer))
        st.chat_message("assistant").write(answer)
        with st.expander("Request measurements"):
            st.json(trace)
    except Exception as exc:
        st.error(f"Request failed ({type(exc).__name__}). See the service log for the failed stage.")
