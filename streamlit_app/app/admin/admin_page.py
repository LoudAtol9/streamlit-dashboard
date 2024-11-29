import streamlit as st
import pandas as pd
import database.mysql_operations as op
import database.bookmark_io as b_io

sidebar_options = ["Escolas", "Turmas", "Matriculas", "Docentes", "Usuarios"]
dep = st.sidebar.selectbox("Tabelas", sidebar_options)

table: pd.DataFrame
elem_list: list[str]

school_dict = dict(zip(st.session_state.escolas['NO_ENTIDADE'], st.session_state.escolas['CO_ENTIDADE']))
school_dict_inv = dict(zip(st.session_state.escolas['CO_ENTIDADE'], st.session_state.escolas['NO_ENTIDADE']))


if dep == "Escolas":
    table = st.session_state.escolas
    dict_norm = dict(zip(table['NO_ENTIDADE'], table['CO_ENTIDADE']))
    dict_inv = school_dict_inv

elif dep == "Turmas":
    table = st.session_state.turma
    dict_norm = dict(zip(table['ID_TURMA'], table['ID_TURMA']))
    dict_inv = dict_norm

elif dep == "Matriculas":
    table = st.session_state.matricula
    dict_norm = dict(zip(table['ID_MATRICULA'], table['ID_MATRICULA']))
    dict_inv = dict_norm

elif dep == "Docentes":
    table = st.session_state.docente
    dict_norm = dict(zip(table['CO_PESSOA_FISICA'], table['CO_PESSOA_FISICA']))
    dict_inv = dict_norm

elif dep == "Usuarios":
    table = op.load_table_custom("SELECT id, nome, email, data_criacao, status, administrador FROM usuario", ())
    dict_norm = dict(zip(table['email'], table['id']))
    dict_inv = dict(zip(table['id'], table['email']))

st.write(table)

selectbox_names = list(dict_norm.keys())

selected_name = st.selectbox(f"Escolha um(a) dos/das {dep}", selectbox_names)
selected_id = dict_norm[selected_name]

if dep == "Usuarios":
    bookmarks = op.load_table_custom("SELECT escola_id FROM usuario_escola_bookmarks WHERE usuario_id = %s", (selected_id,))
    st.write("Bookmarks do Usuário:")
    selectbox_names_bookmark = []

    if st.session_state.user.email != selected_name:
        if st.button("Apagar usuário"):
            st.write("Tem Certeza?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sim"):
                    op.execute_db_query("DELETE FROM usuario WHERE email = %s", (selected_name,))

            with col2:
                st.button("Não")  

    for id in bookmarks['escola_id']:
        selectbox_names_bookmark.append(school_dict_inv[id])

    bookmark = st.selectbox("Bookmarks", selectbox_names_bookmark)
    if st.button("Apagar Bookmark"):
        if st.session_state.user.email == selected_name: 
            b_io.delete_bookmark(school_dict[bookmark])
        else:
            b_io.delete_bookmark_in_db(school_dict[bookmark], selected_id)

    

