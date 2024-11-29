from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op

query = '''

SELECT 
    e.CO_ENTIDADE AS ID_Escola,
    e.NO_ENTIDADE AS Nome_Escola,
    COUNT(DISTINCT m.CO_PESSOA_FISICA) AS Total_Alunos
FROM 
    escola e
LEFT JOIN 
    turma t ON e.CO_ENTIDADE = t.CO_ENTIDADE
LEFT JOIN 
    matricula m ON t.ID_TURMA = m.ID_TURMA
WHERE
	e.TP_SITUACAO_FUNCIONAMENTO = 1
GROUP BY 
    e.CO_ENTIDADE, e.NO_ENTIDADE
ORDER BY 
    Total_Alunos DESC;

'''

school: DataFrame =  op.load_table_custom(query, ())

st.write(school)