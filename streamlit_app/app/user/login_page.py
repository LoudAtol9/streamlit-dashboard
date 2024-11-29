from __future__ import annotations
import streamlit as st


import database.login_io as io

import virtualPage.virtual_pages as vp




    
if vp.current_page() == vp.LOG_IN_OR_SIGN_UP:

    st.title("Pop it - System")
    st.write("Faça Login!")
    st.write("Caso não tenha conta cadastre-se")

    if st.button("Cadastrar"):
        vp.navigate_to(vp.SIGN_UP)

    if st.button("Login"):
        vp.navigate_to(vp.LOG_IN)

elif vp.current_page() == vp.SIGN_UP:

    st.title("Se una aos nossos usuários!")

    if (io.register_user()):
        vp.navigate_to(vp.LOG_IN_OR_SIGN_UP)



elif vp.current_page() == vp.LOG_IN:
    if (io.login_user()):
        vp.navigate_to(vp.HOME_LOG_ON)


elif vp.current_page() == vp.HOME_LOG_ON:
    st.write(f"O usuario está loggado como {st.session_state.user.email}")




