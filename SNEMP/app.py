from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import re
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_pdf import PdfPages
import math
from math import sqrt
import numpy as np
from scipy import spatial
import seaborn as sns
import unicodedata

app = Flask(__name__, template_folder="templates")
ALLOWED_EXTENSIONS = {"csv"}
app.config['UPLOAD_FOLDER'] = "static/Excel"

app.secret_key = "123"

pd.options.mode.chained_assignment = None

###--------------- Remoção da Acentuação ---------------###

def acentoff(texto):
  return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def acentoff2(words):
    wordlist = []
    for word in words.split():
        new = acentoff(word)
        new = re.sub(r'[^\w\a]',"", new)
        if new != "":
            wordlist.append(new.upper())
    return wordlist

def process(words):
    words = acentoff2(words)
    return ' '.join(words)

###-----------------------------------------------------###

def db_connection():
    con = None
    try:
        con = sqlite3.connect('MyData.db')
    except sqlite3.error as e:
        print(e)
    return con

@app.route("/", methods=["GET", "POST"])
def index():
    con = db_connection()
    if request.method == 'GET':
        return render_template("snemp.html")

    if request.method == "POST":
        csvfile = request.files['csvfile']
        tce = pd.read_csv(csvfile, encoding='latin-1', dtype = {"CNPJRaiz": "string", "CPFCNPJCredor": "string", "ElemDespesaTCE": "string", "IdContrato": "string", "CNPJRaiz": "string","CNPJRaiz": "string","CNPJRaiz": "string","CNPJRaiz": "string"})
        
        # TRATAMENTO DOS DADOS
        # Drop da ultima linha por ser um totalizador
        tce = tce.drop(tce.tail(1).index)

        # Convertendo a formatação da DtEmpenho
        tce.DtEmpenho = pd.to_datetime(tce.DtEmpenho, format="%Y-%m-%d")

        # Analisando os dados e atribuindo a melhor formatação dada pelo Pandas de forma automática
        tce = tce.convert_dtypes() ### RESOLVER PROBLEMA DE DTYPE DIFERENTE NA MESMA COLUNA ###
    
        # Considerando que 79% dos registros não possui informação de 'IdUnidOrcamentaria' criaremos dataset sem essa série
        if 'IdUnidOrcamentaria' in tce.columns:
            tce_clean = tce.drop('IdUnidOrcamentaria', axis=1)
        else:
            tce_clean = tce

        # Corrigindo a formatação das colunas de valores
        for col in tce_clean.filter(like='Vlr').columns: #filtrando/restringindo a execução
            tce_clean[col] = tce_clean[col].astype(str) #convertendo em string obs.: já consta naturalmente como string
            tce_clean[col] = tce_clean[col].astype(str).str.replace(',','.') #substituindo virgulas por pontos
            tce_clean[col] = pd.to_numeric(tce_clean[col], errors='coerce') #convertendo em numérico
            tce_clean[col] = tce_clean[col].replace(np.nan, 0) #substituindo valores ausentes por zero
            tce_clean[col] = tce_clean[col].round(2) #arredondando para 2 casas decimais
            tce_clean[col] = tce_clean[col].abs() #tornando os valores absolutos

        # Dentre as demais séries observamos que 20,3% sequer apresenta o número da licitação e concomitância com outras séries importantes. Essa condição nos induz a descartar tais registros.
        # Nosso objetivo é obter um dataset mais conciso para aplicação de modelos e servir de aprendizado.
        # Eliminando entradas que possuem valores ausentes para:
        tce_clean = tce_clean.dropna(subset=['NrLicitacao'], axis=0)
        tce_clean = tce_clean.dropna(subset=['ElemDespesaTCE'], axis=0)
        tce_clean = tce_clean.dropna(subset=['ElemDespesaUG'], axis=0)
        tce_clean = tce_clean.dropna(subset=['Historico'], axis=0)

        # Eliminando do dataset os registros com valores acima de 1 bilhão
        bindex = [] #criando lista que receberá os index com valores superiores a 1 bilhão
        for col in tce_clean.filter(like='Vlr').columns: #filtrando/restringindo a execução
            mask = tce_clean[col] >= 1000000000 #criando o subset com valor superior para cada coluna
            bilion = tce_clean[mask] #criando o dataset para o subset
            bindex.extend(bilion.index.tolist()) #criando uma lista com os index da coluna filtrada e adicionando na lista
        bindex = list(dict.fromkeys(bindex)) #eliminando duplicidades da lista
        bindex.sort() #ordenando a lista
        for row in bindex:
            tce_clean = tce_clean.drop(row)

        # Remoção de algumas colunas a mais no csv
        if 'ElementoPuro' in tce_clean.columns:
            tce_clean = tce_clean.drop('ElementoPuro', axis=1)

        if 'FuncaoPura' in tce_clean.columns:
            tce_clean = tce_clean.drop('FuncaoPura', axis=1)

        if 'SubFuncaoPura' in tce_clean.columns:
            tce_clean = tce_clean.drop('SubFuncaoPura', axis=1)

        # Preparando a base de treinamento
        df_mask = tce_clean['IdContrato']!='0'
        tce_train = tce_clean[df_mask]

        #retirando acentos e tornando maiúsculas
        for col in tce_train.select_dtypes('string').columns: #filtrando/restringindo a execução
            tce_train[col] = tce_train.apply(lambda row: process(row[col]), axis=1)

        ###----------------------------------------------------------###

        tce_clean.to_sql(name = 'data', con = con, if_exists = 'replace', index = False)
        tce_train.to_sql(name = 'train', con = con, if_exists = 'replace', index = False)
        
        return render_template("bd.html", tam = 0)

@app.route('/bd', methods=["GET", "POST"])
def bd():
    con = db_connection()
    cur = con.cursor()   
    if request.form['searchbar1'] != None:
        if request.method == "POST":
            searchitem =  str(request.form['searchbar1'])
            tce_train_df = pd.read_sql('SELECT * FROM train', con)
            mask = tce_train_df['ElemDespesaTCE'] == searchitem
            tce_train_filter = tce_train_df[mask]
            
            # Média, Moda e etc
            if tce_train_filter.empty:
                mean = 0
                moda = 0
                var = 0
                dvp = 0
                min = 0
                max = 0
                tam = 0
            else:
                mean = round(tce_train_filter['Vlr_Pago'].mean())
                moda = round(tce_train_filter['Vlr_Pago'].mode()[0])
                var = round(tce_train_filter['Vlr_Pago'].var())
                dvp = round(tce_train_filter['Vlr_Pago'].std())
                min = round(tce_train_filter['Vlr_Pago'].min())
                max = round(tce_train_filter['Vlr_Pago'].max())
                tam = len(tce_train_filter)

            return render_template("bd.html", mean = mean, moda = moda, var = var, dvp = dvp, min = min, max = max, tam = tam)
    return render_template("bd.html")
    
if __name__ ==  "__main__":
    app.run(debug=True)