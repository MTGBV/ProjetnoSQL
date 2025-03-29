from neo4j_connection import get_neo4j_driver

driver = get_neo4j_driver()

with driver.session() as session:
    result = session.run("RETURN 'Connexion réussie avec Neo4j Aura!' AS message")
    for record in result:
        print(record["message"])
