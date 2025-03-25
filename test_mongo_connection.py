from mongodb.mongo_connection import get_mongo_connection

def test_connection():
    db = get_mongo_connection()
    # Vérifie si la base de données est correctement connectée
    if db is not None:  # Utiliser 'is not None' au lieu de 'if db'
        print(f"Connexion réussie à la base de données : {db.name}")
        print(f"Collections disponibles : {db.list_collection_names()}")
    else:
        print("Échec de la connexion à MongoDB.")

if __name__ == "__main__":
    test_connection()
