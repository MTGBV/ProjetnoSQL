from py2neo import Graph
from mongo_connection import get_mongo_connection

# Connexion à Neo4j
graph = Graph("neo4j+s://668f3c6c.databases.neo4j.io", auth=("neo4j", "XyMdTepNHjyG2vKTDTCRP07GzpUG7u0rW5aNNTIy2vQ"))  # Utilise tes informations d'authentification Neo4j

# Connexion à MongoDB
db = get_mongo_connection()
collection = db["films"]

# Fonction pour insérer des films, acteurs et réalisateurs dans Neo4j
def insert_data_to_neo4j():
    for film in collection.find():
        # Créer un nœud Film
        film_node = graph.merge({"title": film["title"]}, "Film", "title")
        
        # Ajouter des nœuds pour les acteurs
        actors = film["Actors"].split(",")  # Les acteurs sont séparés par des virgules
        for actor in actors:
            actor_node = graph.merge({"name": actor.strip()}, "Actor", "name")
            film_node.relationships.create("ACTED_IN", actor_node)
        
        # Ajouter un nœud pour le réalisateur
        director = film["Director"]
        director_node = graph.merge({"name": director}, "Director", "name")
        film_node.relationships.create("DIRECTED", director_node)

# Appeler la fonction pour insérer les données dans Neo4j
insert_data_to_neo4j()
