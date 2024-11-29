import streamlit as st

HOME_ADM = -1
HOME_LOG_OFF = 0
HOME_LOG_ON = 1
HOME_FAVORITES = 5
LOG_IN_OR_SIGN_UP = 2
SIGN_UP = 3
LOG_IN = 4

def navigate_to(page):
    st.session_state.current_page = page

def current_page() -> int:
    return st.session_state.current_page