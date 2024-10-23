# Importações e definições de variáveis
import serial
import re
from datetime import datetime
import sqlite3
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import sys

def can_convert_to_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
def sao_numericos(dados):
    return all(tentar_converter_para_numerico(item) is not None for item in dados)

def tentar_converter_para_numerico(valor):
    try:
        return int(valor)
    except ValueError:
        try:
            return float(valor)
        except ValueError:
            return None


def registro(DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta, BombaBaixa, BombaAlta):
    global c
    try:
        # Executando a inserção dos valores na tabela estufa
        c.execute('''INSERT INTO estufa 
                    (DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta, BombaBaixa, BombaAlta)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta, BombaBaixa, BombaAlta))
        sleep(3)
    except sqlite3.Error as e:
        print("Erro ao inserir dados no banco de dados:", str(e))


def substituir_nao_int_por_ultimo_int(lista):
    ultimo_int = None  # Variável para armazenar o último valor int válido

    # Iterar sobre a lista original
    for i in range(len(lista)):
        if isinstance(lista[i], int):
            # Atualizar o último valor int válido
            ultimo_int = lista[i]
        else:
            # Substituir valores não int pelo último valor int válido encontrado
            if ultimo_int is not None:
                lista[i] = ultimo_int

    return lista

def plot_estufa(n):
    # Leitura dos parâmetros do arquivo
    with open("./static/parametros.txt", "r") as arquivo:
        parametros = arquivo.read()
    tpm, umm = parametros.split()[1], parametros.split()[2]
    print(tpm, umm)
    #tpm, umm = 30, 60
    # Conexão com o banco de dados SQLite e obtenção dos dados da tabela estufa
    connie = sqlite3.connect(db_locate)
    c = connie.cursor()
    c.execute("SELECT * FROM estufa")
    dados = c.fetchall()

    # Criação do DataFrame a partir dos dados do banco
    columns_info = c.execute("PRAGMA table_info(estufa)").fetchall()
    column_names = [c[1] for c in columns_info]
    df = pd.DataFrame(dados, columns=column_names).set_index('ID')
    df['DataHora'] = pd.to_datetime(df['DataHora'])

    # Verifique se cada valor pode ser convertido para float
    mask = df[df.columns[1:]].apply(lambda col: col.apply(can_convert_to_float))
    # Identifique linhas onde todos os valores podem ser convertidos
    valid_rows = mask.all(axis=1)
    # Filtre o DataFrame para manter apenas as linhas válidas
    df = df[valid_rows]

    #print(df)
    # Preparação dos dados para plotagem
    Amostra = range(len(df['DataHora']))
    Periodo = df['Periodo'].to_numpy()
    Serial = df['Serial'].to_numpy()
    Painel = df['Painel'].to_numpy()
    Exaustor = df['Exaustor'].to_numpy()
    TempAmb = df['TempAmb'].to_numpy()
    UmidAmb = df['UmidAmb'].to_numpy()
    TempSolo = df['TempSolo'].to_numpy()
    UmidSolo = df['UmidSolo'].to_numpy()
    BoiaBaixa = df['BoiaBaixa'].to_numpy()
    BoiaAlta = df['BoiaAlta'].to_numpy()
    BombaBaixa = df['BombaBaixa'].to_numpy()
    BombaAlta = df['BombaAlta'].to_numpy()
# Configuração da figura e subplots

    fig, axs = plt.subplots(2, 1, figsize=(15, 10))

    # Plotagem do primeiro gráfico com temperatura e umidade
    axs[0].plot(Amostra, TempAmb, color='blue', label='TempAb')
    axs[0].plot(Amostra, UmidAmb, color='green', label='UmidAb')
    axs[0].plot(Amostra, TempSolo, color='magenta', label='TempSl')
    axs[0].plot(Amostra, UmidSolo, color='black', label='UmidSl')
    axs[0].plot(Amostra, 100*BoiaBaixa, color='magenta', linestyle='--', label='boiaB')
    axs[0].plot(Amostra, 100*BoiaAlta, color='black', linestyle='--', label='boiaA')

    axs[0].set_xlabel('Amostras')
    axs[0].set_ylabel('Valores')

    # Cálculo dos valores de temperatura, umidade e umidade do solo
    tempo_atual = datetime.now()


    axs[0].set_title(f'Imagem: {n}, Tempo: {str(tempo_atual)[:-10]}, TempAmb: {TempAmb[-1]}°C, UmidAmb: {UmidAmb[-1]}%, TempSolo: {TempSolo[-1]}°C, UmidSolo: {UmidSolo[-1]}%, BoiaBaixa: {BoiaBaixa[-1]}, BoiaAlta: {BoiaAlta[-1]}')
    axs[0].legend(loc='upper left')
    axs[0].grid()

    # Plotagem do segundo gráfico com dados do painel e exaustor
    axs[1].plot(Amostra, Painel+2.2, label='Painel')
    axs[1].plot(Amostra, Exaustor+1.1, label='Exaustor')

    axs[1].plot(Amostra, BombaBaixa, color='magenta', linestyle='--', label='bombaB')
    axs[1].plot(Amostra, BombaAlta, color='black', linestyle='--', label='bombaA')

    axs[1].set_xlabel('Amostras')
    axs[1].set_ylabel('Valores')
    axs[1].set_title(f'Imagem: {n}, Painel: {Painel[-1]}, Exaustor: {Exaustor[-1]}, BombaBaixa: {BombaBaixa[-1]}, BombaAlta: {BombaAlta[-1]}')

   #axs[1].set_title(f'Gráfico do Painel ({str(periodo[-1])}) e Exaustor por Tempo - {str(last_row["data_hora"])[:19]}')
    axs[1].legend(loc='upper left')
    axs[1].grid()

    # Ajuste do espaçamento entre os subplots
    plt.tight_layout()

    # Salvando o gráfico como imagem e fechando a figura
    plt.savefig("./static/pics/plot.png")
    plt.close()



# Defina a porta serial correta do seu Arduino
def serialArduino():
    arduino = None
    porta_serial = '/dev/ttyACM0'  # Primeira tentativa

    try:
        # Tenta conectar à primeira porta
        arduino = serial.Serial(porta_serial, baudrate=9600, timeout=10, dsrdtr= False)
        arduino.dtr = False
        time.sleep(5)  # Aguarda a conexão
        print(f"Conexão com o Arduino estabelecida! Porta serial: {porta_serial}")
    except serial.SerialException as e:
        if arduino and arduino.is_open:
            arduino.close()
            print("Conexão anterior encerrada.")
        print(f"Erro ao conectar ao Arduino em {porta_serial}: {str(e)}")
        time.sleep(5)

        # Verifica se já existe uma conexão aberta e fecha
        if arduino and arduino.is_open:
            arduino.close()
            print("Conexão anterior encerrada.")

        # Tenta conectar à segunda porta
        porta_serial = '/dev/ttyACM1'
        try:
            arduino = serial.Serial(porta_serial, baudrate=9600, timeout=10, dsrdtr= False)
            arduino.dtr = False
            time.sleep(5)  # Aguarda a conexão
            print(f"Conexão com o Arduino estabelecida! Porta serial: {porta_serial}")
        except serial.SerialException as e:
            if arduino and arduino.is_open:
                arduino.close()
                print("Conexão anterior encerrada.")

            print(f"Erro ao conectar ao Arduino em {porta_serial}: {str(e)}")
            time.sleep(5)

    return arduino


arduino = serialArduino()
print(arduino)

# Conexão com o banco de dados SQLite
db_locate = 'greenSe.db'
connie = sqlite3.connect(db_locate)
c = connie.cursor()

# Variáveis para armazenar os últimos dados registrados
ultimos_dados = None

# Padrao e variáveis de controle
padrao = r'\b\d{1,2}:\d{2}:\d{2} \d{2}/\d{2}/\d{4}\b'


# Loop principal
dados_anteriores = {
    "Periodo": None,
    "Serial": None,
    "Painel": None,
    "Exaustor": None,
    "TempAmb": None,
    "UmidAmb": None,
    "TempSolo": None,
    "UmidSolo": None,
    "BoiaBaixa": None,
    "BoiaAlta": None,
    "BombaBaixa": None,
    "BombaAlta": None,
}

def main(n, ultimos_dados, padrao, intervalo_commit, contador_commit):
    # Abrir o arquivo com codificação correta
    try:
        with open("./static/parametros.txt", "r", encoding='utf-8') as arquivo:
            parametros = arquivo.read()
    except UnicodeDecodeError:
        print("Erro ao ler o arquivo com codificação UTF-8. Verifique a codificação do arquivo.")
    except Exception as e:
        print("Erro ao abrir o arquivo:", str(e))

    sleep(3)

    try:
        # Lê da porta serial e decodifica com tratamento de erros
        val = arduino.readline().decode('utf-8', errors='replace')

        if (len(val.split()) == 29) and (val != ''):
            res = val.replace('°C', '').replace('%', '').split(',')
            Valores = ''.join(res).split()
            DataHora = Valores[1] + ' ' + Valores[0]
            try:
                Periodo = Valores[6]
                Serial = Valores[8]
                Painel = Valores[10]
                Exaustor = Valores[12]
                TempAmb = Valores[14]
                UmidAmb = Valores[16]
                TempSolo = Valores[18]
                UmidSolo = Valores[20]
                BoiaBaixa = Valores[22]
                BoiaAlta = Valores[24]
                BombaBaixa = Valores[26]
                BombaAlta = Valores[28]

                dados_anteriores["Periodo"] = Periodo
                dados_anteriores["Serial"] = Serial
                dados_anteriores["Painel"] = Painel
                dados_anteriores["Exaustor"] = Exaustor
                dados_anteriores["TempAmb"] = TempAmb
                dados_anteriores["UmidAmb"] = UmidAmb
                dados_anteriores["TempSolo"] = TempSolo
                dados_anteriores["UmidSolo"] = UmidSolo
                dados_anteriores["BoiaBaixa"] = BoiaBaixa
                dados_anteriores["BoiaAlta"] = BoiaAlta
                dados_anteriores["BombaBaixa"] = BombaBaixa
                dados_anteriores["BombaAlta"] = BombaAlta

            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                print("Mantendo os valores anteriores.")
                Periodo = dados_anteriores["Periodo"]
                Serial = dados_anteriores["Serial"]
                Painel = dados_anteriores["Painel"]
                Exaustor = dados_anteriores["Exaustor"]
                TempAmb = dados_anteriores["TempAmb"]
                UmidAmb = dados_anteriores["UmidAmb"]
                TempSolo = dados_anteriores["TempSolo"]
                UmidSolo = dados_anteriores["UmidSolo"]
                BoiaBaixa = dados_anteriores["BoiaBaixa"]
                BoiaAlta =  dados_anteriores["BoiaAlta"]
                BombaBaixa =  dados_anteriores["BombaBaixa"]
                BombaAlta =  dados_anteriores["BombaAlta"]

            dados_atuais = (
            Periodo, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta, BombaBaixa, BombaAlta)

            if sao_numericos(dados_atuais): #True:  # dados_atuais != ultimos_dados:
                print('DataHora: ', DataHora, ', Periodo: ', Periodo, ', Painel: ', Painel, ', Exaustor: ', Exaustor,
                      ', TempAmb: ', TempAmb, ', UmidAmb: ', UmidAmb, ', TempSolo: ', TempSolo, ', UmidSolo: ',
                      UmidSolo, ', BoiaBaixa: ', BoiaBaixa, ', BoiaAlta: ', BoiaAlta, ', BombaBaixa: ', BombaBaixa,
                      ', BombaAlta: ', BombaAlta)
                registro(DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa,
                         BoiaAlta, BombaBaixa, BombaAlta)
                ultimos_dados = dados_atuais
                contador_commit += 1

                if contador_commit >= intervalo_commit:
                    n += 1
                    connie.commit()
                    contador_commit = 0
                    print("Fazendo commit()!")
                    try:
                        plot_estufa(n)
                    except Exception as e:
                        print("Erro durante o plot:", str(e))
            else:
                raise ValueError("Erro simulado Elementos Não Númericos")


        return ultimos_dados, contador_commit, n

    except Exception as e:
        print("Erro durante a execução Interna:", str(e))


# Configurações para controle de transações
intervalo_commit = 10  # Número de inserções antes de fazer o commit
contador_commit = 0
n = 0

TENTATIVAS_PATH = "./static/tentativas.txt"
MAX_TENTATIVAS = 50

def ler_tentativas():
    """Lê o número de tentativas do arquivo, ou retorna 0 se o arquivo não existir ou estiver vazio."""
    if os.path.exists(TENTATIVAS_PATH):
        with open(TENTATIVAS_PATH, "r") as arquivo:
            try:
                return int(arquivo.read().strip())
            except ValueError:
                return 0
    return 0

def escrever_tentativas(tentativas):
    """Escreve o número de tentativas no arquivo."""
    with open(TENTATIVAS_PATH, "w") as arquivo:
        arquivo.write(str(tentativas))

#escrever_tentativas(0)
while True:

    hora_inicial = time.time()

    while True:
        tempo_decorrido = (time.time() - hora_inicial) / 3600  # convertendo para horas

        if tempo_decorrido >= 24:
            print("12 horas se passaram. Tomando uma decisão...")
            os.execv(sys.executable, [sys.executable] + sys.argv)

            # Aqui você pode colocar a lógica da sua decisão
            break  # Sai do loop após a decisão

        try:
            ultimos_dados, contador_commit, n =  main(n, ultimos_dados, padrao, intervalo_commit, contador_commit)
            sleep(3)
            #raise ValueError("Erro simulado 1")  # Esta linha é para simulação; remova-a no código final.

        except Exception as e:
            if arduino and arduino.is_open:
                arduino.close()
                print("Conexão anterior encerrada.")
            try:
                print("Erro durante a execução rotina principal:", str(e))
                sleep(3)
                #raise ValueError("Erro simulado 2")  # Esta linha é para simulação; remova-a no código final.

                tentativas = ler_tentativas()

                sleep(3)
                tentativas += 1
                print(tentativas)
                escrever_tentativas(tentativas)

                if tentativas <= MAX_TENTATIVAS:
                    print(f"Reiniciando o script... (Tentativa {tentativas}/{MAX_TENTATIVAS})")
                   # print(contador_commit)
                   # if contador_commit == 4:
                   #     raise ValueError("Erro simulado 1")  # Esta linha é para simulação; remova-a no código final.
                    contador_commit = 0

                    os.execv(sys.executable, [sys.executable] + sys.argv)
                    sleep(3)

                else:
                    break
                #arduino = serialArduino()

            except Exception as e:

                print("Erro durante a reiniciar:", str(e))
                break


connie.close()
