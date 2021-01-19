# -*- coding: utf-8 -*-
import urllib.parse
import requests
import pandas as pd

# Plus tard, peuplé la variable names avec une requête SPARQL qui récupère les propriétés prénom des instances got:Personnage
names = {
    'Catelyn': 'Catelyn_Stark',
    'Eddard': 'Eddard_Stark',
    'Sansa': 'Sansa_Stark',
    'Cersei': 'Cersei_Lannister',
    'Robert': 'Robert_Baratheon',
    'Joffrey': 'Joffrey_Lannister'
}

def get_data(line):
    # line = line.decode('utf-8')
    column = line.split(',')
    res = {
        'saison': column[0],
        'numero_global': column[1],
        'numero_episode': column[2],
        'titre': column[3].replace(' ', '_'),
        'directeur': column[4].replace(' ', '_'),
        'scenariste': column[5].replace(' ', '_'),
        'date_diffusion': column[6] + column[7],
        'audience': column[8],
        'duree': column[9],
        'resume': column[10]
    }
    res['scenariste'] = res['scenariste'].replace(b'\xc2\xa0'.decode('utf-8'), "_")
    res['date_diffusion'] = res['date_diffusion'].replace('"', '')
    res['date_diffusion'] = res['date_diffusion'].replace(b'\xc2\xa0'.decode('utf-8'), "_")
    return res


def get_api(method):
    slug = ""
    if method == 'QUERY':
        slug = 'query?query='
    elif method == 'UPDATE':
        slug = 'update?query='
    return 'http://localhost:8080/api/' + slug


def get_headers():
    return {"content-type": "application/x-www-form-urlencoded", "Accept": "application/sparql-result+json"}


def get_prefixe():
    prefixes = 'prefix got: <http://www.got.org/esirem#> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>'
    return prefixes


def parse_query(query):
    query = urllib.parse.unquote(query)
    query = urllib.parse.quote(query, safe="")
    return query


def query_builder_contient(num_global_episode, resume):
    query = ""

    for name in names:
        if resume.find(name) != -1:
            query += " insert data {got:Episode_" + num_global_episode + " got:contient_le_personnage got:" + names[name] + "};" + "\n"

    return query


def filter(dfrow):
    dfrow['Season']               = str(dfrow['Season'])
    dfrow['Episode Number']       = str(dfrow['Episode Number'])
    dfrow['Number in Season']     = str(dfrow['Number in Season'])
    dfrow['Episode Name']         = dfrow['Episode Name'].replace(' ', '_').replace(',', '').replace(b'\xc2\xa0'.decode('utf-8'), "_").replace('\'', '')
    dfrow['Director']             = dfrow['Director'].replace(' ', '_').replace(',', '').replace(b'\xc2\xa0'.decode('utf-8'), "_").replace('&', 'and')
    dfrow['Writer']               = dfrow['Writer'].replace(' ', '_').replace(',', '').replace(b'\xc2\xa0'.decode('utf-8'), "_").replace('&', 'and')
    dfrow['Original Air Date']    = dfrow['Original Air Date'].replace(' ', '_').replace(',', '').replace(b'\xc2\xa0'.decode('utf-8'), "_")
    dfrow['US viewers (million)'] = str(dfrow['US viewers (million)'])
    dfrow['Runtime (mins)']       = str(dfrow['Runtime (mins)'])
    # dfrow[''] = dfrow[''].replace(' ', '_')
    return dfrow


def query_builder(dfrow):
    dfrow = filter(dfrow)

    # Récuperons les prefixes
    query = get_prefixe() + "\n"

    # Create instance of Episode
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " a got:Episode" + "};" + "\n"

    # Saison
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_pour_numéro_de_saison got:Saison_" + dfrow['Season'] + "};" + "\n"

    # Numéro d'épisode global
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_pour_numéro_dépisode_total got:Num_Global_" + dfrow['Episode Number'] + "};" + "\n"

    # Numéro d'épisode de saison
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_pour_numéro_dépisode_de_saison got:Num_Saison_" + dfrow['Number in Season'] + "};" + "\n"

    # Titre
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_un_titre got:" + dfrow['Episode Name'] + "};" + "\n"

    # Directeur
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_un_directeur got:" + dfrow['Director'] + "};" + "\n"

    # Scénariste
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_un_scénariste got:" + dfrow['Writer'] + "};" + "\n"

    # Date de première diffusion
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_une_date_de_première_diffusion got:" + dfrow['Original Air Date'] + "};" + "\n"

    # nb_vues
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_pour_audience_américaine got:" + dfrow['US viewers (million)'] + "mil};" + "\n"

    # durée
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_pour_durée got:" + dfrow['Runtime (mins)'] + "min};" + "\n"

    # résumé
    query += " insert data {got:Episode_" + dfrow['Episode Number'] + " got:a_pour_résumé got:Résumé_" + dfrow['Episode Number'] + "};" + "\n"

    # Généré les liens entre l'épisode et les personnages présent dans son résumé
    query += query_builder_contient(dfrow['Episode Number'], dfrow['IMDB Description'])

    return query


def load_csv(path, nb_line=0):
    with open(path, encoding="utf-8") as file:
        lines = file.readlines()
        if (nb_line != 0):
            return lines[nb_line]
        else:
            return lines
    return false


path = './got_data.csv'
df = pd.read_csv(path)

for index, row in df.iterrows():
    if index > -1:
        query = query_builder(row)
        url = get_api('UPDATE') + parse_query(query)
        r = requests.post(url, headers=get_headers())
        print("Query: \n" + query)
        print("Response: \n" + r.content.decode())
        if r.content.decode().find("Error ") != -1:
            print("URL : \n" + url)
            break

# row = next(df.loc[df['Episode Number'] == 4].iterrows())[1]
# query = query_builder(row)
# url = get_api('UPDATE') + parse_query(query)
# r = requests.post(url, headers=get_headers())
# print("Query: \n" + query)
# print("Response: \n" + r.content.decode())
# if r.content.decode().find("Error ") != -1:
#     print("URL : \n" + url)