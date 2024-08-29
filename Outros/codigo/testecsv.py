def le():
    arq = open('alunos.csv', 'r')
    print(arq)
    dados = arq.readlines()
    saida = {}
    for linha in dados:
        linha[:-1].split(';')
        print(linha[0])
        saida[linha[0]] = linha[1]
    return saida

print(le())

def salva_dados():
    arq = open('dados/matricula.csv', 'a')
    arq.write(f'{matricula};{nome}\n')
    arq.close()

matricula = 1234
def deleta():
    arq = open('dados/matricula.csv', 'r+')
    dados = arq.readlines()
    saida = {}
    for linha in dados:
        lista = linha.split(';')
        if lista[0] != matricula:
            saida += linha
    print(saida)
    arq.write(saida)
