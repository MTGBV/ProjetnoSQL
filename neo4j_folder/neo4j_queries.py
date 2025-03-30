from neo4j_folder.neo4j_connection import get_neo4j_driver

driver = get_neo4j_driver()

#test de connexion
with driver.session() as session:
    result = session.run("RETURN 'Connexion réussie avec Neo4j Aura!' AS message")
    for record in result:
        print(record["message"])

#question 14
def get_top_actor_by_film_count():
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    RETURN a.name AS actor, COUNT(f) AS film_count
    ORDER BY film_count DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query)
        return result.single()

#question 15
def get_actors_who_played_with_anne_hathaway():
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(anne:Actor {name: "Anne Hathaway"})
    WHERE a.name <> "Anne Hathaway"
    RETURN DISTINCT a.name AS actor
    """
    with driver.session() as session:
        return [record["actor"] for record in session.run(query)]

#question 16
from neo4j_folder.neo4j_connection import get_neo4j_driver

def get_top_actor_by_revenue():
    driver = get_neo4j_driver()
    with driver.session() as session:
        query = """
        MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
        WHERE f.revenue IS NOT NULL
        WITH a.name AS actor, SUM(f.revenue) AS total_revenue
        RETURN actor, total_revenue
        ORDER BY total_revenue DESC
        LIMIT 1
        """
        result = session.run(query)
        record = result.single()
        if record:
            return {
                "actor": record["actor"],
                "total_revenue": record["total_revenue"]
            }
        else:
            return None

#question 17
def get_average_votes():
    query = """
    MATCH (f:Film)
    WHERE f.votes IS NOT NULL
    RETURN AVG(f.votes) AS average_votes
    """
    with driver.session() as session:
        return session.run(query).single()["average_votes"]
    
#question 18
def get_most_common_genre():
    query = """
    MATCH (f:Film)-[:HAS_GENRE]->(g:Genre)
    RETURN g.name AS genre, COUNT(*) AS occurrence
    ORDER BY occurrence DESC
    LIMIT 1
    """
    driver = get_neo4j_driver()
    with driver.session() as session:
        result = session.run(query).single()
        return result if result else None

#question 19
def get_films_with_my_coactors(my_name="Ton Nom"):
    query = """
    MATCH (me:Actor {name: $my_name})-[:ACTED_IN]->(myFilm:Film)<-[:ACTED_IN]-(coactor:Actor)
    MATCH (coactor)-[:ACTED_IN]->(otherFilm:Film)
    WHERE NOT (me)-[:ACTED_IN]->(otherFilm)
    RETURN DISTINCT otherFilm.title AS title
    LIMIT 20
    """
    with driver.session() as session:
        results = session.run(query, my_name=my_name)
        return [record["title"] for record in results]

#question 20
def get_director_with_most_actors():
    query = """
    MATCH (d:Director)-[:DIRECTED]->(f:Film)<-[:ACTED_IN]-(a:Actor)
    RETURN d.name AS director, COUNT(DISTINCT a) AS actor_count
    ORDER BY actor_count DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query).single()
        return {"director": result["director"], "actor_count": result["actor_count"]}

#question 21
def get_most_connected_films():
    query = """
    MATCH (f1:Film)<-[:ACTED_IN]-(a:Actor)-[:ACTED_IN]->(f2:Film)
    WHERE f1 <> f2
    WITH f1, COUNT(DISTINCT f2) AS related_films
    RETURN f1.title AS film, related_films
    ORDER BY related_films DESC
    LIMIT 5
    """
    with driver.session() as session:
        return session.run(query).data()

#question 22
def get_top_actors_by_director_diversity():
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:DIRECTED]-(d:Director)
    RETURN a.name AS actor, COUNT(DISTINCT d.name) AS directors_count
    ORDER BY directors_count DESC
    LIMIT 5
    """
    with driver.session() as session:
        return session.run(query).data()

#question 23
def recommend_films_by_genre(actor_name):
    query = """
    MATCH (a:Actor {name: $actor_name})-[:ACTED_IN]->(:Film)-[:HAS_GENRE]->(g:Genre)
    WITH a, COLLECT(DISTINCT g) AS genres

    MATCH (rec:Film)-[:HAS_GENRE]->(g)
    WHERE NOT (a)-[:ACTED_IN]->(rec)
    RETURN rec.title AS recommended_film, COUNT(DISTINCT g) AS matched_genres
    ORDER BY matched_genres DESC
    LIMIT 5
    """
    with driver.session() as session:
        return session.run(query, actor_name=actor_name).data()

#question 24
def create_influence_relationships():
    query = """
    MATCH (d1:Director)-[:DIRECTED]->(:Film)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(:Film)<-[:DIRECTED]-(d2:Director)
    WHERE d1 <> d2
    WITH d1, d2, COUNT(DISTINCT g) AS shared_genres
    WHERE shared_genres >= 2
    MERGE (d1)-[:INFLUENCED_BY]->(d2)
    RETURN d1.name AS from_director, d2.name AS to_director, shared_genres
    LIMIT 10
    """
    with driver.session() as session:
        return session.run(query).data()

#question 25
def get_shortest_path_between_actors(actor1, actor2):
    query = """
    MATCH (a1:Actor {name: $actor1}), (a2:Actor {name: $actor2}),
    p = shortestPath((a1)-[*]-(a2))
    RETURN [n IN nodes(p) | 
        CASE 
            WHEN 'Actor' IN labels(n) THEN n.name
            WHEN 'Director' IN labels(n) THEN n.name
            WHEN 'Film' IN labels(n) THEN n.title
            ELSE 'Unknown'
        END
    ] AS path
    """
    with driver.session() as session:
        result = session.run(query, actor1=actor1, actor2=actor2).single()
        return result["path"] if result else None