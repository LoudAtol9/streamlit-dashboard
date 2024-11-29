from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op

query = '''

SELECT 
    e.CO_ENTIDADE AS ID_Escola,
    e.NO_ENTIDADE AS Nome_Escola,
    COUNT(DISTINCT m.CO_PESSOA_FISICA) AS Total_Alunos,
    COUNT(DISTINCT d.CO_PESSOA_FISICA) AS Total_Professores,
    COUNT(DISTINCT t.ID_TURMA) AS Total_Turmas
FROM 
    escola e
LEFT JOIN 
    turma t ON e.CO_ENTIDADE = t.CO_ENTIDADE
LEFT JOIN 
    docente d ON t.ID_TURMA = d.ID_TURMA
LEFT JOIN 
    matricula m ON t.ID_TURMA = m.ID_TURMA
WHERE
	e.TP_SITUACAO_FUNCIONAMENTO = 1
GROUP BY 
    e.CO_ENTIDADE, e.NO_ENTIDADE
ORDER BY 
    e.NO_ENTIDADE;

'''

school_data: DataFrame =  op.load_table_custom(query, ())

st.write(school_data)