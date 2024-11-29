import streamlit as st
import virtualPage.virtual_pages as vp


if st.button("Logout"):
    st.session_state.user = None
    vp.navigate_to(vp.LOG_IN_OR_SIGN_UP)
    