import streamlit as st
import bcrypt

import database.mysql_operations as sql_op
import database.bookmark_io as book_io
from user.user import User


# Gerar hash da senha
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Gera um salt único
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Verificar se a senha inserida corresponde com o hash
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# Salva o usuario no banco de dados
def save_user_in_db(name: str, email: str, password: str):
    query = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)"
    hashed_password = hash_password(password)  

    sql_op.execute_db_query(query, (name, email, hashed_password), "Cadastrado com Sucesso", "Erro ao cadastrar usuario", None)

# Carrega as informacoes essenciais do usuario do banco de dados
def load_user_from_db(email: str):
    query = "SELECT id, nome, senha FROM usuario WHERE email = %s"
    #cursor = st.session_state.connection_censo.cursor()
    #cursor.execute(query, (email,))
    #return cursor.fetchall()
    return sql_op.execute_db_query(query, (email,), "", "Erro ao carregar usuario do Banco de Dados", None)

# Verifica se campos do cadastro, nao sao vazios

def validate(name: str, email: str, password: str) -> bool:
    return bool(name and email and password)



# Abre o forms de registro e faz o cadastro
def register_user() -> bool:

    with st.form("Cadastro"):
        st.title('Cadastro de usuarios')
        name: str = st.text_input('Nome: ')
        email: str = st.text_input('E-mail: ')
        pasword: str = st.text_input('Senha: ', type="password")
        submit: bool = st.form_submit_button("Enviar")

    print(f"submit status: {submit}, name: {name}, email: {email}")

    if submit:

        if validate(name, email, pasword):

            if load_user_from_db(email) == []:
                save_user_in_db(name, email, pasword)
                return True
                # st.session_state.current_page = vp.LOG_IN_OR_SIGN_UP

            else:
                st.warning("Usuario ja cadastrado!")
        else:
            st.warning("Dados invalidos!")
        return False



# Abre o forms de login e o faz
def login_user() -> bool:

    with st.form("Login"):

        st.title('Login do usuario')
        email: str = st.text_input('E-mail: ')
        pasword: str = st.text_input('Senha: ', type="password")
        submit: bool = st.form_submit_button("Enviar")

        print(st.session_state.user)

        if submit and email and pasword:

            rows = load_user_from_db(email)

            if rows != []:

                password_db = rows[0][2]

                if verify_password(pasword, password_db):

                    user = User()

                    user.name = rows[0][1]
                    user.id = rows[0][0]
                    user.email = email

                    user.set_bookmarks(book_io.load_bookmarks_from_db(user.id))

                    st.session_state.user = user

                    #st.session_state.current_page = vp.HOME_LOG_ON

                    st.success("Bem vindo")
                    return True

                else:
                    st.warning("Senha invalida")
            else:
                st.warning("Esse Usuario nao existe")
            return False
        elif submit:
            st.warning("Dados invalidos!")
            return False