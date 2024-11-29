import streamlit as st
import database.mysql_operations as sql_op
import pandas as pd

                                                                

# Salva novo bookmark no banco de dados
def save_bookmark_in_db(school_id: str, user_id: str):
    query = "INSERT INTO usuario_escola_bookmarks (usuario_id, escola_id) VALUES (%s, %s)"
    sql_op.execute_db_query(query, (user_id, school_id), "Bookmark salvo com sucesso!", "Erro ao salvar bookmark", None)

# Salva novo bookmark na seccao e no banco de dados
def save_bookmark(school_id: int):

    # Tem que ver se ja existe
    if school_id in st.session_state.user.bookmarks_id:
        st.warning("Essa escola ja está salva nas favoritas")
    else:
        st.session_state.user.add_bookmark(school_id)
        save_bookmark_in_db(str(school_id), str(st.session_state.user.id))

# Apaga um bookmark no banco de dados
def delete_bookmark_in_db(school_id: str, user_id: str):
    query = "DELETE FROM usuario_escola_bookmarks WHERE usuario_id = %s AND escola_id = %s"
    sql_op.execute_db_query(query, (user_id, school_id), "Bookmark removido com sucesso!", "Erro ao remover bookmark", None)

def delete_bookmark(school_id: int):
    st.session_state.user.remove_bookmark(school_id)
    delete_bookmark_in_db(str(school_id), str(st.session_state.user.id))

def load_bookmarks_from_db(user_id: str) -> pd.DataFrame | None:

    query = "SELECT escola_id FROM usuario_escola_bookmarks WHERE usuario_id = %s"
    #cursor = st.session_state.connection_censo.cursor()
    #cursor.execute(query, (user_id,))
    #v = cursor.fetchall()
    return sql_op.load_table_custom(query, (user_id,))
