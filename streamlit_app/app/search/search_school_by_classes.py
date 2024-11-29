from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op

query = ''' SELECT
    e.NO_ENTIDADE AS nome_escola,
    t.NO_TURMA AS nome_turma,
    CASE
        WHEN t.IN_DISC_QUIMICA = 1 THEN 'Química'
        WHEN t.IN_DISC_FISICA = 1 THEN 'Física'
        WHEN t.IN_DISC_MATEMATICA = 1 THEN 'Matemática'
        WHEN t.IN_DISC_BIOLOGIA = 1 THEN 'Biologia'
        WHEN t.IN_DISC_CIENCIAS = 1 THEN 'Ciências'
        WHEN t.IN_DISC_LINGUA_PORTUGUESA = 1 THEN 'Língua Portuguesa'
        WHEN t.IN_DISC_LINGUA_INGLES = 1 THEN 'Língua Inglesa'
        WHEN t.IN_DISC_LINGUA_ESPANHOL = 1 THEN 'Língua Espanhola'
        WHEN t.IN_DISC_LINGUA_FRANCES = 1 THEN 'Língua Francesa'
        WHEN t.IN_DISC_LINGUA_OUTRA = 1 THEN 'Outra Língua'
        WHEN t.IN_DISC_LINGUA_INDIGENA = 1 THEN 'Língua Indígena'
        WHEN t.IN_DISC_ARTES = 1 THEN 'Artes'
        WHEN t.IN_DISC_EDUCACAO_FISICA = 1 THEN 'Educação Física'
        WHEN t.IN_DISC_HISTORIA = 1 THEN 'História'
        WHEN t.IN_DISC_GEOGRAFIA = 1 THEN 'Geografia'
        WHEN t.IN_DISC_FILOSOFIA = 1 THEN 'Filosofia'
        WHEN t.IN_DISC_ENSINO_RELIGIOSO = 1 THEN 'Ensino Religioso'
        WHEN t.IN_DISC_ESTUDOS_SOCIAIS = 1 THEN 'Estudos Sociais'
        WHEN t.IN_DISC_SOCIOLOGIA = 1 THEN 'Sociologia'
        WHEN t.IN_DISC_EST_SOCIAIS_SOCIOLOGIA = 1 THEN 'Sociologia/Estudos Sociais'
        WHEN t.IN_DISC_INFORMATICA_COMPUTACAO = 1 THEN 'Informática/Computação'
        WHEN t.IN_DISC_PROFISSIONALIZANTE = 1 THEN 'Profissionalizante'
        WHEN t.IN_DISC_ATENDIMENTO_ESPECIAIS = 1 THEN 'Atendimento Especial'
        WHEN t.IN_DISC_DIVER_SOCIO_CULTURAL = 1 THEN 'Diversidade Socio-Cultural'
        WHEN t.IN_DISC_LIBRAS = 1 THEN 'Libras'
        WHEN t.IN_DISC_PEDAGOGICAS = 1 THEN 'Pedagógicas'
        WHEN t.IN_DISC_OUTRAS = 1 THEN 'Outras Disciplinas'
        ELSE 'Sem Disciplina Definida'
    END AS disciplina
FROM
    escola e
JOIN
    turma t
ON
    e.CO_ENTIDADE = t.CO_ENTIDADE
WHERE
    e.CO_ENTIDADE = %s
ORDER BY
    t.NO_TURMA, disciplina;'''

escolas_dict = dict(zip(st.session_state.escolas['NO_ENTIDADE'], st.session_state.escolas['CO_ENTIDADE']))

escola_nome_to_selectbox = list(escolas_dict.keys())

# Exibe os nomes das escolas no selectbox
escola_selecionada_nome = st.selectbox("Escolha uma escola:", escola_nome_to_selectbox)

school: DataFrame =  op.load_table_custom(query, (escolas_dict[escola_selecionada_nome],))

st.write(school)