import streamlit as st

st.title("I wish you enjoyed our little app !")
st.write("We would really appreciate a feedback")

sentiment_mapping = ["one","two","three","four","five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

txt = st.text_area("What motivates your choice ?")

st.write(txt)