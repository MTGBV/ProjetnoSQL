from mongodb.mongo_connection import get_mongo_connection

#question 1 : l'année avec le plus grand nombre de films sortis
def get_year_with_most_films():
    db = get_mongo_connection()  # Connexion à la base MongoDB
    collection = db["films"]  # Accède à la collection 'films'
    
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},  # Trie par nombre de films, du plus grand au plus petit
        {"$limit": 1}  # Limite à 1 résultat
    ]
    
    result = collection.aggregate(pipeline)
    
    # Récupérer l'année et le nombre de films
    for item in result:
        return item["_id"], item["count"]
    
#question 2 : trouver le nb de films apres 1999
def get_films_after_1999():
    db = get_mongo_connection()
    collection = db["films"]
    
    # Compte les films sortis après 1999
    result = collection.count_documents({"year": {"$gt": 1999}})
    
    return result

#question 3 : moyenne des votes des films en 2007
def get_average_votes_in_2007():
    db = get_mongo_connection()
    collection = db["films"]
    
    # Trouver tous les films sortis en 2007
    films_2007 = collection.find({"year": 2007})
    
    # Calculer la moyenne des votes
    total_votes = 0
    count = 0
    
    for film in films_2007:
        total_votes += film["Votes"]
        count += 1
    
    if count > 0:
        return total_votes / count
    else:
        return 0

# Question 4 : Histogramme du nombre de films par année
def get_films_count_by_year():
    db = get_mongo_connection()
    collection = db["films"]
    
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}  # Trie par année croissante
    ]
    
    result = list(collection.aggregate(pipeline))
    
    years = [item["_id"] for item in result]
    counts = [item["count"] for item in result]
    
    return years, counts

# Question 5 : Récupérer tous les genres de films uniques
def get_unique_genres():
    db = get_mongo_connection()
    collection = db["films"]

    # Récupère uniquement les champs 'genre'
    cursor = collection.find({}, {"genre": 1, "_id": 0})

    genres_set = set()

    for doc in cursor:
        if "genre" in doc and isinstance(doc["genre"], str):
            # Sépare les genres et les nettoie
            genres = [g.strip() for g in doc["genre"].split(",")]
            genres_set.update(genres)

    return sorted(list(genres_set))

# Question 6 : Film avec le plus de revenu
def get_highest_grossing_film():
    db = get_mongo_connection()
    collection = db["films"]

    film = collection.find_one(
        {"Revenue (Millions)": {"$ne": ""}},  
        sort=[("Revenue (Millions)", -1)]     
    )

    if film:
        return film["title"], film["Revenue (Millions)"]
    else:
        return None, None

# Question 7 : Réalisateurs ayant réalisé plus de 5 films
def get_directors_with_more_than_5_films():
    db = get_mongo_connection()
    collection = db["films"]

    pipeline = [
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}  # Optionnel : pour les classer du plus prolifique au moins
    ]

    result = list(collection.aggregate(pipeline))
    return [{"director": item["_id"], "film_count": item["count"]} for item in result]

#Question 8 : Quel est le genre de film qui rapporte en moyenne le plus de revenus ?
def get_movie_with_highest_revenue(collection):
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$ne": ""}}},
        {"$sort": {"Revenue (Millions)": -1}},
        {"$limit": 1},
        {"$project": {
            "_id": 0,
            "title": 1,
            "Revenue (Millions)": 1
        }}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

#Question 9
def get_genre_with_highest_average_revenue(collection):
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$ne": ""}}},  # Écarter les entrées sans revenu
        {"$project": {
            "Revenue (Millions)": 1,
            "genres": {"$split": ["$genre", ","]}
        }},
        {"$unwind": "$genres"},  # On décompose les genres multiples
        {"$group": {
            "_id": {"$trim": {"input": "$genres"}},  # Supprime les espaces
            "average_revenue": {"$avg": "$Revenue (Millions)"}
        }},
        {"$sort": {"average_revenue": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

#Question 10
def get_top_director_by_total_revenue(collection):
    pipeline = [
        {"$match": {
            "Revenue (Millions)": {"$ne": ""},
            "Director": {"$ne": ""}
        }},
        {"$group": {
            "_id": "$Director",
            "total_revenue": {"$sum": "$Revenue (Millions)"}
        }},
        {"$sort": {"total_revenue": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

#Question 11 : 
def get_top_genre_by_average_revenue(collection):
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$ne": ""}}},
        {"$project": {
            "Revenue (Millions)": 1,
            "genres": {
                "$split": ["$genre", ","]
            }
        }},
        {"$unwind": "$genres"},
        {"$project": {
            "Revenue (Millions)": 1,
            "genre": {"$trim": {"input": "$genres"}}
        }},
        {"$group": {
            "_id": "$genre",
            "average_revenue": {"$avg": "$Revenue (Millions)"}
        }},
        {"$sort": {"average_revenue": -1}},
        {"$limit": 1}
    ]

    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

#Question 12
def get_top_10_most_voted_movies(collection):
    pipeline = [
        {"$match": {"Votes": {"$exists": True, "$ne": ""}}},
        {"$sort": {"Votes": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "title": 1,
            "Votes": 1
        }}
    ]
    return list(collection.aggregate(pipeline))

#Question 13
def get_average_runtime_by_genre(collection):
    pipeline = [
        {"$match": {"genre": {"$exists": True, "$ne": ""}, "Runtime (Minutes)": {"$exists": True}}},
        {
            "$project": {
                "genre": {"$split": ["$genre", ","]},
                "Runtime (Minutes)": 1
            }
        },
        {"$unwind": "$genre"},
        {
            "$group": {
                "_id": {"$trim": {"input": "$genre"}},
                "average_runtime": {"$avg": "$Runtime (Minutes)"}
            }
        },
        {"$sort": {"average_runtime": -1}}
    ]
    return list(collection.aggregate(pipeline))
