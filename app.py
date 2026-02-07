import streamlit as st
import textwrap
 # only if YT is still .ipynb
import YT as lch

st.title("YouTube Assistant")

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.text_area(
            label="What is the YouTube video URL?",
            height=50
        )
        query = st.text_area(
            label="Ask me about the video?",
            height=50,
            key="query"
        )
        
        submit_button = st.form_submit_button(label='Submit')

if submit_button and query and youtube_url:
    db = lch.create_db_from_youtube_video_url(youtube_url)
    response, docs = lch.get_response(db, query)

    st.subheader("Answer:")
    st.text(textwrap.fill(response, width=85))
