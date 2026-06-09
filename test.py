import streamlit as st

st.set_page_config(page_title="Test App", layout="centered")

st.title("✅ Δοκιμαστική Εφαρμογή")
st.write("Αν βλέπεις αυτό το μήνυμα, το Streamlit Cloud δουλεύει!")

user_name = st.text_input("Πώς σε λένε;")

if user_name:
    st.success(f"Γεια σου, {user_name}!")