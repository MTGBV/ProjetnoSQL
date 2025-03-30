from mongo_connection import get_mongo_connection
import json

def export_mongodb_films_for_neo4j(output_path="data/films_export.json"):
    db = get_mongo_connection()
    collection = db["films"]

    result = collection.find({
        "Actors": {"$exists": True, "$ne": ""},
        "Director": {"$exists": True, "$ne": ""}
    }, {
        "_id": 1,
        "title": 1,
        "year": 1,
        "Votes": 1,
        "Revenue (Millions)": 1,
        "rating": 1,
        "Director": 1,
        "Actors": 1,
        "genre": 1  # <-- Ajout ici pour être sûr que le champ est inclus
    })

    cleaned = []
    for doc in result:
        # Traitement du champ genre (peut être une string comme "Drama,Action")
        genres_raw = doc.get("genre", "")
        genres = [g.strip() for g in genres_raw.split(",")] if genres_raw else []

        cleaned.append({
            "id": str(doc["_id"]),
            "title": doc.get("title"),
            "year": doc.get("year"),
            "Votes": doc.get("Votes"),
            "Revenue": doc.get("Revenue (Millions)"),
            "rating": doc.get("rating"),
            "director": doc.get("Director"),
            "actors": [a.strip() for a in doc.get("Actors", "").split(",")],
            "genres": genres  # <-- champs genre bien transformé en liste
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"✅ Export terminé. Fichier enregistré dans {output_path}")

if __name__ == "__main__":
    export_mongodb_films_for_neo4j()
