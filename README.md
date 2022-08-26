# Projeto e Construção de Sistemas - CEFET-RJ
Repositório da disciplina de "Projeto e Construção de Sistemas", do CEFET-RJ, através do Projeto 7 - "Ferramenta para identificação de disparidades em compras públicas, com base em Notas de Empenhos emitidas".

<p align="center">
<img src="http://img.shields.io/static/v1?label=REQUERIMENTS_TXT&message=CONCLUIDO&color=green&style=for-the-badge"/>
<img src="http://img.shields.io/static/v1?label=SELENIUM&message=CONCLUIDO&color=green&style=for-the-badge"/>
<img src="http://img.shields.io/static/v1?label=DOCKER&message=EM%20DESENVOLVIMENTO&color=yellow&style=for-the-badge"/>
</p>

Grupo 3 (composto por):

- BRUNO FERRARI SENHORA

- IAN ALEXANDER ZAHNER MCINTOSH

- PAULUS JOSEPHUS DE ALMEIDA BARBOSA E DACO

:open_file_folder: 

![Imagem do Projeto SNEMP](https://github.com/paulusdaco/cefet-proj-constr-sistemas-Snemp-Projeto7/blob/main/docs/99%20_%20GENERALIDADES/simbolo_SNEmp.png)


# :hammer: Instalação da ferramenta (caso deseja instalar o repositório do GIT)
- Instale o Python em sua máquina:
    - Entre no site do python: 
    ```
    https://www.python.org/downloads/
    ```
    - Baixe o arquivo do python e execute o instalador.
    - Caso esteja utilizando o VS Code, além dos passos acima, faça o download da extensão do Python, no próprio VSCode.
- Instale as bibliotecas requeridas:
    - Basta executar a linha de comando abaixo no diretório 'SNEMP'.
    ```
    pip install -r requirements.txt
    ```

# Como rodar o aplicativo web
- Abra um terminal do VS-Code, exatamente no diretório 'SNEMP';
- Digite:
```
python app.py
```
- Entre no site abaixo:
```
http://localhost/5000
```

# Como utilizar o aplicativo web
- Selecione um arquivo do tipo '.csv', contendo dados orçamentários de uso pelo TCE-RJ, de sua máquina.
- Um arquivo csv para teste foi disponibilizado em duas pastas, na dataset contida dentro da pasta docs e na pasta csv dentro da pasta static da pasta SNEMP.
- Extraia o arquivo rar e faça o upload desse arquivo csv no site.
- Clique no botão "Submit"
- Após ser redirecionado para outra página, basta pesquisar no campo de input o tipo de produto que quer, lembrando que a busca é feita na coluna ElemDespesaTCE e os valores mostrados são correspondentes a coluna de Vlr_Pago.( Importante realizar a pesquisa em CapsLock )Exemplo de busca: MATERIAL DE CONSUMO.

# Arquivo 'requirements.txt'
- [Arquivo 'requirements.txt'](https://github.com/paulusdaco/cefet-proj-constr-sistemas-Snemp-Projeto7/blob/main/SNEMP/requirements.txt)


# Procedimento para instalação e configuração da aplicação via docker
- Baixe o Docker em sua máquina pelo site seguindo o tutorial disponibilizado pelo mesmo:
```
https://www.docker.com/
```
- Faça o pull do container na sua máquina com o seguinte comando:
```
Ainda está em upload pelo arquivo ser muito grande
```
- Para saber o nome do docker execute o comando:
```
docker images
```
- Em sequência execute o comando abaixo:
```
docker run -it -d -p 5000:5000 "nome do docker"  # <-- Tire as aspas
```

# Testes funcionais com Selenium
- [Teste no Selenium](https://github.com/paulusdaco/cefet-proj-constr-sistemas-Snemp-Projeto7/blob/main/SNEMP/testeSelenium.py)

# ✔️ Técnicas e tecnologias utilizadas

- ``Python``
- ``Visual Studio Code``
- ``Flask``
- ``sqlite3``
- ``doker``
- ``wsl2``

# 📁 Acesso ao projeto
Você pode acessar os arquivos do projeto, clicando [aqui](https://github.com/paulusdaco/cefet-proj-constr-sistemas-Snemp-Projeto7/tree/main/SNEMP).

# Alunos

| [<img src="https://avatars.githubusercontent.com/u/67447500?v=4" width=115><br><sub>Bruno Ferrari</sub>](https://github.com/brsferrari) |  [<img src="https://avatars.githubusercontent.com/u/61014227?v=4" width=115><br><sub>Ian McIntosh</sub>](https://github.com/Crian53) |  [<img src="https://avatars.githubusercontent.com/u/31428022?v=4" width=115><br><sub>Paulus Daco</sub>](https://github.com/paulusdaco) |
| :---: | :---: | :---: |
