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
        "Actors": 1
    })

    cleaned = []
    for doc in result:
        cleaned.append({
            "id": str(doc["_id"]),
            "title": doc.get("title"),
            "year": doc.get("year"),
            "Votes": doc.get("Votes"),
            "Revenue": doc.get("Revenue (Millions)"),
            "rating": doc.get("rating"),
            "director": doc.get("Director"),
            "actors": [a.strip() for a in doc.get("Actors", "").split(",")]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)
