import streamlit as st
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "notes" not in st.session_state:
    st.session_state.notes = None

st.title("DIGESTIFY")
#initialize the chat history

#display chat messages before input and on each rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
prompt= st.chat_input("Ask a question...")
if prompt:
    #first display users prompt
    with st.chat_message("user"):
        st.markdown(prompt)
    #add the prompt to history
    st.session_state.messages.append({"role":"user", "content":prompt})

    response= "This is the default response"
    with st.chat_message("assistant"):
        st.markdown(response)
    #add it to history
    st.session_state.messages.append({"role":"assistant", "content":response})
st.sidebar.title("📚Your AI Study Mate!")
uploaded_file= st.sidebar.file_uploader("Upload your PDF file", type=['pdf'])
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    st.sidebar.success(f"{uploaded_file.name} uploaded successfully!")
if st.sidebar.button("Generate Notes", width=400):
    pass
if st.sidebar.button("Download Notes", width=400):
    pass

