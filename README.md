# streamlit-dashboard
 Projeto de criação de um dashboard web usando a biblioteca Streamlit para o Python, a fim de analisar dados do Censo de escolas municipais da cidade de Rio Claro - SP

Como rodar:


Criar pasta .streamlit com o secrets.toml com as informações do banco de dados

MySQL:

(exemplo, crie como quiser)

docker run --name MySQL -e MYSQL_ROOT_PASSWORD=123 -e MYSQL_DATABASE=streamlit_db -p 3306:3306 -v path_to/mysql_docker_volume:/var/lib/mysql-files -d mysql:latest

(entrar via workbench para executar os scripts de inicialização na pasta mysql_docker_volume)

Streamlit:
(na pasta streamlit app)

docker build -t streamlit_dashboard .

docker run --name app -it streamlit_dashboard

Conexão:

docker network create my_network

docker network connect my_network MySQL

docker network connect my_network App


Reinicie os Dockers


Acessar o site:

http://localhost:8501/
