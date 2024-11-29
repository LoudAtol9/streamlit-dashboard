from __future__ import annotations
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

import database.mysql_operations as sql_op
import virtualPage.virtual_pages as vp


# Filtrar escolas por município
def listar_escolas_por_cidade(cidade, escolas_df):
    return escolas_df[escolas_df['CO_MUNICIPIO'] == cidade]

# Contar total de alunos, professores e turmas por escola
def contar_por_escola(escolas_df, docentes_df, matriculas_df, turmas_df):
    resumo = escolas_df.copy()
    resumo['TOTAL_ALUNOS'] = resumo['CO_ENTIDADE'].map(
        matriculas_df.groupby('CO_ENTIDADE')['CO_PESSOA_FISICA'].count()
    )
    resumo['TOTAL_PROFESSORES'] = resumo['CO_ENTIDADE'].map(
        docentes_df.groupby('CO_ENTIDADE')['CO_PESSOA_FISICA'].count()
    )
    resumo['TOTAL_TURMAS'] = resumo['CO_ENTIDADE'].map(
        turmas_df.groupby('CO_ENTIDADE')['ID_TURMA'].count()
    )
    return resumo

# Ordenar escolas pelo número de alunos
def ordenar_por_alunos(escolas_df):
    return escolas_df.sort_values(by='TOTAL_ALUNOS', ascending=False)

# Selecionar uma escola e listar suas turmas
def listar_turmas_por_escola(escola_id, turmas_df):
    return turmas_df[turmas_df['CO_ENTIDADE'] == escola_id][['NO_TURMA', 'IN_DISC_CIENCIAS', 'IN_DISC_MATEMATICA']]

# Selecionar professores e alunos de cada escola
def detalhar_pessoas_por_escola(escola_id, docentes_df, matriculas_df):
    professores = docentes_df[docentes_df['CO_ENTIDADE'] == escola_id][['CO_PESSOA_FISICA']]
    alunos = matriculas_df[matriculas_df['CO_ENTIDADE'] == escola_id][['CO_PESSOA_FISICA']]
    return professores, alunos

# Agrupar alunos por nível de ensino
def agrupar_alunos_por_nivel(matriculas_df):
    niveis = matriculas_df.groupby('TP_ETAPA_ENSINO')['ID_MATRICULA'].count()
    return niveis


def show_map():
    df_coords = st.session_state.escolas[['LAT', 'LON']].copy()

    df_coords['LAT'] = df_coords['LAT'].astype(float)
    df_coords['LON'] = df_coords['LON'].astype(float)

    st.map(df_coords)



# Inicializa a variaveis na Session
if 'escolas' not in st.session_state:

    st.session_state.connection_censo = []
    sql_op.connect_with_sql()

    st.session_state.current_page = vp.LOG_IN_OR_SIGN_UP
    st.session_state.aux_var = 0

    #st.session_state.connection_login 
    #st.session_state.cursor_login

    st.session_state.escolas = sql_op.load_table("escola")
    st.session_state.docente = sql_op.load_table("docente")
    st.session_state.turma = sql_op.load_table("turma")
    st.session_state.matricula = sql_op.load_table("matricula")

    st.session_state.filtered_df = pd.DataFrame()

    st.session_state.user = None

#st.write(vp.current_page())

#if st.session_state.user == None: # Não está logado

if st.session_state.user == None:
    pg = st.navigation([st.Page("user/login_page.py", title="Login", default=True),])
elif sql_op.is_admin(): # Logado  
    pg = st.navigation(
    {
      "Conta": [
        st.Page("user/logout_page.py", title="Logout", icon=":material/logout:"),
        st.Page("user/user_info_page.py", title="Informações do Usuário")
      ],
      "Geral": [
        st.Page("general/school_info.py", title="Dashboard", default=True, icon=":material/dashboard:"),
      ],
      "Escolas":[
        st.Page("school/school_filter.py", title="Busca", icon=":material/bookmarks:"),
        st.Page("school/map_page.py", title="Mapa", icon=":material/bookmarks:"),
      ],
      "Buscas":[
          st.Page("search/search_school_by_students.py", title="Mostra escolas por número de alunos"),
          st.Page("search/search_school_by_classes.py", title="Mostra escolas pelas classes"),
          st.Page("search/search_school_by_total.py", title="Mostra escolas pelo total"),
          st.Page("search/search_school_data_list.py", title="Mostra escolas por data list"),
          st.Page("search/search_school_select_pro_stu.py", title="Mostra os professores e estudantes"),
          st.Page("search/search_students_level.py", title="Mostra o nível dos estudantes"),
      ],
      "Administrador":[
        st.Page("admin/admin_page.py", title="Painel de Controle"),
      ]
    }
  )
else: # Logado
    pg = st.navigation(
    {
      "Conta": [
        st.Page("user/logout_page.py", title="Logout", icon=":material/logout:"),
        st.Page("user/user_info_page.py", title="Informações do Usuário")
      ],
      "Geral": [
        st.Page("general/school_info.py", title="Dashboard", default=True, icon=":material/dashboard:"),
      ],
      "Escolas":[
        st.Page("school/school_filter.py", title="Busca", icon=":material/bookmarks:"),
        st.Page("school/map_page.py", title="Mapa", icon=":material/bookmarks:"),
      ],
      "Buscas":[
          st.Page("search/search_school_by_students.py", title="Mostra escolas por número de alunos"),
          st.Page("search/search_school_by_classes.py", title="Mostra escolas pelas classes"),
          st.Page("search/search_school_by_total.py", title="Mostra escolas pelo total"),
          st.Page("search/search_school_data_list.py", title="Mostra escolas por data list"),
          st.Page("search/search_school_select_pro_stu.py", title="Mostra os professores e estudantes"),
          st.Page("search/search_students_level.py", title="Mostra o nível dos estudantes"),
      ],
    }
  )

pg.run()


# main()




    


        