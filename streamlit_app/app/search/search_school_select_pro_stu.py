from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op

query_aluno = '''

SELECT 
    e.CO_ENTIDADE AS Codigo_Escola,
    e.NO_ENTIDADE AS Nome_Escola,
    'Aluno' AS Tipo_Pessoa,
    m.CO_PESSOA_FISICA AS Codigo_Pessoa
FROM 
    escola e
INNER JOIN 
    matricula m ON e.CO_ENTIDADE = m.CO_ENTIDADE
WHERE 
    e.CO_ENTIDADE = %s
ORDER BY 
Tipo_Pessoa , Codigo_Pessoa;


'''



query_prof = '''

SELECT 
    e.CO_ENTIDADE AS Codigo_Escola,
    e.NO_ENTIDADE AS Nome_Escola,
    'Professor' AS Tipo_Pessoa,
    d.CO_PESSOA_FISICA AS Codigo_Pessoa
FROM 
    escola e
INNER JOIN 
    docente d ON e.CO_ENTIDADE = d.CO_ENTIDADE
WHERE 
    e.CO_ENTIDADE = %s
ORDER BY 
Tipo_Pessoa , Codigo_Pessoa;

'''

escolas_dict = dict(zip(st.session_state.escolas['NO_ENTIDADE'], st.session_state.escolas['CO_ENTIDADE']))

escola_nome_to_selectbox = list(escolas_dict.keys())

# Exibe os nomes das escolas no selectbox
escola_selecionada_nome = st.selectbox("Escolha uma escola:", escola_nome_to_selectbox)

student: DataFrame =  op.load_table_custom(query_aluno, (escolas_dict[escola_selecionada_nome],))
professor: DataFrame = op.load_table_custom(query_prof, (escolas_dict[escola_selecionada_nome],))

st.write(student)
st.write(professor)