import streamlit as st

st.write(f"O usuario está loggado como {st.session_state.user.email}")
st.write(f"Nome do usuario: {st.session_state.user.name}")

