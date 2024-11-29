from __future__ import annotations
import streamlit as st
import pandas as pd

# Configurando os elementos interativos para a página principal
st.title("Filtros e Resultados")

# Criar colunas para organizar os filtros
col1, col2 = st.columns(2)

# Dependência administrativa
dep_opcoes = ["Qualquer"] + st.session_state.escolas['TP_DEPENDENCIA'].unique().tolist()
with col1:
    dep = st.selectbox("Dependência administrativa", dep_opcoes)

# Localização
loc_opcoes = ["Qualquer"] + st.session_state.escolas['TP_LOCALIZACAO'].unique().tolist()
with col2:
    loc = st.radio("Localização", loc_opcoes)

# Nome
nom = st.multiselect("Nome", st.session_state.escolas['NO_ENTIDADE'].unique())

# Slider com intervalo
min_val = st.session_state.escolas['NU_COMPUTADOR'].min()
max_val = st.session_state.escolas['NU_COMPUTADOR'].max()
sl = st.slider(
    "Quantidade de Computadores",
    min_val, max_val, (min_val, max_val)  # Seleção inicial: intervalo completo
)


# Botões para aplicar e limpar filtros
col3, col4 = st.columns(2)
with col3:
    filtrar = st.button("Filtrar")
with col4:
    limpar = st.button("Limpar")



# Lógica para aplicar ou limpar filtros
if filtrar:
    st.session_state.filtered_df = st.session_state.escolas[
        ((st.session_state.escolas['TP_DEPENDENCIA'] == dep) | (dep == "Qualquer")) &
        ((st.session_state.escolas['TP_LOCALIZACAO'] == loc) | (loc == "Qualquer")) &
        (st.session_state.escolas['NO_ENTIDADE'].isin(nom if nom else st.session_state.escolas['NO_ENTIDADE'])) &
        (st.session_state.escolas['NU_COMPUTADOR'] >= sl[0]) & (st.session_state.escolas['NU_COMPUTADOR'] <= sl[1])
    ]
elif limpar:
    st.session_state.filtered_df = pd.DataFrame()

# Botão para baixar a tabela
st.download_button(
    label="Baixar Tabela como csv",
    data=st.session_state.escolas.to_csv() if st.session_state.filtered_df.empty else st.session_state.filtered_df.to_csv(),
    file_name="dados.csv",
    mime="text/csv"
)

if st.session_state.filtered_df.empty:
    st.write(st.session_state.escolas)
else:
    st.write(st.session_state.filtered_df)
