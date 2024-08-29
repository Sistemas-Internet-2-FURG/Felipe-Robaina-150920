from flask import Flask,request,render_template
#from markupsafe import escape
#import urllib.request, json 

import csv

app = Flask(__name__)
def le_arquivo():
	arq = open('alunos.csv', 'r')
	dados = arq.readlines()
	saida = {}
	print(dados)
	for linha in dados:
		partes = linha.split(';')
		saida[partes[0]] = partes[1]
	return saida

#chamada = {12:'Joao'}
chamada = le_arquivo()

@app.route("/")
def alo_mundo():
	nome = "João"
	teste = ['a','b','c']
	return render_template('index.html',nome=nome,teste=teste)

@app.route("/cumprimenta/<nome>")
def diz_oi(nome):
	return("oi, " + nome)

@app.route("/deleta/<matricula>")
def apagar(matricula):
	arq = open('alunos.csv', 'r+')
	dados = arq.readlines()
	saida = {}
	for linha in dados:
		lista = linha.split(';')
		if lista[0] != matricula:
			saida[lista[0]] = lista[1]
	arq.write(str(saida))
	return 'done'

@app.route("/variaveis", methods=['POST', 'GET'])
def usando_variaveis():
	matricula = request.form.get('nova_matricula')
	aluno = request.form.get('novo_aluno')
	chamada = le_arquivo()
	# print(matricula, aluno)
	if request.method == 'POST' and len(matricula)>0:
		chamada[matricula] = aluno
	
	#arquivo_csv = open('alunos.csv', 'w')
	#escritor = csv.writer(arquivo_csv)
	#escritor.writerow([chamada])
	#arquivo_csv.close()
	return render_template('variaveis.html',chamada=chamada)

@app.route("/sobre")
def sobre():
	saida = "<h1>OIOIOIOIOI</h1><br>" *100
	return(saida)

