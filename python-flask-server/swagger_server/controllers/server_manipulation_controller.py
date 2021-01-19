import six
import json
import urllib
import requests
import connexion
import subprocess

from swagger_server import util

# absolute_path = "C:\\Users\\anaki\\Documents\\modelisation"
absolute_path = "C:\\Users\\Logtimiz\\Downloads\\tp_noter"

localhost = 'http://localhost'
port = ':3330'
base_url = localhost+port

def create():  # noqa: E501
    # Ecrire la commande pour me placer au bon endroit et lancer le serveur jena
    cmd = r'cd .. ; cd .\jena_fuseki-master ; java -jar .\out\artifacts\fuseki_jar\fuseki.jar'

    # Lançons le serveur fuseki
    result = subprocess.Popen(["powershell", "-Command", cmd])

    # Si tout s'est bien déroulé
    if result.stderr == None:
        # Afficher que tout va bien
        return 'Serveur GOT à démarrer correctement'
    # Sinon
    else:
        # Informer qu'il y a eu un soucis
        return 'Quelque chose s\'est mal passé'



def create_from_file(ontology):  # noqa: E501
    """Create a server with an owl file

     # noqa: E501

    :param ontology: 
    :type ontology: werkzeug.datastructures.FileStorage

    :rtype: object
    """
    return 'do some magic!'


def delete():  # noqa: E501
    """Delete all data

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def get_dataset():  # noqa: E501
    r = requests.get('http://localhost:3330/ds')
    content_utf8 = r.content.decode('utf-8')
    return content_utf8


def send_query(query):  # noqa: E501
    # Testons avec la première faite pendant le TP :
    # http://localhost:3330/ds?query=prefix%20famille:%20%3Chttp://www.famille.org/esirem%23%3E%20prefix%20rdf:%20%3Chttp://www.w3.org/1999/02/22-rdf-syntax-ns%23%3E%20select%20?person%20where%20{?person%20a%20famille:Personne%20.%20}
    # query value (a mettre dans swagger) pour les personnes      : prefix famille: <http://www.famille.org/esirem%23> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns%23> select ?person where {?person a famille:Personne . }
    # query value (a mettre dans swagger) pour les petits enfants : prefix famille: <http://www.famille.org/esirem%23> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns%23> select ?petitEnfant ?grandParent where { ?petitEnfant famille:Petit_enfant_de ?grandParent . }
    
    query = urllib.parse.unquote(query)
    query = urllib.parse.quote(query, safe="")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "application/sparql-result+json"
    }
    
    url =  base_url + '/ds/' + '?query=' + query
    # return url
    r = requests.get(url)
    return json.loads(r.content.decode())

def stop():  # noqa: E501
    """Stop the server

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def update(query):  # noqa: E501
    # query (a mettre dans swagger) : prefix famille: <http://www.famille.org/esirem%23> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns%23> insert data {famille:Pierre famille:Fils_de famille:Jacques}
    query = urllib.parse.unquote(query)
    query = urllib.parse.quote(query, safe="")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "application/sparql-result+json"
    }

    url = 'http://localhost:3330/ds?update={}'.format(query)

    r = requests.post(url, headers=headers)
    return r.content.decode()