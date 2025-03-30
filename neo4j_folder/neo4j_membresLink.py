from neo4j_connection import get_neo4j_driver

def add_team_members_to_graph():
    driver = get_neo4j_driver()
    with driver.session() as session:
        members = ["Tanguy Vuillemin", "David Sidoun"]
        film_id = "13"#parce que rogue one = meilleur star wars

        for member in members:
            session.run("""
                MERGE (a:Actor {name: $name})
                WITH a
                MATCH (f:Film {id: $film_id})
                MERGE (a)-[:ACTED_IN]->(f)
            """, name=member, film_id=film_id)

if __name__ == "__main__":
    add_team_members_to_graph()
