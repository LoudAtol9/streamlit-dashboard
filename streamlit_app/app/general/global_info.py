from __future__ import annotations
import streamlit as st
import pandas as pd

# Configuração da página
st.title("Status Geral dos Dados")


# Realizar os joins usando pandas
escolas_turmas = pd.merge(st.session_state.escolas, st.session_state.turma, on='CO_ENTIDADE', how='left')
escolas_turmas_matriculas = pd.merge(escolas_turmas, st.session_state.matricula, on='ID_TURMA', how='left')

# Contar o número total de alunos únicos por escola
alunos_por_escola = (
    escolas_turmas_matriculas.groupby(['CO_ENTIDADE', 'NO_ENTIDADE'])
    .agg(Total_Alunos=('CO_PESSOA_FISICA', 'nunique'))  # Contar alunos únicos
    .reset_index()
)

# Cálculos gerais
total_escolas = len(alunos_por_escola)
total_alunos = alunos_por_escola['Total_Alunos'].sum()
total_professores = st.session_state.escolas['NU_PROFESSORES'].sum() if 'NU_PROFESSORES' in st.session_state.escolas.columns else "Informação não disponível"

# Estatísticas de computadores
total_computadores = st.session_state.escolas['NU_COMPUTADOR'].sum() if 'NU_COMPUTADOR' in st.session_state.escolas.columns else "Informação não disponível"
media_computadores = (
    st.session_state.escolas['NU_COMPUTADOR'].mean() if 'NU_COMPUTADOR' in st.session_state.escolas.columns else "Informação não disponível"
)

# Exibição dos dados gerais
st.subheader("Resumo Geral")
st.markdown(f"**Total de Escolas:** {total_escolas}")
st.markdown(f"**Total de Alunos:** {total_alunos}")
st.markdown(f"**Total de Professores:** {total_professores}")
st.markdown(f"**Total de Computadores:** {total_computadores}")
st.markdown(f"**Média de Computadores por Escola:** {media_computadores:.2f}" if isinstance(media_computadores, (float, int)) else f"**Média de Computadores por Escola:** {media_computadores}")

# Tabelas adicionais
st.subheader("Distribuição por Dependência Administrativa")
if 'TP_DEPENDENCIA' in st.session_state.escolas.columns:
    dependencias = st.session_state.escolas['TP_DEPENDENCIA'].value_counts()
    st.table(dependencias)
else:
    st.write("Informação sobre dependências administrativas não disponível.")

st.subheader("Distribuição por Localização")
if 'TP_LOCALIZACAO' in st.session_state.escolas.columns:
    localizacoes = st.session_state.escolas['TP_LOCALIZACAO'].value_counts()
    st.table(localizacoes)
else:
    st.write("Informação sobre localizações não disponível.")