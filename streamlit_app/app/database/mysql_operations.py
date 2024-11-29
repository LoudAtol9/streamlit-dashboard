import streamlit as st
import mysql.connector
import mysql.connector.cursor
from mysql.connector import Error
import pandas as pd


# Inicia o connector e o cursor para o banco de dados
def connect_with_sql() -> bool:
    
    try:
        st.session_state.connection_censo = mysql.connector.connect(
            host=st.secrets["database"]["host"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            database=st.secrets["database"]["database"],
            port=3306
        )

        if st.session_state.connection_censo.is_connected():

            print("Conexão bem-sucedida!")
            return True
        
    except Error as e:

        st.error(f"Erro ao conectar ao banco: {e}")
        return False


def load_table_custom(query: str, params: tuple) -> pd.DataFrame:
    try:
        cursor = st.session_state.connection_censo.cursor(buffered=True)
        cursor.execute(query, params)
        
        # Obtendo os dados
        v = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # Pega os nomes das colunas
        
        cursor.close()  # Fechando o cursor após a consulta

        # Criando o DataFrame
        df = pd.DataFrame(v, columns=columns)
        return df

    except Exception as e:
        st.error(f"Erro ao carregar a tabela: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


# Carrega uma tabela no formato de DataFrame
def load_table(table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    try:
        cursor = st.session_state.connection_censo.cursor(buffered=True)
        cursor.execute(query)
        
        # Obtendo os dados
        v = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # Pega os nomes das colunas
        
        cursor.close()  # Fechando o cursor após a consulta

        # Criando o DataFrame
        df = pd.DataFrame(v, columns=columns)
        return df

    except Exception as e:
        st.error(f"Erro ao carregar a tabela {table_name}: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


# Roda uma query no banco de dados e retorna uma MATRIZ
# Caso ache apenas um elemento, retorna uma MATRIZ 1x1
# Caso seja uma insercao ele nao retornara nada
def execute_db_query(query: str, params: tuple, success_message: str, error_message: str, columns: list):
    try:
        cursor = st.session_state.connection_censo.cursor(buffered=True)
        cursor.execute(query, params)
        st.session_state.connection_censo.commit()

        # Consome resultados, se disponíveis
        result = None
        if cursor.description:  # Apenas consultas SELECT têm descrição
            result = cursor.fetchall()  # Consome os resultados

            if columns:
                columns = [col[0] for col in cursor.description]
        else:
            # Descartar resultados pendentes (em caso de procedimentos armazenados ou múltiplos conjuntos)
            while cursor.nextset():
                pass

        if success_message:
            st.success(success_message)

        cursor.close()
        return result

    except Exception as e:
        st.error(f"{error_message}: {e}")
        return None




def is_admin() -> bool:

    query = "SELECT administrador FROM usuario WHERE email = %s"
    v = execute_db_query(query, (st.session_state.user.email,),"","",None)

    if v == None:
        return False
    return True