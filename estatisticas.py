#!/usr/local/bin/python
# coding: utf-8
"""
Script que mostra informações com base nos jogos antetiores da Mega-Sena
"""

import numpy as np
from decimal import Decimal
from collections import OrderedDict
from html_table_parser.parser_functions import extract_tables, make2d


def show_statistics():
    """ Mostra na tela informações sobre os jogos anteriores """
    print('Analisando...')

    numbers = {}
    winners = []
    prizes = []

    # Lendo dados do arquivo HTML...
    with open('data/d_megasc.htm') as file:
        tables = extract_tables(file.read())
        data = make2d(tables[0])[1:]
        for line in data:
            # Soma ocorrência de cada número:
            for num in range(2, 8):
                num = line[num]
                if num not in numbers:
                    numbers[num] = 0
                numbers[num] += 1

            # Quantidade de ganhadores
            winners_qty = int(line[9])
            winners.append(winners_qty)

            # Total do prêmio
            prize_value = line[12].replace('.', '').replace(',', '.')
            prize_total = Decimal(prize_value) * Decimal(winners_qty)
            prizes.append(prize_total)

    # Ordena os números sorteados por ocorrência
    sorted_numbers = OrderedDict(sorted(numbers.items(), key=lambda x: x[1], reverse=True))
    listed_numbers = [n for n in sorted_numbers.keys()]
    more_frequent_numbers = listed_numbers[:10]
    less_frequent_numbers = listed_numbers[-10:]
    less_frequent_numbers.reverse()

    print('\nConcursos de %s até %s:' % (data[0][1], data[-1][1]))
    print('    Concursos realizados: %s\n' % format_number(len(data)))

    print('    Total de ganhadores: %s' % format_number(int(np.sum(winners))))
    print('    Média de ganhadores por concurso: %s\n' % format_number(float(np.mean(winners))))

    print('    Total em prêmios concedidos: R$ %s' % format_number(int(np.sum(prizes))))
    print('    Média de prêmio por concurso: R$ %s\n' % format_number(int(np.mean(prizes))))

    print('    Os 10 números mais frequêntes: %s' % ', '.join(more_frequent_numbers))
    print('    Os 10 números menos frequêntes: %s' % ', '.join(less_frequent_numbers))


def format_number(number):
    """ Formata número para BRL """
    if type(number) == int:
        return '{:0,}'.format(number).replace(',', '.')
    return '{0:.2f}'.format(number).replace('.', ',')


if __name__ == '__main__':
    show_statistics()
