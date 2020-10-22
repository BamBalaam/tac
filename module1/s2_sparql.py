"""Query Wikidata for Belgian monarchs"""
from datetime import datetime as dt
from os import system, name

from SPARQLWrapper import SPARQLWrapper, JSON


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
        print(
            "Voici les Monarques Belges pour lesquels Wikidata a des informations.\n"
            "Choisissez celui pour lequel vous voulez avoir des informations.\n"
        )
        for key, value in choices.items():
            print(f"- {key}: {value}")
        user_choice = input('\nVotre choix: ')
    return user_choice


def query_sparql(sparql, statement):
    sparql.setQuery(statement)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    rows = results['results']['bindings']
    return rows


def get_monarchs(sparql):
    """Retrieve Belgian monarchs from SPARQL"""

    statement = """
        SELECT
          ?item ?itemLabel ?fatherLabel ?motherLabel ?dateBirth ?dateDeath
        WHERE
        {
          ?item wdt:P27 wd:Q31 .
          ?item wdt:P106 wd:Q116 .
          ?item wdt:P22 ?father .
          ?item wdt:P25 ?mother .
          ?item wdt:P569 ?dateBirth .
          OPTIONAL {?item wdt:P570 ?dateDeath .}

          SERVICE wikibase:label {
            bd:serviceParam wikibase:language "fr".
          }
        }
        ORDER BY ?dateBirth
    """
    return query_sparql(sparql, statement)


def get_family(sparql, monarch):
    """Retrieve list of children and mother for Belgian monarchs from SPARQL"""
    monarch_wikidata_id = monarch['item']['value'].rsplit('/', 1)[-1]
    statement = f"""
        SELECT
            ?mother ?motherLabel
            (GROUP_CONCAT(DISTINCT ?childLabel; SEPARATOR="|") AS ?childrenNames)
        WHERE
        {{
          ?child wdt:P22 wd:{monarch_wikidata_id}.
          ?child wdt:P25 ?mother.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr,en".
                                  ?mother rdfs:label ?motherLabel.
                                  ?child  rdfs:label ?childLabel.
                                 }}
        }}
        GROUP BY ?mother ?motherLabel
    """
    return query_sparql(sparql, statement)


def display_monarch_family(family):
    print("Famille:")
    for item in family:
        spouse = item['motherLabel']['value']
        children = item['childrenNames']['value'].split('|')
        print(
            f"\tÉpouse: {spouse}\n"
            f"\tEnfants: {', '.join(children)}\n"
        )


def display_monarch_info(sparql, monarch):
    clear_terminal()

    name = monarch['itemLabel']['value']
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    try:
        birth = dt.strptime(monarch['dateBirth']['value'], date_format)
        birth_day = birth.day
        birth_month = birth.month
        birth_year = birth.year
    except KeyError:
        birth_day, birth_month, birth_year = "???"
    try:
        death = dt.strptime(monarch['dateDeath']['value'], date_format)
        death_day = death.day
        death_month = death.month
        death_year = death.year
    except KeyError:
        death_day, death_month, death_year = "???"

    father = monarch['fatherLabel']['value']
    mother = monarch['motherLabel']['value']

    family = get_family(sparql, monarch)
    print(
        f"\n\nNom: {name}\n"
        f"Date de naissance: {birth_day}/{birth_month}/{birth_year}\n"
        f"Mort: {death_day}/{death_month}/{death_year}\n\n"
        f"Parents: {father} & {mother}"
        "\n\n"
    )
    display_monarch_family(family)


if __name__ == "__main__":
    endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    sparql = SPARQLWrapper(endpoint)
    monarchs = get_monarchs(sparql)
    choices = {
        str(i+1): monarchs[i]['itemLabel']['value']
        for i in range(0, len(monarchs))
    }

    choice = picker(choices)
    display_monarch_info(sparql, monarchs[int(choice)-1])
