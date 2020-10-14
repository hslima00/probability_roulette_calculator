import random
import xlsxwriter
import csv
from collections import Counter
import time
import sys

num_apostado = int(input("Insira um numero de 0 a 36: "))
simul = int(input("Nr de simul: "))
""" read excel"""
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()

"""read .csv"""
dict_bets = {}
bet_data = r'bet_data.csv'
# let o ficheiro e meter as merdas todas num dict
with open(bet_data, 'r') as csv_file:
    # open file with mode read
    csv_reader = csv.reader(csv_file)
    # loop the file
    for line in csv_reader:
        # try:except in case of broken links dont stopping the scrip
        n_jogada = line[0]
        bet = line[1]
        dict_bets.update({n_jogada: bet})
        # nº de jogada / bet
"""---Instaciação de Lists----"""
jogadas = []
aposta_f = []
v_ganho = []
t_gasto = []
lucro = []
n_apostado = []
headers = ['Jogadas', 'Bet', 'V. Ganho', 'T. Gasto', 'Lucro', 'N Apostado']


def leastFrequent(arr, n):

    # Sort the array
    arr.sort()

    # find the min frequency using
    # linear traversal
    min_count = n + 1
    res = -1
    curr_count = 1
    for i in range(1, n):
        if (arr[i] == arr[i - 1]):
            curr_count = curr_count + 1
        else:
            if (curr_count < min_count):
                min_count = curr_count
                res = arr[i - 1]

            curr_count = 1

    # If last element is least frequent
    if (curr_count < min_count):
        min_count = curr_count
        res = arr[n - 1]

    return res


def update_progress(progress):
    barLength = 40  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format(
        "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


dict_total = []
"""calculadora"""
i = 0
while i != simul:

    nr_calhado = 40  # pq é impossivel calhar um numero acima de 36
    counter = 1
    valor_gasto = 0
    dict_freq = []

    while num_apostado != nr_calhado:

        nr_calhado = random.randint(0, 36)
        dict_freq.append(nr_calhado)
        bet = float(dict_bets.get(str(counter)))
        if counter >= 200:
            counter = 200
        else:
            counter = counter + 1

        valor_gasto = valor_gasto + bet
    dict_total.extend(dict_freq)
    progress = i/simul
    update_progress(progress)
    num_apostado = leastFrequent(dict_total, len(dict_total))

    if len(dict_total) > 10000:
        dict_total = []

    jogadas.append(str(counter-1))
    aposta_f.append(str(bet))
    v_ganho.append(str(bet*36))
    t_gasto.append(str(valor_gasto))
    lucro.append(str(bet*36-valor_gasto))
    n_apostado.append(str(num_apostado))
    i = i + 1
""" Criar a primera linha com os titulos"""
p = 0
for item in headers:
    row = 0
    column = p
    worksheet.write(row, column, item)
    p = p + 1
"""meter as merdas todas na tabela"""
p = 0
for item in jogadas:
    row = p + 1
    column = 0
    worksheet.write(row, column, float(item))
    p = p + 1
p = 0
for item in aposta_f:
    row = p + 1
    column = 1
    worksheet.write(row, column, float(item))
    p = p + 1
p = 0
for item in v_ganho:
    row = p + 1
    column = 2
    worksheet.write(row, column, float(item))
    p = p + 1
p = 0
for item in t_gasto:
    row = p + 1
    column = 3
    worksheet.write(row, column, float(item))
    p = p + 1
p = 0
for item in lucro:
    row = p + 1
    column = 4
    worksheet.write(row, column, float(item))
    p = p + 1
p = 0
for item in n_apostado:
    row = p + 1
    column = 5
    worksheet.write(row, column, float(item))
    p = p + 1
workbook.close()
