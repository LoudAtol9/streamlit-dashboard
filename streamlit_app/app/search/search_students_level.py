from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op

query = '''

SELECT
    CASE
        WHEN e.IN_COMUM_CRECHE = 1 THEN 'CRECHE'
        WHEN e.IN_COMUM_PRE = 1 THEN 'EI'
        WHEN e.IN_COMUM_FUND_AI = 1 THEN 'EFI'
        WHEN e.IN_COMUM_FUND_AF = 1 THEN 'EFII'
        WHEN e.IN_COMUM_MEDIO_MEDIO = 1 THEN 'EM'
        WHEN e.IN_COMUM_EJA_FUND = 1 THEN 'EJA'
        WHEN e.IN_COMUM_PROF = 1 THEN 'EP'
        ELSE 'Outro'
    END AS nivel_ensino,
    COUNT(m.ID_MATRICULA) AS numero_alunos
FROM
    escola e
JOIN
    matricula m ON e.CO_ENTIDADE = m.CO_ENTIDADE
GROUP BY
    nivel_ensino
ORDER BY
    nivel_ensino;'''

students_level = op.load_table_custom(query, ())

st.write(students_level)