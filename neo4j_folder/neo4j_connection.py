from neo4j import GraphDatabase

def get_neo4j_driver():
    uri = "neo4j+s://668f3c6c.databases.neo4j.io"
    user = "neo4j"
    password = "XyMdTepNHjyG2vKTDTCRP07GzpUG7u0rW5aNNTIy2vQ"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver
