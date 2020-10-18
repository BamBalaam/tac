import datetime
import json
from os import system, name
import sys

import requests


def clear_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


def picker(choices):
    user_choice = ''
    while user_choice not in choices.keys():
        clear_terminal()
        for key, value in choices.items():
            print(f"- {key}: {value}")
        user_choice = input('\nVotre choix: ')
    return user_choice


def pretty_print_bourgmestre(item):
    bourgmestre = (
        f"   {item['bourgmestres']} "
        f"({item['date_de_naissance']} - {item['decede']})"
        f"\n      Nomination: {item['arrete_royal_de_nomination']}"
        f"\n      Date d'entrée en fonction: {item['date_d_installation']}"
        f"\n      Date de fin de fonction: {item['fin_de_fonction']}"
    )
    print(bourgmestre)


def pretty_print_bourgmestres_list(data):
    clear_terminal()
    print("Liste des bourgmestres:\n")
    ordered_data = sorted(
        data['records'], key=lambda k: k['fields']['date_d_installation']
    )
    for item in ordered_data:
        fields = item['fields']
        pretty_print_bourgmestre(fields)


def query_bourgmestres():
    menu = {
        '1': 'Liste des bourgmestres entre 1847 et 1978',
    }
    choice = picker(menu)
    if choice == '1':
        query = (
            "fin_de_fonction >= 1847-01-01 AND "
            "date_d_installation <= 1978-12-31"
        )

    osm = "https://opendata.bruxelles.be/api/records/1.0/search/"
    params = {
        'dataset': 'bxl_bourgmestres', 'q': query,
        'format': 'json', 'rows': 100
    }
    resp = requests.get(osm, params)
    data = json.loads(resp.text)

    if choice == '2':
        clear_terminal()
        print('\nAnnée:')
        user_choice = input()

    if data['nhits'] == 0:
        print("Aucun résultat n'a été trouvé")
        sys.exit(0)
    pretty_print_bourgmestres_list(data)


def pretty_print_population_list(data):
    clear_terminal()
    ordered_data = sorted(
        data['records'], key=lambda k: k['fields']['annee']
    )
    print("{:<8} {:<15} {:<8} {:<15}".format(
        'Année', 'Population', 'Année', 'Population')
    )

    for i in range(0, len(ordered_data), 2):
        fields_1 = ordered_data[i]['fields']
        if i+1 < len(ordered_data):
            fields_2 = ordered_data[i+1]['fields']
            print("{:<8} {:<15} {:<8} {:<15}".format(
                fields_1['annee'], fields_1['population'],
                fields_2['annee'], fields_2['population'],
            ))
        else:
            print("{:<8} {:<15}".format(
                fields_1['annee'], fields_1['population'],
            ))


def query_population():
    """ Dataset contient des valeurs de population entre 1921 et 2014 """
    menu = {
        '1': (
            'Population de Bruxelles entre 1847 et 1978 '
            '(pour les années où les données sont accessibles)'
        ),
        '2': (
            'Population de Bruxelles entre deux années choisies '
            '(pour les années où les données sont accessibles)'
        ),
    }
    choice = picker(menu)

    if choice == '1':
        query = 'annee: [1847 TO 1978]'
    elif choice == '2':
        clear_terminal()
        print('Années disponibles - entre 1921 et 2014.')
        year_from = input("Année de départ: ")
        year_to = input("Année de fin: ")
        if int(year_to) < int(year_from):
            print("L'année de fin est antérieure à l'année de départ.")
            sys.exit(1)
        query = f"annee: [{year_from} TO {year_to}]"

    osm = "https://opendata.bruxelles.be/api/records/1.0/search/"
    params = {
        'dataset': 'population-bruxelloise-copie0',
        'q': query,
        'format': 'json',
        'rows': 100,
    }
    resp = requests.get(osm, params)
    data = json.loads(resp.text)

    if data['nhits'] == 0:
        print("\nAucun résultat n'a été trouvé")
        sys.exit(0)

    pretty_print_population_list(data)


if __name__ == "__main__":
    caller = {
        'population': query_population,
        'bourgmestres': query_bourgmestres,
    }

    try:
        task = sys.argv[1]
    except IndexError:
        message = (
            "Pas de tâche choisie, passez une valeur en paramètre. "
            f"Choix possibles: {', '.join(caller.keys())}"
        )
        print(message)
        sys.exit(1)

    if task not in caller.keys():
        message = (
            f"Paramètre incorrect. Choix possibles: {', '.join(caller.keys())}"
        )
        print(message)
        sys.exit(1)

    callback = caller[task]
    callback()
