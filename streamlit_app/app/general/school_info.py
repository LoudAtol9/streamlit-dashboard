from __future__ import annotations
import streamlit as st
import pandas as pd

import database.bookmark_io as io
import virtualPage.virtual_pages as vp
import database.join_csv_geo as jcg

# Selecionar uma escola e listar suas turmas
def listar_turmas_por_escola(escola_id, turmas_df):
    return turmas_df[turmas_df['CO_ENTIDADE'] == escola_id][['NO_TURMA', 'IN_DISC_CIENCIAS', 'IN_DISC_MATEMATICA']]

# Selecionar professores e alunos de cada escola
def detalhar_pessoas_por_escola(escola_id, docentes_df, matriculas_df):
    professores = docentes_df[docentes_df['CO_ENTIDADE'] == escola_id][['CO_PESSOA_FISICA']]
    alunos = matriculas_df[matriculas_df['CO_ENTIDADE'] == escola_id][['CO_PESSOA_FISICA']]
    return professores, alunos

def print_pos(school_id: int, school_df: pd.DataFrame) -> None:
    df_coords = school_df[school_df['CO_ENTIDADE'] == school_id][['LAT', 'LON']]
    df_coords['LAT'] = df_coords['LAT'].astype(float)
    df_coords['LON'] = df_coords['LON'].astype(float)
    st.map(df_coords)

def bookmark_default_page(escola_filtered: pd.DataFrame):

    # Cria um dicionário mapeando os nomes das escolas para os identificadores
    escolas_dict = dict(zip(escola_filtered['NO_ENTIDADE'], escola_filtered['CO_ENTIDADE']))
    escolas_dict_inv = dict(zip(escola_filtered['CO_ENTIDADE'], escola_filtered['NO_ENTIDADE']))

    escola_nome_to_selectbox = list(escolas_dict.keys())

    # Exibe os nomes das escolas no selectbox
    escola_selecionada_nome = st.selectbox("Escolha uma escola:", escola_nome_to_selectbox)

    # Obtém o identificador da escola selecionada
    escola_selecionada_id = escolas_dict[escola_selecionada_nome]

    if not escola_selecionada_id in st.session_state.user.bookmarks_id:
        if st.button("Salvar nas Favoritas"):
            io.save_bookmark(escola_selecionada_id)
    else:
        if st.button("Remover das Favoritas"):
            io.delete_bookmark(escola_selecionada_id)

    if st.button("Ver Favoritas"):
        vp.navigate_to(vp.HOME_FAVORITES)

            
    # Agora use o identificador para buscar informações relacionadas
    turmas_escola = listar_turmas_por_escola(escola_selecionada_id, st.session_state.turma)
    st.write("Turmas da escola:")
    st.write(turmas_escola)

    professores, alunos = detalhar_pessoas_por_escola(escola_selecionada_id, st.session_state.docente, st.session_state.matricula)
    st.write("Professores:")
    st.write(professores)
    st.write("Alunos:")
    st.write(alunos)

    print_pos(escola_selecionada_id, jcg.get_table_map_pos())
    

def bookmark_favorites_page(escola_filtered: pd.DataFrame):

    # Cria um dicionário mapeando os nomes das escolas para os identificadores
    escolas_dict = dict(zip(escola_filtered['NO_ENTIDADE'], escola_filtered['CO_ENTIDADE']))
    escolas_dict_inv = dict(zip(escola_filtered['CO_ENTIDADE'], escola_filtered['NO_ENTIDADE']))

    nome_escola = []

    # Exibe os botões de cada escola favorita
    for id in st.session_state.user.bookmarks_id:
        nome_escola.append(escolas_dict_inv.get(id))

    # Exibe os nomes das escolas no selectbox
    escola_selecionada_nome = st.selectbox("Escolha uma escola:", nome_escola)


    # Obtém o identificador da escola selecionada
    escola_selecionada_id = escolas_dict[escola_selecionada_nome]

    if st.button("Remover das Favoritas"):
        io.delete_bookmark(escola_selecionada_id)
            
    # Agora use o identificador para buscar informações relacionadas
    turmas_escola = listar_turmas_por_escola(escola_selecionada_id, st.session_state.turma)
    st.write("Turmas da escola:")
    st.write(turmas_escola)

    professores, alunos = detalhar_pessoas_por_escola(escola_selecionada_id, st.session_state.docente, st.session_state.matricula)
    st.write("Professores:")
    st.write(professores)
    st.write("Alunos:")
    st.write(alunos)

    print_pos(escola_selecionada_id, jcg.get_table_map_pos())

    
    if st.button("Voltar"):
        vp.navigate_to(vp.HOME_LOG_ON)

# Configurando os elementos interativos para a página principal
st.title("Dashboard")

# Elementos interativos
dep_opcoes = ["Qualquer"] + st.session_state.escolas['TP_DEPENDENCIA'].unique().tolist()
dep = st.sidebar.selectbox("Dependência administrativa", dep_opcoes)

loc_opcoes = ["Qualquer"] + st.session_state.escolas['TP_LOCALIZACAO'].unique().tolist()
loc = st.sidebar.radio("Localização", loc_opcoes)

# Slider com intervalo
min_val = st.session_state.escolas['NU_COMPUTADOR'].min()
max_val = st.session_state.escolas['NU_COMPUTADOR'].max()
sl = st.sidebar.slider(
    "Quantidade de Computadores",
    min_val, max_val, (min_val, max_val)  # Seleção inicial: intervalo completo
)

is_filtered: bool


# Botao para aplicar filtros
if st.sidebar.button("Filtrar"):
    # Aplicar os filtros no DataFrame
    st.session_state.filtered_df = st.session_state.escolas[
        ((st.session_state.escolas['TP_DEPENDENCIA'] == dep) | (dep == "Qualquer")) &
        ((st.session_state.escolas['TP_LOCALIZACAO'] == loc) | (loc == "Qualquer")) &
        (st.session_state.escolas['NU_COMPUTADOR'] >= sl[0]) & (st.session_state.escolas['NU_COMPUTADOR'] <= sl[1])
    ]

# Botao para limpar os filtros
if st.sidebar.button("Limpar"):
    st.session_state.filtered_df = pd.DataFrame()


result_school_df: pd.DataFrame

if st.session_state.filtered_df.size == 0 :
    # Exibir o DataFrame completo antes do filtro
    result_school_df = st.session_state.escolas
else:
    result_school_df = st.session_state.filtered_df

if vp.current_page() == vp.HOME_LOG_ON:
    bookmark_default_page(result_school_df)

elif vp.current_page() == vp.HOME_FAVORITES:
    bookmark_favorites_page(result_school_df)
