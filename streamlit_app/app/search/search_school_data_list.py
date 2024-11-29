from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op

query = '''

SELECT 
    NO_ENTIDADE AS Nome_da_Escola,
    CASE 
        WHEN TP_SITUACAO_FUNCIONAMENTO = 1 THEN 'Ativa'
        ELSE 'Inativa'
    END AS Status_de_Funcionamento,
    CO_MUNICIPIO AS Municipio,
    CASE 
        WHEN TP_LOCALIZACAO = 1 THEN 'Urbana'
        WHEN TP_LOCALIZACAO = 2 THEN 'Rural'
        ELSE 'Indefinida'
    END AS Localizacao,
    CASE 
        WHEN TP_DEPENDENCIA = 1 THEN 'Federal'
        WHEN TP_DEPENDENCIA = 2 THEN 'Estadual'
        WHEN TP_DEPENDENCIA = 3 THEN 'Municipal'
        WHEN TP_DEPENDENCIA = 4 THEN 'Privada'
        ELSE 'Indefinida'
    END AS Dependencia,
    CONCAT(
        CASE WHEN IN_COMUM_CRECHE = 1 THEN 'EI, ' ELSE '' END,
        CASE WHEN IN_COMUM_PRE = 1 THEN 'EI, ' ELSE '' END,
        CASE WHEN IN_COMUM_FUND_AI = 1 THEN 'EF1, ' ELSE '' END,
        CASE WHEN IN_COMUM_FUND_AF = 1 THEN 'EF2, ' ELSE '' END,
        CASE WHEN IN_COMUM_MEDIO_MEDIO = 1 THEN 'EM, ' ELSE '' END,
        CASE WHEN IN_COMUM_EJA_FUND = 1 THEN 'EJA, ' ELSE '' END,
        CASE WHEN IN_COMUM_PROF = 1 THEN 'EP, ' ELSE '' END
    ) AS Niveis_Atendidos
FROM escola 
ORDER BY NO_ENTIDADE

'''

school_data_list: DataFrame =  op.load_table_custom(query, ())

st.write(school_data_list)