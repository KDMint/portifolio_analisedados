import streamlit as st
from components.navigation import navigation_bar

st.set_page_config(page_title="Portfólio Khadija", page_icon="👩‍💻", layout="wide")

navigation_bar()

# Redirect to home page
st.switch_page("pages/home.py")