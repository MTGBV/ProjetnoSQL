import json
from neo4j_connection import get_neo4j_driver

def load_data_to_neo4j(json_path="data/films_export.json"):
    driver = get_neo4j_driver()
    with driver.session() as session:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
            for film in data:
                session.execute_write(create_film_graph, film)

def create_film_graph(tx, film):
    # Extraction sécurisée
    film_id = film.get("id")
    title = film.get("title")
    year = film.get("year")
    votes = film.get("Votes", 0)
    revenue = film.get("Revenue", 0.0)
    rating = film.get("rating", "unrated")
    director = film.get("director", "")
    actors = film.get("actors", [])
    genres = film.get("genres", [])  # maintenant une liste !

    try:
        revenue = float(revenue)
    except:
        revenue = 0.0

    # Création du noeud Film
    tx.run("""
        MERGE (f:Film {id: $id})
        SET f.title = $title,
            f.year = $year,
            f.votes = $votes,
            f.revenue = $revenue,
            f.rating = $rating,
            f.director = $director
    """, id=film_id, title=title, year=year, votes=votes,
         revenue=revenue, rating=rating, director=director)

    # Création du noeud Réalisateur et relation
    if director:
        tx.run("""
            MERGE (r:Director {name: $director})
            WITH r
            MATCH (f:Film {id: $id})
            MERGE (r)-[:DIRECTED]->(f)
        """, director=director, id=film_id)

    # Création des acteurs et relations
    for actor in actors:
        tx.run("""
            MERGE (a:Actor {name: $actor})
            WITH a
            MATCH (f:Film {id: $id})
            MERGE (a)-[:ACTED_IN]->(f)
        """, actor=actor, id=film_id)

    # Création des genres et relations
    for genre in genres:
        tx.run("""
            MERGE (g:Genre {name: $genre})
            WITH g
            MATCH (f:Film {id: $id})
            MERGE (f)-[:HAS_GENRE]->(g)
        """, genre=genre, id=film_id)

if __name__ == "__main__":
    load_data_to_neo4j()
