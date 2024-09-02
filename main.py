import json
import requests
from datetime import datetime
from datetime import date
import os

try:
    url = 'https://api.cartola.globo.com/atletas/mercado'
    resposta = requests.get(url)

    #utilizei a biblioteca DATATIME e o Módulo OS para Obter informações da data exata que o arquivo "mercado.json" foi atualizado.
    NOME_DO_ARQUIVO = 'mercado.json'
    modificacao = os.path.getmtime(NOME_DO_ARQUIVO)
    ultima_modificacao = datetime.fromtimestamp(modificacao)
    data_atual = date.today()
    data_atual_formatada = data_atual.strftime("%d-%m-%Y")

    # A Biblioteca REQUESTS foi utilizada para obter um arquivo .json diretamente da api do cartola e subscrever ela sobre o arquivo "mercado.json"
    # dessa forma será possível ter informações atualizadas sempre que o código for executado e obter uma resposta HTTP
    if resposta.status_code == 200:
        dados = resposta.json()
        content = json.dumps(dados)
        fd = open(NOME_DO_ARQUIVO, 'w')
        fd.write(content)
        fd.close()

        print(f"ÚLTIMA ATUALIZAÇÃO EM: {data_atual_formatada}")
    else:
        print(f"ÚLTIMA ATUALIZAÇÃO EM: {ultima_modificacao}")

    
    # Abertura, leitura de conteúdo e fechamento do arquivo JSON da Api do cartola
    fd = open (NOME_DO_ARQUIVO,'r', encoding='utf8')
    dados = fd.read()
    fd.close()

    # Transformando o arquivo JSON em Dicionário
    mercado = json.loads(dados)

    # Armazenando Elementos(Chaves) do Dicionário Necessárias para extrair as informações
    clubes = mercado['clubes']
    atletas = mercado['atletas']

    # Criei essa LISTA (lista_de_ids) pois de acordo com a quantidade de vezes em que o id dos times aparecem na lista, 
    # significa a quantidade de jogadores que representou cada time.
    lista_de_ids = []
    jogadores_e_numero_de_jogos = {}
    times_e_quantidade_de_jogadores = {}

    # criei este FOR para iterar sobre a lista de atletas e extrair os ids dos clubes de cada atleta 
    for atleta in atletas:
        lista_de_ids.append(atleta[str('clube_id')])

    for atleta in atletas:
        numero_de_jogos = atleta['jogos_num']
        if numero_de_jogos > 0 and atleta['posicao_id'] != 6:
            jogadores_e_numero_de_jogos [atleta['apelido_abreviado']] = numero_de_jogos
            jogadores_e_numero_de_jogos 
    
    jogadores_em_ordem = dict(sorted(jogadores_e_numero_de_jogos.items(), key=lambda item: item[1], reverse=True))

    # este FOR é usado para contar quantas vezes os ids dos clubes aparecem na lista, 
    # assim é possível identificar a >> QUANTIDADE DE JOGADORES QUE CADA TIME USOU NA COMPETIÇÃO <<
    # e adicionar no dicionário
    for i in lista_de_ids:
        repeticoes_do_id = lista_de_ids.count(i)
        i = str(i)
        nome_do_time = clubes[i]['nome']
        times_e_quantidade_de_jogadores [nome_do_time] = repeticoes_do_id

    print("\n>> QUANTIDADE DE JOGADORES USADOS (POR CLUBE) <<\n")

    for time in times_e_quantidade_de_jogadores:
        print(f"- {time}: {times_e_quantidade_de_jogadores[time]} Jogadores")

    print("\n>> TOP 10 JOGADORES COM MAIS PARTIDAS JOGADAS<<\n")
    
    cont = 0
    for jogador in jogadores_em_ordem:
        if cont == 10:
            break
        else:
            print(f'- {jogador}: {jogadores_em_ordem[jogador]}')
            cont += 1

    # para acessar numero de partidas de cada jogador: atletas[0]['jogos_num']

except Exception as e:
    print(f"Um Erro Foi Encontrado: {e}")
